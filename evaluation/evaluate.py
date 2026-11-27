"""All methods on the same test shots; per-shot results to results/eval_<code>[_ms<alpha>].pkl.
Example: python -m evaluation.evaluate --code 72 --ms 0.9 --N 20000 --methods fixed,random,ensemble24
"""
import argparse, os, pickle, time
import numpy as np
from ldpc import BpDecoder, mod2
from bb_code import bb_code_poly, BB_CODES, is_failure

MS = 1.0   # min-sum scaling factor (--ms)


def shots(code, p, N, H_Z):
    rng = np.random.default_rng(31415 + int(code) * 1000 + int(round(p * 1000)))
    n = H_Z.shape[1]
    E = (rng.random((N, n)) < p).astype(np.uint8)
    return E, ((E @ H_Z.T) % 2).astype(np.uint8)


def run_ldpc_orders(H_X, H_Z, rank_HX, p, E, S, orders, max_iter=50):
    """ldpc serial BP with one order per shot."""
    n = H_Z.shape[1]
    dec = BpDecoder(H_Z, error_rate=p, max_iter=max_iter, bp_method="minimum_sum", ms_scaling_factor=MS,
                    schedule="serial", serial_schedule_order=list(range(n)))
    N = len(S)
    fail = np.zeros(N, bool); conv = np.zeros(N, bool); its = np.zeros(N)
    for i in range(N):
        if not S[i].any():
            conv[i] = True; continue            # empty syndrome
        if orders is not None:
            dec.serial_schedule_order = orders[i].tolist()
        eh = dec.decode(S[i])
        conv[i] = dec.converge; its[i] = dec.iter
        fail[i] = is_failure(H_X, rank_HX, E[i], eh, dec.converge)
    return dict(fail=fail, conv=conv, iters=its)


def run_ldpc(H_X, H_Z, rank_HX, p, E, S, **kw):
    dec = BpDecoder(H_Z, error_rate=p, max_iter=50, bp_method="minimum_sum", ms_scaling_factor=MS, **kw)
    N = len(S)
    fail = np.zeros(N, bool); conv = np.zeros(N, bool); its = np.zeros(N)
    for i in range(N):
        if not S[i].any():
            conv[i] = True; continue
        eh = dec.decode(S[i])
        conv[i] = dec.converge; its[i] = dec.iter
        fail[i] = is_failure(H_X, rank_HX, E[i], eh, dec.converge)
    return dict(fail=fail, conv=conv, iters=its)


def run_restart(H_X, H_Z, rank_HX, p, E, S, R=30):
    # retry with random orders until BP converges
    n = H_Z.shape[1]
    prng = np.random.default_rng(99)
    orders = [list(range(n))] + [prng.permutation(n).tolist() for _ in range(R - 1)]
    dec = BpDecoder(H_Z, error_rate=p, max_iter=50, bp_method="minimum_sum", ms_scaling_factor=MS,
                    schedule="serial", serial_schedule_order=orders[0])
    N = len(S)
    fail = np.zeros(N, bool); conv = np.zeros(N, bool); its = np.zeros(N); tries = np.zeros(N)
    for i in range(N):
        if not S[i].any():
            conv[i] = True; continue
        total = 0
        for r, o in enumerate(orders):
            dec.serial_schedule_order = o
            eh = dec.decode(S[i]); total += dec.iter
            if dec.converge:
                break
        conv[i] = dec.converge; its[i] = total; tries[i] = r + 1
        fail[i] = is_failure(H_X, rank_HX, E[i], eh, dec.converge)
    return dict(fail=fail, conv=conv, iters=its, tries=tries)


