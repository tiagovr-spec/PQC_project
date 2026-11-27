
### code 144, min-sum scaling 0.9, p = 0.03  (N = 10000)
| method | LER ± SE | converged | non-conv share of failures | iters | vs fixed: fixed / broken / z |
|---|---|---|---|---|---|
| flooding | 0.0117 ± 0.0011 | 0.989 | 97% | 3.54 | 1 / 93 / -9.5 |
| fixed serial | 0.0025 ± 0.0005 | 0.998 | 76% | 2.07 |  |
| random serial | 0.0017 ± 0.0004 | 0.999 | 71% | 2.05 | 11 / 3 / +2.1 |
| static heuristic order | 0.0029 ± 0.0005 | 0.998 | 76% | 1.88 | 4 / 8 / -1.2 |
| per-step heuristic, early stop | 0.0025 ± 0.0005 | 0.999 | 56% | 0.83 | 10 / 10 / +0.0 |
| per-step heuristic, no early stop | 0.0021 ± 0.0005 | 0.999 | 71% | 1.82 | 11 / 7 / +0.9 |
| RL-S shared Q (3b), trained on n=72, early stop | 0.0023 ± 0.0005 | 0.999 | 48% | 0.81 | 10 / 8 / +0.5 |
| RL-S shared Q (3b), trained on n=72, no early stop | 0.0027 ± 0.0005 | 0.999 | 44% | 1.79 | 10 / 12 / -0.4 |
| RL-S shared Q (3b), mixture-trained, no early stop | 0.0027 ± 0.0005 | 0.999 | 44% | 1.79 | 10 / 12 / -0.4 |
| ensemble of 24 random-order decoders (Maan et al. style) | 0.0011 ± 0.0003 | 1.000 | 45% | 49.13 | 14 / 0 / +3.7 |
| BP-OSD-CS order 10 (conv = BP alone) | 0.0011 ± 0.0003 | 0.998 | 45% | 2.07 | 14 / 0 / +3.7 |
| BP-OSD-0 (conv = BP alone) | 0.0017 ± 0.0004 | 0.998 | 65% | 2.07 | 8 / 0 / +2.8 |
| restart (≤30 decodes) | 0.0012 ± 0.0003 | 1.000 | 33% | 3.05 | 13 / 0 / +3.6 |
| RL-S per-qubit Q (3a), trained on n=144, early stop | 0.0020 ± 0.0004 | 0.999 | 35% | 0.81 | 16 / 11 / +1.0 |
| GNN order per syndrome (2b), trained on n=72 [score L2 1e-3] | 0.0023 ± 0.0005 | 0.998 | 74% | 2.22 | 8 / 6 / +0.5 |
| RL-S shared Q (3b), trained on n=144, no early stop | 0.0026 ± 0.0005 | 0.999 | 31% | 1.78 | 10 / 11 / -0.2 |
| RL-S per-qubit Q (3a), trained on n=144, no early stop | 0.0018 ± 0.0004 | 0.999 | 39% | 1.78 | 15 / 8 / +1.5 |
| RL-S per-qubit Q (3a), true-objective reward, trained on n=144, no early stop | 0.0020 ± 0.0004 | 0.999 | 40% | 1.77 | 12 / 7 / +1.1 |
| GNN order per syndrome (2b), trained on n=144 [score L2 1e-3] | 0.0028 ± 0.0005 | 0.998 | 86% | 2.18 | 5 / 8 / -0.8 |
| ldpc serial_relative (most reliable first) | 0.0028 ± 0.0005 | 0.998 | 75% | 2.17 | 5 / 8 / -0.8 |

