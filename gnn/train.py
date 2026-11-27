"""Train the GNN with REINFORCE (reward 1/0, baseline = mean of the other orders).
Example: python -m gnn.train --code 72 --ms 0.9 --lr 3e-4 --score_l2 1e-3 --hours 3
"""
import argparse, os, time, json
import numpy as np
import torch
from ldpc import BpDecoder, mod2
from bb_code import bb_code_poly, BB_CODES, is_failure
from gnn.model import TannerGNN, sample_orders, pl_logprob, greedy_orders, block_onehot


def make_shots(rng, H_Z, p, N):
    n = H_Z.shape[1]
    E = (rng.random((N, n)) < p).astype(np.uint8)
    return E, ((E @ H_Z.T) % 2).astype(np.uint8)


def decode_fail(dec, H_X, rank_HX, e, s, order):
    dec.serial_schedule_order = order
    eh = dec.decode(s)
    return is_failure(H_X, rank_HX, e, eh, dec.converge)


def evaluate(model, H_t, block, H_X, H_Z, rank_HX, decs, val):
    """Validation LER with the greedy order."""
    out = {}
    with torch.no_grad():
        for p, (E, S) in val.items():
            scores = model(torch.as_tensor(S, dtype=torch.long), H_t, block)
            orders = greedy_orders(scores).numpy()
            out[p] = float(np.mean([decode_fail(decs[p], H_X, rank_HX, E[i], S[i], orders[i].tolist())
                                    for i in range(len(S))]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--code", default="72")
    ap.add_argument("--ps", default="0.03,0.035,0.04,0.045")
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--K", type=int, default=8)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--d", type=int, default=32)
    ap.add_argument("--rounds", type=int, default=4)
    ap.add_argument("--max_iter", type=int, default=50)
    ap.add_argument("--ms", type=float, default=1.0)
    ap.add_argument("--val_ps", default="0.03,0.04")
    ap.add_argument("--hours", type=float, default=5.0)
    ap.add_argument("--max_steps", type=int, default=10**9)
    ap.add_argument("--val_every", type=int, default=250)
    ap.add_argument("--val_shots", type=int, default=2000)
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--tag", default="")
    ap.add_argument("--score_l2", type=float, default=0.0)  # stabilizes training
    a = ap.parse_args()
    torch.set_num_threads(a.threads)
    torch.manual_seed(a.seed)
    rng = np.random.default_rng(a.seed)

    ps = [float(x) for x in a.ps.split(",")]
    val_ps = [float(x) for x in a.val_ps.split(",")]
    # --code 72,90,144: each step uses a random code
    codes = {}
    for c in a.code.split(","):
        H_X, H_Z = bb_code_poly(**BB_CODES[c])
        H_X, H_Z = H_X.astype(np.uint8), H_Z.astype(np.uint8)
        n = H_Z.shape[1]
        mk = lambda p: BpDecoder(H_Z, error_rate=p, max_iter=a.max_iter, bp_method="minimum_sum",
                                 ms_scaling_factor=a.ms, schedule="serial", serial_schedule_order=list(range(n)))
        vrng = np.random.default_rng(555)
        codes[c] = dict(H_X=H_X, H_Z=H_Z, n=n, rank_HX=mod2.rank(H_X), H_t=torch.as_tensor(H_Z, dtype=torch.float32),
                        block=block_onehot(n), decs={p: mk(p) for p in set(ps) | set(val_ps)},
                        val={p: make_shots(vrng, H_Z, p, a.val_shots) for p in val_ps})
    for c, g in codes.items():
        for p, (E, S) in g["val"].items():
            fixed = np.mean([decode_fail(g["decs"][p], g["H_X"], g["rank_HX"], E[i], S[i], list(range(g["n"])))
                             for i in range(len(S))])
            print(f"[val baseline] code {c} p={p}: fixed serial {fixed:.4f}", flush=True)

    def validate():
        return {f"{c}_{p}": x for c, g in codes.items()
                for p, x in evaluate(model, g["H_t"], g["block"], g["H_X"], g["H_Z"], g["rank_HX"], g["decs"], g["val"]).items()}

    model = TannerGNN(a.d, a.rounds)
    opt = torch.optim.Adam(model.parameters(), lr=a.lr)
    os.makedirs("results", exist_ok=True)
    name = f"gnn_{a.code.replace(',', '-')}{a.tag}"
    best, hist = 1e9, []
    t0 = time.time()
    v = validate()
    print(f"[step 0] val greedy LER {v} (untrained)", flush=True)

    step = 0
    while time.time() - t0 < a.hours * 3600 and step < a.max_steps:
        step += 1
        c = list(codes)[rng.integers(len(codes))]
        g = codes[c]
        H_X, H_Z, n, rank_HX, H_t, block, decs = (g[k] for k in ("H_X", "H_Z", "n", "rank_HX", "H_t", "block", "decs"))
        pshot = rng.choice(ps, size=a.batch)
        E = np.zeros((a.batch, n), np.uint8)
        for i, p in enumerate(pshot):
            E[i] = (rng.random(n) < p)
        S = ((E @ H_Z.T) % 2).astype(np.uint8)

        S_t = torch.as_tensor(S, dtype=torch.long)
        scores = model(S_t, H_t, block)
        with torch.no_grad():
            orders = sample_orders(scores.detach(), a.K)
        on = orders.numpy()
        R = np.zeros((a.batch, a.K), np.float32)
        for i in range(a.batch):
            if not S[i].any():
                R[i] = 1.0
                continue
            for k in range(a.K):
                R[i, k] = 1.0 - decode_fail(decs[pshot[i]], H_X, rank_HX, E[i], S[i], on[i, k].tolist())
        R_t = torch.as_tensor(R)
        adv = R_t - (R_t.sum(1, keepdim=True) - R_t) / (a.K - 1)
        logp = pl_logprob(scores, orders)
        centered = scores - scores.mean(1, keepdim=True)
        loss = -(adv * logp).mean() + a.score_l2 * (centered ** 2).mean()
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()

        if step % 50 == 0:
            sens = float(((R.min(1) == 0) & (R.max(1) == 1)).mean())
            print(f"step {step}  mean reward {R.mean():.4f}  order-sensitive in batch {sens:.3f}  "
                  f"score std {centered.std().item():.2f}  "
                  f"loss {loss.item():+.4f}  [{(time.time()-t0)/60:.1f} min]", flush=True)
        if step % a.val_every == 0:
            v = validate()
            m = float(np.mean(list(v.values())))
            hist.append(dict(step=step, minutes=(time.time() - t0) / 60, **{str(k): x for k, x in v.items()}))
            tag = ""
            if m < best:
                best = m
                torch.save(dict(state=model.state_dict(), args=vars(a), step=step, val=v), f"results/{name}_best.pt")
                tag = "  * saved best"
            print(f"[val step {step}] greedy LER {v}{tag}", flush=True)
            json.dump(hist, open(f"results/{name}_val_history.json", "w"))
    torch.save(dict(state=model.state_dict(), args=vars(a), step=step), f"results/{name}_last.pt")
    print("done", step, "steps", flush=True)


if __name__ == "__main__":
    main()
