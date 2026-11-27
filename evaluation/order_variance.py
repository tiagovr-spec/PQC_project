"""Task B (same shots and orders as 02_order_variance.ipynb) for any min-sum scaling.
Usage: python -m evaluation.order_variance --ms 0.9
"""
import argparse, pickle
import numpy as np
from ldpc import BpDecoder, mod2
from bb_code import bb_code, is_failure


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ms", type=float, default=1.0)
    ap.add_argument("--ps", default="0.03,0.04")
    ap.add_argument("--N", type=int, default=1000)
    ap.add_argument("--K", type=int, default=30)
    a = ap.parse_args()
    H_X, H_Z = bb_code()
    n = H_Z.shape[1]
    rank_HX = mod2.rank(H_X)
    for p in [float(x) for x in a.ps.split(",")]:
        rng = np.random.default_rng(7)
        E = (rng.random((a.N, n)) < p).astype(np.uint8)
        S = ((E @ H_Z.T) % 2).astype(np.uint8)
        perm_rng = np.random.default_rng(99)
        orders = [perm_rng.permutation(n) for _ in range(a.K)]
        fails = np.zeros((a.K, a.N), bool); conv = np.zeros((a.K, a.N), bool)
        for k, order in enumerate(orders):
            dec = BpDecoder(H_Z, error_rate=p, max_iter=50, bp_method="minimum_sum", ms_scaling_factor=a.ms,
                            schedule="serial", serial_schedule_order=order.tolist())
            for i in range(a.N):
                eh = dec.decode(S[i]); conv[k, i] = dec.converge
                fails[k, i] = is_failure(H_X, rank_HX, E[i], eh, dec.converge)
        dec = BpDecoder(H_Z, error_rate=p, max_iter=50, bp_method="minimum_sum", ms_scaling_factor=a.ms,
                        schedule="serial")
        fails_fixed = np.array([is_failure(H_X, rank_HX, E[i], dec.decode(S[i]), dec.converge) for i in range(a.N)])

        ler = fails.mean(1); fr = fails.mean(0)
        always_fail = (fr == 1).mean(); sensitive = 1 - (fr == 0).mean() - always_fail
        first = conv.argmax(0)
        restart = np.where(conv.any(0), fails[first, np.arange(a.N)], True)
        nonconv = (fails & ~conv).sum() / max(1, fails.sum())
        half = a.N // 2
        corr = np.corrcoef(fails[:, :half].mean(1), fails[:, half:].mean(1))[0, 1]
        print(f"ms={a.ms} p={p}: fixed {fails_fixed.mean():.4f} | orders mean {ler.mean():.4f} "
              f"range {ler.min():.4f}-{ler.max():.4f} | order-sensitive {sensitive:.1%} | "
              f"oracle {always_fail:.4f} | restart {restart.mean():.4f} | non-conv share {nonconv:.0%} | "
              f"split-half corr {corr:+.2f}", flush=True)
        pickle.dump(dict(fails=fails, conv=conv, fails_fixed=fails_fixed, orders=orders, p=p, ms=a.ms),
                    open(f"results/taskB_ms{a.ms}_p{p}.pkl", "wb"))


if __name__ == "__main__":
    main()
