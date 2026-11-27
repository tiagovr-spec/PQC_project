"""Average order position of true error qubits vs others, by fired checks.
Usage: python -m gnn.interpret results/gnn_72_l2e-2_best.pt 0.04
"""
import sys
import numpy as np
import torch
from bb_code import bb_code_poly, BB_CODES
from gnn.model import TannerGNN, block_onehot
from evaluation.evaluate import shots

path = sys.argv[1]
p = float(sys.argv[2]) if len(sys.argv) > 2 else 0.04
_, H_Z = bb_code_poly(**BB_CODES["72"])
H_Z = H_Z.astype(np.uint8)
ck = torch.load(path, weights_only=False)
a = ck["args"]
model = TannerGNN(a["d"], a["rounds"]); model.load_state_dict(ck["state"]); model.eval()
E, S = shots("72", p, 5000, H_Z)
with torch.no_grad():
    sc = model(torch.as_tensor(S, dtype=torch.long), torch.as_tensor(H_Z, dtype=torch.float32),
               block_onehot(72)).numpy()
cnt = S.astype(int) @ H_Z.astype(int)
sc_c = sc - sc.mean(1, keepdims=True)
pos = np.argsort(np.argsort(-sc, 1, kind="stable"), 1)
err = E.astype(bool)

out = [f"GNN {path}, p={p}, 5000 shots. Position 0 = updated first, 71 = last."]
out.append("fired checks | share of qubits | mean centered score | avg position true errors | avg position others")
for k in range(4):
    mk = cnt == k
    te = pos[mk & err].mean() if (mk & err).any() else float("nan")
    out.append(f"{k} | {mk.mean():.3f} | {sc_c[mk].mean():+.2f} | {te:.1f} | {pos[mk & ~err].mean():.1f}")
out.append(f"all | | | {pos[err].mean():.1f} | {pos[~err].mean():.1f}")
txt = "\n".join(out)
print(txt)
open(path.replace(".pt", f"_interpretation_p{p}.txt"), "w").write(txt + "\n")