def run_ensemble(H_X, H_Z, rank_HX, p, E, S, R=24):
    """R random-order decoders (Maan et al. 2026), lowest-weight converged output."""
    n = H_Z.shape[1]
    prng = np.random.default_rng(2026)
    orders = [list(range(n))] + [prng.permutation(n).tolist() for _ in range(R - 1)]
    dec = BpDecoder(H_Z, error_rate=p, max_iter=50, bp_method="minimum_sum", ms_scaling_factor=MS,
                    schedule="serial", serial_schedule_order=orders[0])
    N = len(S)
    fail = np.zeros(N, bool); conv = np.zeros(N, bool); its = np.zeros(N)
    for i in range(N):
        if not S[i].any():
            conv[i] = True; continue
        best, best_w, fallback, total = None, n + 1, None, 0
        for r, o in enumerate(orders):
            dec.serial_schedule_order = o
            eh = dec.decode(S[i]).copy(); total += dec.iter
            if r == 0:
                fallback = eh
            if dec.converge and eh.sum() < best_w:
                best, best_w = eh, eh.sum()
        conv[i] = best is not None; its[i] = total
        fail[i] = is_failure(H_X, rank_HX, E[i], best if conv[i] else fallback, conv[i])
    return dict(fail=fail, conv=conv, iters=its)


def run_bposd(H_X, H_Z, rank_HX, p, E, S, osd_method, osd_order):
    """ldpc BP-OSD."""
    from ldpc import BpOsdDecoder
    dec = BpOsdDecoder(H_Z, error_rate=p, max_iter=50, bp_method="minimum_sum", ms_scaling_factor=MS,
                       schedule="serial", osd_method=osd_method, osd_order=osd_order)
    N = len(S)
    fail = np.zeros(N, bool); conv = np.zeros(N, bool); its = np.zeros(N)
    for i in range(N):
        if not S[i].any():
            conv[i] = True; continue
        eh = dec.decode(S[i])
        conv[i] = dec.converge; its[i] = dec.iter
        fail[i] = is_failure(H_X, rank_HX, E[i], eh, True)
    return dict(fail=fail, conv=conv, iters=its)


def static_heur_orders(H_Z, S):
    cnt = S.astype(int) @ H_Z.astype(int)        # fired checks per qubit
    return np.argsort(-cnt, axis=1, kind="stable")


def gnn_orders(path, H_Z, S):
    import torch
    from gnn.model import TannerGNN, greedy_orders, block_onehot
    ck = torch.load(path, weights_only=False)
    a = ck["args"]
    model = TannerGNN(a["d"], a["rounds"]); model.load_state_dict(ck["state"]); model.eval()
    H_t = torch.as_tensor(H_Z, dtype=torch.float32)
    block = block_onehot(H_Z.shape[1])
    out = []
    with torch.no_grad():
        for b in range(0, len(S), 2000):
            sc = model(torch.as_tensor(S[b:b + 2000], dtype=torch.long), H_t, block)
            out.append(greedy_orders(sc).numpy())
    return np.concatenate(out)


