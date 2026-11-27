"""Figures in figures/ (one per result). Usage: python -m evaluation.figures"""
import os, pickle
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("figures", exist_ok=True)
plt.rcParams.update({"font.size": 12, "axes.spines.top": False, "axes.spines.right": False,
                     "font.family": "sans-serif"})
COL = {"flooding": "#9AA5B1", "fixed": "#0B1F3A", "random": "#6C8EBF", "gnn": "#D9482B",
       "gnn_mix": "#F08C6E", "rls": "#138A7E", "ensemble": "#E3A33B", "bposd": "#7A5C99", "restart": "#B8C4CF"}
GNN1 = "gnn:results/gnn_72_l2e-2_best.pt"            # GNN trained at SF 1.0
GNNMIX = "gnn:results/gnn_72-90-144_l2e-2_best.pt"   # GNN trained on a mixture of codes, SF 1.0
GNN9 = "gnn:results/gnn_72_ms0.9_l2e-3_best.pt"      # GNN trained at SF 0.9
RLS9 = "rlsNoES:results/rls_shared_noES_ms0.9_72_300000.npz"


def load(path):
    return pickle.load(open(path, "rb")) if os.path.exists(path) else {}


def ler(res, m, p):
    f = res[(m, p)]["fail"].mean()
    return f, np.sqrt(f * (1 - f) / len(res[(m, p)]["fail"]))


def save(fig, name):
    fig.tight_layout()
    fig.savefig(f"figures/{name}", dpi=200)
    plt.close(fig)


e1 = {c: load(f"results/eval_{c}.pkl") for c in ("72", "90", "144")}
e9 = {c: load(f"results/eval_{c}_ms0.9.pkl") for c in ("72", "90", "144")}
ps = [0.02, 0.03, 0.04, 0.05]

# Task A: flooding vs fixed vs random serial on [[72]], SF 1.0
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4))
for m, lab in [("flooding", "flooding"), ("fixed", "fixed serial"), ("random", "random serial")]:
    y = [ler(e1["72"], m, p) for p in ps]
    a1.errorbar(ps, [v[0] for v in y], yerr=[v[1] for v in y], marker="o", capsize=3, color=COL[m], label=lab)
    a2.plot(ps, [e1["72"][(m, p)]["iters"].mean() for p in ps], marker="o", color=COL[m], label=lab)
a1.set_yscale("log"); a1.set_xlabel("physical error rate p"); a1.set_ylabel("logical error rate")
a1.set_title("Logical error rate"); a1.legend(frameon=False); a1.grid(alpha=0.3, which="both")
a2.set_xlabel("physical error rate p"); a2.set_ylabel("average BP iterations"); a2.set_title("Convergence speed")
a2.grid(alpha=0.3)
save(fig, "taskA_baselines.png")

# Task B: 30 random orders on the same 1000 shots, SF 1.0
fig, (b1, b2) = plt.subplots(1, 2, figsize=(10, 4), gridspec_kw={"width_ratios": [1.2, 1]})
labels, shares = [], []
for i, p in enumerate([0.03, 0.04]):
    d = load(f"results/taskB_ms1.0_p{p}.pkl")
    per_order = d["fails"].mean(1)
    x = i + (np.random.default_rng(0).random(len(per_order)) - 0.5) * 0.3
    b1.scatter(x, per_order * 100, s=18, color=COL["random"], label="one random order" if i == 0 else None)
    b1.hlines(d["fails_fixed"].mean() * 100, i - 0.25, i + 0.25, color=COL["fixed"], lw=2.5,
              label="fixed order 0..71" if i == 0 else None)
    fr = d["fails"].mean(0)
    shares.append([(fr == 0).mean(), 1 - (fr == 0).mean() - (fr == 1).mean(), (fr == 1).mean()])
    labels.append(f"p = {p}")
b1.set_xticks([0, 1]); b1.set_xticklabels(labels); b1.set_ylabel("logical error rate (%)")
b1.set_title("Each dot: LER of one order"); b1.legend(frameon=False, fontsize=10); b1.set_ylim(0, 30)
shares = np.array(shares) * 100
bottom = np.zeros(2)
for j, (lab, c) in enumerate([("always correct", "#C9E4E0"), ("depends on the order", COL["gnn"]),
                              ("always wrong", COL["fixed"])]):
    b2.bar(labels, shares[:, j], bottom=bottom, color=c, label=lab, width=0.55)
    for k in range(2):
        if shares[k, j] > 4:
            b2.text(k, bottom[k] + shares[k, j] / 2, f"{shares[k, j]:.0f}%", ha="center", va="center",
                    color="white" if j else "#0B1F3A", fontsize=11)
    bottom += shares[:, j]
b2.set_ylabel("share of shots (%)"); b2.set_title("Same shot, 30 orders")
b2.legend(frameon=False, fontsize=10, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2)
save(fig, "taskB_order_variance.png")

# Task C: GNN vs the Task A baselines on [[72]], SF 1.0
fig, ax = plt.subplots(figsize=(7.2, 4.4))
for m, lab, c, ls in [("flooding", "flooding", COL["flooding"], "-"), ("fixed", "fixed serial", COL["fixed"], "-"),
                      ("random", "random serial", COL["random"], "-"),
                      ("restart30", "fixed serial + up to 30 restarts", COL["restart"], "--"),
                      (GNN1, "GNN order (one decode)", COL["gnn"], "-")]:
    y = [ler(e1["72"], m, p) for p in ps]
    ax.errorbar(ps, [v[0] for v in y], yerr=[v[1] for v in y], marker="o", capsize=3, color=c, ls=ls, label=lab,
                lw=2.5 if m == GNN1 else 1.5)
