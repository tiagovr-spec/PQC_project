"""LER vs min-sum scaling factor (alpha = 0: ldpc adaptive). Output: results/alpha_sweep.pkl"""
import argparse, os, pickle, time
import numpy as np
from ldpc import mod2
from evaluation import evaluate
from bb_code import bb_code_poly, BB_CODES


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--codes", default="72,90,144")
    ap.add_argument("--ps", default="0.03,0.04")
    ap.add_argument("--alphas", default="0.5,0.6,0.7,0.75,0.8,0.85,0.9,0.95,1.0,0")
    ap.add_argument("--schedules", default="parallel,serial,serial_relative")
    ap.add_argument("--N", type=int, default=10000)
    a = ap.parse_args()
    out = "results/alpha_sweep.pkl"
    res = pickle.load(open(out, "rb")) if os.path.exists(out) else {}
    for code in a.codes.split(","):
        H_X, H_Z = bb_code_poly(**BB_CODES[code])
        H_X, H_Z = H_X.astype(np.uint8), H_Z.astype(np.uint8)
        rank_HX = mod2.rank(H_X)
        for p in [float(x) for x in a.ps.split(",")]:
            E, S = evaluate.shots(code, p, a.N, H_Z)
            for sched in a.schedules.split(","):
                for al in [float(x) for x in a.alphas.split(",")]:
                    t0 = time.time()
                    evaluate.MS = al
                    r = evaluate.run_ldpc(H_X, H_Z, rank_HX, p, E, S, schedule=sched)
                    res[(code, p, sched, al)] = r
                    f = r["fail"].mean()
                    print(f"[[{code}]] p={p} {sched:16s} alpha={al:<5} LER {f:.4f} ± {np.sqrt(f*(1-f)/a.N):.4f} "
                          f"conv {r['conv'].mean():.3f} iters {r['iters'].mean():.2f} [{time.time()-t0:.0f}s]", flush=True)
                    pickle.dump(res, open(out, "wb"))


if __name__ == "__main__":
    main()
