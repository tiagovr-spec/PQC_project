"""Train an RL-S Q-table.
Example: python -m rls.train --layout shared --code 72 --episodes 300000 --ms 0.9 --no_early_stop
"""
import argparse, os, time
import numpy as np
from bb_code import bb_code_poly, BB_CODES
from rls.bp import build_graph
from rls.agent import train, MODE_BITS, MODE_COUNT


def layout_setup(layout, n):

    if layout == "perqubit":
        return np.zeros((8, n)), np.arange(n, dtype=np.int64), MODE_BITS
    if layout == "shared":
        return np.zeros((8, 1)), np.zeros(n, dtype=np.int64), MODE_COUNT
    raise ValueError(layout)


def heuristic_table(n):
    # not learned: most unsatisfied checks first
    Q = np.zeros((8, 1))
    for st in range(8):
        Q[st, 0] = st // 2
    return Q, np.zeros(n, dtype=np.int64), MODE_COUNT


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--layout", choices=["perqubit", "shared"], required=True)
    ap.add_argument("--code", default="72", help="comma-separated keys of BB_CODES; >1 only for shared")
    ap.add_argument("--episodes", type=int, default=100_000)
    ap.add_argument("--ps", default="0.02,0.03,0.04,0.05,0.06")
    ap.add_argument("--max_iter", type=int, default=50)
    ap.add_argument("--ms", type=float, default=1.0, help="min-sum scaling factor")
    ap.add_argument("--lr", type=float, default=0.1)
    ap.add_argument("--gamma", type=float, default=0.9)
    ap.add_argument("--eps0", type=float, default=0.6)
    ap.add_argument("--eps_min", type=float, default=0.05)
    ap.add_argument("--chunks", type=int, default=10, help="report progress this many times")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--aligned", action="store_true",
                    help="reward = +1/-1 for logically correct/incorrect final correction (true objective)")
    ap.add_argument("--no_early_stop", action="store_true",
                    help="finish every sweep; convergence (and the +1 bonus) only at sweep end")
    a = ap.parse_args()

    codes = a.code.split(",")
    if len(codes) > 1 and a.layout == "perqubit":
        raise SystemExit("per-qubit tables are tied to one code; mixtures need --layout shared")
    ps = np.array([float(x) for x in a.ps.split(",")])

    from ldpc import mod2
    setups, kernels = [], {}
    for c in codes:
        H_X, H_Z = bb_code_poly(**BB_CODES[c])
        g = build_graph(H_Z)
        Kc = mod2.kernel(H_X)
        kernels[c] = (np.asarray(Kc.todense() if hasattr(Kc, "todense") else Kc) % 2).astype(np.uint8)
        setups.append((c, H_Z.astype(np.uint8), g))
    Q, _, mode = layout_setup(a.layout, setups[0][2]["n"])

    per_chunk = a.episodes // a.chunks
    t0 = time.time()
    for k in range(a.chunks):
        frac0, frac1 = k / a.chunks, (k + 1) / a.chunks
        e0 = a.eps0 + (a.eps_min - a.eps0) * frac0
        e1 = a.eps0 + (a.eps_min - a.eps0) * frac1
        conv = []
        for c, H, g in setups:
            _, slot, _ = layout_setup(a.layout, g["n"])
            conv.append(train(Q, slot, mode, H, ps, per_chunk // len(setups), a.ms, a.max_iter,
                              g["e_row"], g["e_col"], g["col_ptr"], g["col_edges"],
                              g["row_ptr"], g["row_edges"], a.lr, a.gamma, e0, e1,
                              a.seed * 1000 + k * 10 + len(conv), not a.no_early_stop,
                              1 if a.aligned else 0, kernels[c]))
        print(f"chunk {k+1}/{a.chunks}  eps {e0:.2f}->{e1:.2f}  train convergence "
              + " ".join(f"{c}:{v:.3f}" for (c, _, _), v in zip(setups, conv))
              + f"  [{time.time()-t0:.0f}s]", flush=True)

    os.makedirs("results", exist_ok=True)
    ms_tag = "" if a.ms == 1.0 else f"_ms{a.ms}"
    out = (f"results/rls_{a.layout}{'_aligned' if a.aligned else ''}{'_noES' if a.no_early_stop else ''}"
           f"{ms_tag}_{'-'.join(codes)}_{a.episodes}.npz")
    np.savez(out, Q=Q, mode=mode, layout=a.layout, codes=codes, ps=ps, early_stop=not a.no_early_stop, ms=a.ms, aligned=a.aligned, **{
        k: getattr(a, k) for k in ("episodes", "max_iter", "lr", "gamma", "eps0", "eps_min", "seed")})
    print("saved", out)
    if a.layout == "shared":
        print("learned shared table (rows: #unsatisfied checks, cols: current bit 0/1):")
        print(np.round(Q[:, 0].reshape(4, 2), 3))


if __name__ == "__main__":
    main()