ax.set_yscale("log"); ax.set_xlabel("physical error rate p"); ax.set_ylabel("logical error rate")
ax.legend(frameon=False, fontsize=10); ax.grid(alpha=0.3, which="both")
save(fig, "taskC_gnn.png")

# Task E (and D): GNN on bigger codes, SF 1.0, p = 0.04
def transfer_plot(meths, name):
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    w = 0.8 / len(meths)
    for j, (m, lab, c) in enumerate(meths):
        vals = [ler(e1[cd], m, 0.04) for cd in ("72", "90", "144")]
        xs = np.arange(3) + (j - (len(meths) - 1) / 2) * w
        ax.bar(xs, [v[0] * 100 for v in vals], w * 0.95, yerr=[v[1] * 100 for v in vals], color=c, label=lab,
               capsize=2)
    ax.set_xticks(range(3)); ax.set_xticklabels(["[[72,12,6]]", "[[90,8,10]]", "[[144,12,12]]"])
    ax.set_ylabel("logical error rate (%)")
    ax.legend(frameon=False, fontsize=10, ncol=2, loc="lower center", bbox_to_anchor=(0.5, 1.0))
    save(fig, name)


base = [("fixed", "fixed serial", COL["fixed"]), ("random", "random serial", COL["random"]),
        (GNN1, "GNN trained on [[72]]", COL["gnn"])]
transfer_plot(base, "taskE_gnn_transfer.png")
have_mix = all((GNNMIX, 0.04) in e1[c] for c in e1)
if have_mix:
    transfer_plot(base + [(GNNMIX, "GNN trained on all three", COL["gnn_mix"])], "taskD_gnn_mixture.png")

# SF 0.9: LER vs scaling factor + all methods on [[72]]
sw = load("results/alpha_sweep.pkl")
fig, (s1, s2) = plt.subplots(1, 2, figsize=(11, 4.2), gridspec_kw={"width_ratios": [1, 1.25]})
for sched, lab, c in [("parallel", "flooding", COL["flooding"]), ("serial", "fixed serial", COL["fixed"])]:
    al = sorted(a for cd, p, s, a in sw if cd == "72" and p == 0.04 and s == sched and a > 0)
    s1.plot(al, [sw[("72", 0.04, sched, a)]["fail"].mean() * 100 for a in al], marker="o", color=c, label=lab)
s1.axvline(0.9, color="k", ls=":", lw=1); s1.text(0.885, 31, "SF 0.9", ha="right", fontsize=10)
s1.set_xlabel("min-sum scaling factor (SF)"); s1.set_ylabel("logical error rate (%)")
s1.set_title("[[72]], p = 0.04: LER vs SF"); s1.legend(frameon=False); s1.grid(alpha=0.3); s1.set_ylim(0, 36)
meth9 = [("flooding", "flooding", COL["flooding"]), ("fixed", "fixed serial", COL["fixed"]),
         ("random", "random serial", COL["random"]), (GNN9, "GNN", COL["gnn"]),
         ("ensemble24", "24 decoders", COL["ensemble"]), ("bposd_cs10", "BP-OSD", COL["bposd"])]
vals = [ler(e9["72"], m, 0.04) for m, _, _ in meth9]
s2.bar(range(len(meth9)), [v[0] * 100 for v in vals], yerr=[v[1] * 100 for v in vals], capsize=3,
       color=[c for _, _, c in meth9])
for i, v in enumerate(vals):
    s2.text(i, (v[0] + v[1]) * 100 + 0.3, f"{v[0]*100:.1f}", ha="center", fontsize=10)
s2.set_xticks(range(len(meth9))); s2.set_xticklabels([l for _, l, _ in meth9], rotation=20, ha="right")
s2.set_ylabel("logical error rate (%)"); s2.set_title("[[72]], p = 0.04, SF 0.9"); s2.set_ylim(0, 12)
save(fig, "scaling_factor.png")

# RL-S + bigger codes, SF 0.9, p = 0.04
meths = [("fixed", "fixed serial", COL["fixed"]), ("random", "random serial", COL["random"]),
         (GNN9, "GNN", COL["gnn"]), (RLS9, "RL-S (8 numbers)", COL["rls"]),
         ("ensemble24", "24 decoders", COL["ensemble"]), ("bposd_cs10", "BP-OSD", COL["bposd"])]
fig, axs = plt.subplots(1, 3, figsize=(12, 4))
for ax, cd, name in zip(axs, ("72", "90", "144"), ("[[72,12,6]]", "[[90,8,10]]", "[[144,12,12]]")):
    vals = [ler(e9[cd], m, 0.04) for m, _, _ in meths]
    ax.bar(range(len(meths)), [v[0] * 100 for v in vals], yerr=[v[1] * 100 for v in vals], capsize=3,
           color=[c for _, _, c in meths])
    top = max(v[0] for v in vals) * 100
    for i, v in enumerate(vals):
        ax.text(i, (v[0] + v[1]) * 100 + top * 0.03, f"{v[0]*100:.2f}", ha="center", fontsize=9)
    ax.set_ylim(0, top * 1.2)
    ax.set_xticks(range(len(meths))); ax.set_xticklabels([l for _, l, _ in meths], rotation=30, ha="right", fontsize=10)
    ax.set_title(name)
axs[0].set_ylabel("logical error rate (%)")
fig.suptitle("p = 0.04, SF 0.9 · GNN and RL-S trained on [[72]] only", fontsize=12)
save(fig, "rls_bigger_codes.png")
print("figures done", "(with mixture GNN)" if have_mix else "(no mixture GNN yet)")
