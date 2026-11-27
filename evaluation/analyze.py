"""Tables (LER, convergence, McNemar test vs fixed serial) and plots from evaluate.py results.
Usage: python -m evaluation.analyze --code 72 --ms 0.9
"""
import argparse, os, pickle
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PRETTY = {
    "flooding": "flooding",
    "fixed": "fixed serial",
    "random": "random serial",
    "serial_relative": "ldpc serial_relative (most reliable first)",
    "restart30": "restart (≤30 decodes)",
    "fixed_jitter": "fixed serial, tie-broken priors",
    "flooding_jitter": "flooding, tie-broken priors",
    "static_heur": "static heuristic order",
    "step_heur": "per-step heuristic, early stop",
    "step_heur_noES": "per-step heuristic, no early stop",
    "ensemble24": "ensemble of 24 random-order decoders (Maan et al. style)",
    "bposd_cs10": "BP-OSD-CS order 10 (conv = BP alone)",
    "bposd0": "BP-OSD-0 (conv = BP alone)",
}


def pretty(m):
    if m in PRETTY:
        return PRETTY[m]
    if m.startswith("rls:") or m.startswith("rlsNoES:"):
        f = m.split("/")[-1]
        name = "RL-S per-qubit Q (3a)" if "perqubit" in f else "RL-S shared Q (3b)"
        if "_aligned" in f:
            name += ", true-objective reward"
        if "-90-144" in f:
            name += ", mixture-trained"
        else:
            name += f", trained on n={f.rsplit('_', 2)[-2]}"
        name += ", early stop" if m.startswith("rls:") else ", no early stop"
        return name
    if m.startswith("gnn:"):
        f = m.split("/")[-1]
        return (f"GNN order per syndrome (2b), trained on n={f.split('_')[1]}"
                + (" [run1, unstable]" if "run1" in f else "")
                + (" [score L2 1e-2]" if "l2e-2" in f else " [score L2 1e-3]" if "l2e-3" in f else ""))
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--code", default="72")
    ap.add_argument("--plot_methods", default="")
    ap.add_argument("--ms", type=float, default=1.0)
    a = ap.parse_args()
    tag = a.code + ("" if a.ms == 1.0 else f"_ms{a.ms}")
    res = pickle.load(open(f"results/eval_{tag}.pkl", "rb"))
    os.makedirs("figures", exist_ok=True)
    methods = list(dict.fromkeys(m for m, _ in res))
    ps = sorted(set(p for _, p in res))

    lines = []
    for p in ps:
        lines.append(f"\n### code {a.code}, min-sum scaling {a.ms}, p = {p}  (N = {len(next(iter(res.values()))['fail'])})")
        lines.append("| method | LER ± SE | converged | non-conv share of failures | iters | vs fixed: fixed / broken / z |")
        lines.append("|---|---|---|---|---|---|")
        base = res.get(("fixed", p))
        for m in methods:
            if (m, p) not in res:
                continue
            r = res[(m, p)]
            f, N = r["fail"].mean(), len(r["fail"])
            nonconv = (r["fail"] & ~r["conv"]).sum() / max(1, r["fail"].sum())
            paired = ""
            if base is not None and m != "fixed":
                b = int((base["fail"] & ~r["fail"]).sum()); c = int((~base["fail"] & r["fail"]).sum())
                z = (b - c) / np.sqrt(b + c) if b + c else 0.0
                paired = f"{b} / {c} / {z:+.1f}"
            lines.append(f"| {pretty(m)} | {f:.4f} ± {np.sqrt(f*(1-f)/N):.4f} | {r['conv'].mean():.3f} | "
                         f"{nonconv:.0%} | {r['iters'].mean():.2f} | {paired} |")
    txt = "\n".join(lines)
    print(txt)
    open(f"results/eval_{tag}_tables.md", "w").write(txt)

    # LER vs p
    plot_m = a.plot_methods.split(",") if a.plot_methods else methods
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for m in plot_m:
        pts = [(p, res[(m, p)]["fail"].mean(), len(res[(m, p)]["fail"])) for p in ps if (m, p) in res]
        if not pts:
            continue
        x, y, N = map(np.array, zip(*pts))
        err = np.sqrt(y * (1 - y) / N)
        style = "--" if m in ("flooding", "fixed", "random", "restart30") else "-"
        ax.errorbar(x, y, yerr=err, marker="o", ls=style, capsize=3, label=pretty(m))
    ax.set_yscale("log"); ax.set_xlabel("physical error rate p"); ax.set_ylabel("logical error rate")
    ax.set_title(f"BB code n={a.code}, code capacity, min-sum BP, scaling {a.ms} (max 50 it)")
    ax.legend(fontsize=7); ax.grid(alpha=0.3, which="both")
    fig.tight_layout(); fig.savefig(f"figures/ler_vs_p_{tag}.png", dpi=200)

    # failure breakdown
    for p in ps:
        ms = [m for m in plot_m if (m, p) in res]
        nc = [(res[(m, p)]["fail"] & ~res[(m, p)]["conv"]).mean() for m in ms]
        cw = [(res[(m, p)]["fail"] & res[(m, p)]["conv"]).mean() for m in ms]
        fig, ax = plt.subplots(figsize=(7, 4))
        y = np.arange(len(ms))
        ax.barh(y, nc, label="did not converge (detectable)")
        ax.barh(y, cw, left=nc, label="converged to wrong logical (silent)")
        ax.set_yticks(y); ax.set_yticklabels([pretty(m) for m in ms], fontsize=8)
        ax.invert_yaxis(); ax.set_xlabel("fraction of shots"); ax.legend(fontsize=8)
        ax.set_title(f"Failure types, n={a.code}, p={p}")
        fig.tight_layout(); fig.savefig(f"figures/failures_{tag}_p{p}.png", dpi=200)
    print("figures saved to figures/")


if __name__ == "__main__":
    main()