def run_policy(H_X, H_Z, rank_HX, p, E, S, Q, slot, mode, early_stop=True):
    from rls.agent import PolicyDecoder
    dec = PolicyDecoder(H_Z, p, Q, slot, mode, early_stop=early_stop, ms_scaling_factor=MS)
    N = len(S)
    fail = np.zeros(N, bool); conv = np.zeros(N, bool); its = np.zeros(N)
    for i in range(N):
        eh = dec.decode(S[i])
        conv[i] = dec.converge; its[i] = dec.iter
        fail[i] = is_failure(H_X, rank_HX, E[i], eh, dec.converge)
    return dict(fail=fail, conv=conv, iters=its)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--code", default="72")
    ap.add_argument("--ps", default="0.02,0.03,0.04,0.05")
    ap.add_argument("--N", type=int, default=20000)
    ap.add_argument("--methods", required=True)
    ap.add_argument("--ms", type=float, default=1.0)
    a = ap.parse_args()
    global MS
    MS = a.ms

    H_X, H_Z = bb_code_poly(**BB_CODES[a.code])
    H_X, H_Z = H_X.astype(np.uint8), H_Z.astype(np.uint8)
    n = H_Z.shape[1]
    rank_HX = mod2.rank(H_X)
    out_path = f"results/eval_{a.code}{'' if a.ms == 1.0 else f'_ms{a.ms}'}.pkl"
    res = pickle.load(open(out_path, "rb")) if os.path.exists(out_path) else {}

    for p in [float(x) for x in a.ps.split(",")]:
        E, S = shots(a.code, p, a.N, H_Z)
        for m in a.methods.split(","):
            t0 = time.time()
            if m == "flooding":
                r = run_ldpc(H_X, H_Z, rank_HX, p, E, S, schedule="parallel")
            elif m == "fixed":
                r = run_ldpc(H_X, H_Z, rank_HX, p, E, S, schedule="serial")
            elif m == "serial_relative":
                r = run_ldpc(H_X, H_Z, rank_HX, p, E, S, schedule="serial_relative")
            elif m == "random":
                r = run_ldpc(H_X, H_Z, rank_HX, p, E, S, schedule="serial",
                             random_serial_schedule=True, random_schedule_seed=1)
            elif m in ("fixed_jitter", "flooding_jitter"):
                # tiny prior noise breaks exact min-sum ties
                jit = (p * (1 + 1e-6 * np.random.default_rng(7).standard_normal(n))).tolist()
                sched = "serial" if m == "fixed_jitter" else "parallel"
                dec = BpDecoder(H_Z, error_channel=jit, max_iter=50, bp_method="minimum_sum", ms_scaling_factor=MS, schedule=sched)
                N_ = len(S); r = dict(fail=np.zeros(N_, bool), conv=np.zeros(N_, bool), iters=np.zeros(N_))
                for i in range(N_):
                    if not S[i].any():
                        r["conv"][i] = True; continue
                    eh = dec.decode(S[i]); r["conv"][i] = dec.converge; r["iters"][i] = dec.iter
                    r["fail"][i] = is_failure(H_X, rank_HX, E[i], eh, dec.converge)
            elif m == "restart30":
                r = run_restart(H_X, H_Z, rank_HX, p, E, S)
            elif m == "ensemble24":
                r = run_ensemble(H_X, H_Z, rank_HX, p, E, S)
            elif m == "bposd_cs10":
                r = run_bposd(H_X, H_Z, rank_HX, p, E, S, "osd_cs", 10)
            elif m == "bposd0":
                r = run_bposd(H_X, H_Z, rank_HX, p, E, S, "osd0", 0)
            elif m == "static_heur":
                r = run_ldpc_orders(H_X, H_Z, rank_HX, p, E, S, static_heur_orders(H_Z, S))
            elif m.startswith("gnn:"):
                r = run_ldpc_orders(H_X, H_Z, rank_HX, p, E, S, gnn_orders(m[4:], H_Z, S))
            elif m in ("step_heur", "step_heur_noES"):
                from rls.train import heuristic_table
                Q, slot, mode = heuristic_table(n)
                r = run_policy(H_X, H_Z, rank_HX, p, E, S, Q, slot, mode, early_stop=(m == "step_heur"))
            elif m.startswith("rls:") or m.startswith("rlsNoES:"):
                d = np.load(m.split(":", 1)[1], allow_pickle=True)
                Q, mode = d["Q"], int(d["mode"])
                if Q.shape[1] == 1:
                    slot = np.zeros(n, np.int64)
                elif Q.shape[1] == n:
                    slot = np.arange(n)
                else:
                    print(f"skip {m}: per-qubit table for a different code"); continue
                r = run_policy(H_X, H_Z, rank_HX, p, E, S, Q, slot, mode,
                               early_stop=m.startswith("rls:"))
            else:
                raise ValueError(m)
            res[(m, p)] = r
            f = r["fail"].mean()
            print(f"code {a.code} p={p:.3f} {m:45s} LER {f:.4f} ± {np.sqrt(f*(1-f)/a.N):.4f}  "
                  f"conv {r['conv'].mean():.3f}  iters {r['iters'].mean():.2f}  [{time.time()-t0:.0f}s]",
                  flush=True)
            pickle.dump(res, open(out_path, "wb"))


if __name__ == "__main__":
    main()