### code 144, min-sum scaling 0.9, p = 0.04  (N = 10000)
| method | LER ± SE | converged | non-conv share of failures | iters | vs fixed: fixed / broken / z |
|---|---|---|---|---|---|
| flooding | 0.0343 ± 0.0018 | 0.968 | 93% | 6.35 | 10 / 200 / -13.1 |
| fixed serial | 0.0153 ± 0.0012 | 0.988 | 76% | 3.36 |  |
| random serial | 0.0136 ± 0.0012 | 0.990 | 74% | 3.39 | 34 / 17 / +2.4 |
| static heuristic order | 0.0137 ± 0.0012 | 0.990 | 77% | 2.94 | 29 / 13 / +2.5 |
| per-step heuristic, early stop | 0.0127 ± 0.0011 | 0.992 | 66% | 1.78 | 44 / 18 / +3.3 |
| per-step heuristic, no early stop | 0.0126 ± 0.0011 | 0.991 | 73% | 2.84 | 42 / 15 / +3.6 |
| RL-S shared Q (3b), trained on n=72, early stop | 0.0126 ± 0.0011 | 0.994 | 52% | 1.74 | 48 / 21 / +3.3 |
| RL-S shared Q (3b), trained on n=72, no early stop | 0.0121 ± 0.0011 | 0.995 | 38% | 2.69 | 59 / 27 / +3.5 |
| RL-S shared Q (3b), mixture-trained, no early stop | 0.0121 ± 0.0011 | 0.995 | 38% | 2.69 | 59 / 27 / +3.5 |
| ensemble of 24 random-order decoders (Maan et al. style) | 0.0119 ± 0.0011 | 0.994 | 53% | 80.20 | 34 / 0 / +5.8 |
| BP-OSD-CS order 10 (conv = BP alone) | 0.0102 ± 0.0010 | 0.988 | 64% | 3.36 | 51 / 0 / +7.1 |
| BP-OSD-0 (conv = BP alone) | 0.0130 ± 0.0011 | 0.988 | 72% | 3.36 | 23 / 0 / +4.8 |
| restart (≤30 decodes) | 0.0111 ± 0.0010 | 0.994 | 51% | 13.67 | 42 / 0 / +6.5 |
| RL-S per-qubit Q (3a), trained on n=144, early stop | 0.0127 ± 0.0011 | 0.993 | 54% | 1.75 | 48 / 22 / +3.1 |
| GNN order per syndrome (2b), trained on n=72 [score L2 1e-3] | 0.0138 ± 0.0012 | 0.990 | 75% | 3.61 | 30 / 15 / +2.2 |
| RL-S shared Q (3b), trained on n=144, no early stop | 0.0120 ± 0.0011 | 0.994 | 49% | 2.71 | 50 / 17 / +4.0 |
| RL-S per-qubit Q (3a), trained on n=144, no early stop | 0.0124 ± 0.0011 | 0.993 | 55% | 2.73 | 49 / 20 / +3.5 |
| RL-S per-qubit Q (3a), true-objective reward, trained on n=144, no early stop | 0.0120 ± 0.0011 | 0.995 | 45% | 2.69 | 51 / 18 / +4.0 |
| GNN order per syndrome (2b), trained on n=144 [score L2 1e-3] | 0.0148 ± 0.0012 | 0.989 | 74% | 3.55 | 24 / 19 / +0.8 |
| ldpc serial_relative (most reliable first) | 0.0138 ± 0.0012 | 0.990 | 75% | 3.63 | 28 / 13 / +2.3 |

### code 144, min-sum scaling 0.9, p = 0.05  (N = 10000)
| method | LER ± SE | converged | non-conv share of failures | iters | vs fixed: fixed / broken / z |
|---|---|---|---|---|---|
| flooding | 0.0875 ± 0.0028 | 0.917 | 95% | 10.87 | 21 / 393 / -18.3 |
| fixed serial | 0.0503 ± 0.0022 | 0.961 | 78% | 5.88 |  |
| random serial | 0.0458 ± 0.0021 | 0.966 | 74% | 5.87 | 93 / 48 / +3.8 |
| static heuristic order | 0.0498 ± 0.0022 | 0.960 | 81% | 5.40 | 61 / 56 / +0.5 |
| per-step heuristic, early stop | 0.0469 ± 0.0021 | 0.966 | 72% | 4.04 | 88 / 54 / +2.9 |
| per-step heuristic, no early stop | 0.0468 ± 0.0021 | 0.964 | 77% | 5.14 | 82 / 47 / +3.1 |
| RL-S shared Q (3b), trained on n=72, early stop | 0.0414 ± 0.0020 | 0.977 | 56% | 3.70 | 146 / 57 / +6.2 |
| RL-S shared Q (3b), trained on n=72, no early stop | 0.0419 ± 0.0020 | 0.979 | 49% | 4.63 | 157 / 73 / +5.5 |
| RL-S shared Q (3b), mixture-trained, no early stop | 0.0419 ± 0.0020 | 0.979 | 49% | 4.63 | 157 / 73 / +5.5 |
| ensemble of 24 random-order decoders (Maan et al. style) | 0.0364 ± 0.0019 | 0.980 | 56% | 141.53 | 139 / 0 / +11.8 |
| BP-OSD-CS order 10 (conv = BP alone) | 0.0351 ± 0.0018 | 0.961 | 69% | 5.88 | 152 / 0 / +12.3 |
| BP-OSD-0 (conv = BP alone) | 0.0429 ± 0.0020 | 0.961 | 75% | 5.88 | 74 / 0 / +8.6 |
| restart (≤30 decodes) | 0.0359 ± 0.0019 | 0.980 | 55% | 40.59 | 144 / 0 / +12.0 |
| RL-S per-qubit Q (3a), trained on n=144, early stop | 0.0422 ± 0.0020 | 0.976 | 56% | 3.62 | 129 / 48 / +6.1 |
| GNN order per syndrome (2b), trained on n=72 [score L2 1e-3] | 0.0501 ± 0.0022 | 0.959 | 83% | 6.25 | 56 / 54 / +0.2 |
| RL-S shared Q (3b), trained on n=144, no early stop | 0.0409 ± 0.0020 | 0.976 | 59% | 4.70 | 143 / 49 / +6.8 |
| RL-S per-qubit Q (3a), trained on n=144, no early stop | 0.0406 ± 0.0020 | 0.978 | 53% | 4.57 | 150 / 53 / +6.8 |
| RL-S per-qubit Q (3a), true-objective reward, trained on n=144, no early stop | 0.0407 ± 0.0020 | 0.978 | 54% | 4.57 | 150 / 54 / +6.7 |
| GNN order per syndrome (2b), trained on n=144 [score L2 1e-3] | 0.0489 ± 0.0022 | 0.960 | 81% | 6.05 | 62 / 48 / +1.3 |
| ldpc serial_relative (most reliable first) | 0.0499 ± 0.0022 | 0.961 | 79% | 6.29 | 64 / 60 / +0.4 |