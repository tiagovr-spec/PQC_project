
### code 90, min-sum scaling 0.9, p = 0.03  (N = 10000)
| method | LER ± SE | converged | non-conv share of failures | iters | vs fixed: fixed / broken / z |
|---|---|---|---|---|---|
| flooding | 0.0138 ± 0.0012 | 0.987 | 93% | 3.18 | 2 / 71 / -8.1 |
| fixed serial | 0.0069 ± 0.0008 | 0.995 | 80% | 2.11 |  |
| random serial | 0.0065 ± 0.0008 | 0.995 | 74% | 2.10 | 16 / 12 / +0.8 |
| static heuristic order | 0.0073 ± 0.0009 | 0.994 | 78% | 1.92 | 8 / 12 / -0.9 |
| per-step heuristic, early stop | 0.0066 ± 0.0008 | 0.996 | 59% | 0.87 | 18 / 15 / +0.5 |
| per-step heuristic, no early stop | 0.0072 ± 0.0008 | 0.995 | 69% | 1.85 | 11 / 14 / -0.6 |
| RL-S shared Q (3b), trained on n=72, early stop | 0.0059 ± 0.0008 | 0.997 | 56% | 0.87 | 28 / 18 / +1.5 |
| RL-S shared Q (3b), trained on n=72, no early stop | 0.0067 ± 0.0008 | 0.996 | 57% | 1.88 | 21 / 19 / +0.3 |
| RL-S shared Q (3b), mixture-trained, no early stop | 0.0067 ± 0.0008 | 0.996 | 57% | 1.88 | 21 / 19 / +0.3 |
| ensemble of 24 random-order decoders (Maan et al. style) | 0.0044 ± 0.0007 | 0.998 | 50% | 50.02 | 25 / 0 / +5.0 |
| BP-OSD-CS order 10 (conv = BP alone) | 0.0039 ± 0.0006 | 0.995 | 64% | 2.11 | 30 / 0 / +5.5 |
| BP-OSD-0 (conv = BP alone) | 0.0056 ± 0.0007 | 0.995 | 75% | 2.11 | 13 / 0 / +3.6 |
| restart (≤30 decodes) | 0.0041 ± 0.0006 | 0.998 | 39% | 5.69 | 28 / 0 / +5.3 |
| GNN order per syndrome (2b), trained on n=72 [score L2 1e-3] | 0.0078 ± 0.0009 | 0.994 | 77% | 2.23 | 8 / 17 / -1.8 |
| RL-S shared Q (3b), trained on n=144, no early stop | 0.0057 ± 0.0008 | 0.996 | 68% | 1.87 | 26 / 14 / +1.9 |
| GNN order per syndrome (2b), trained on n=144 [score L2 1e-3] | 0.0075 ± 0.0009 | 0.994 | 87% | 2.22 | 10 / 16 / -1.2 |
| ldpc serial_relative (most reliable first) | 0.0072 ± 0.0008 | 0.994 | 79% | 2.19 | 10 / 13 / -0.6 |

### code 90, min-sum scaling 0.9, p = 0.04  (N = 10000)
| method | LER ± SE | converged | non-conv share of failures | iters | vs fixed: fixed / broken / z |
|---|---|---|---|---|---|
| flooding | 0.0460 ± 0.0021 | 0.958 | 92% | 6.07 | 15 / 183 / -11.9 |
| fixed serial | 0.0292 ± 0.0017 | 0.976 | 82% | 3.75 |  |
| random serial | 0.0259 ± 0.0016 | 0.980 | 78% | 3.69 | 66 / 33 / +3.3 |
| static heuristic order | 0.0294 ± 0.0017 | 0.975 | 84% | 3.48 | 36 / 38 / -0.2 |
| per-step heuristic, early stop | 0.0253 ± 0.0016 | 0.984 | 62% | 2.10 | 75 / 36 / +3.7 |
| per-step heuristic, no early stop | 0.0265 ± 0.0016 | 0.980 | 76% | 3.25 | 60 / 33 / +2.8 |
| RL-S shared Q (3b), trained on n=72, early stop | 0.0256 ± 0.0016 | 0.985 | 58% | 2.12 | 72 / 36 / +3.5 |
| RL-S shared Q (3b), trained on n=72, no early stop | 0.0240 ± 0.0015 | 0.985 | 61% | 3.18 | 91 / 39 / +4.6 |
| RL-S shared Q (3b), mixture-trained, no early stop | 0.0240 ± 0.0015 | 0.985 | 61% | 3.18 | 91 / 39 / +4.6 |
| ensemble of 24 random-order decoders (Maan et al. style) | 0.0195 ± 0.0014 | 0.990 | 51% | 90.17 | 97 / 0 / +9.8 |
| BP-OSD-CS order 10 (conv = BP alone) | 0.0173 ± 0.0013 | 0.976 | 69% | 3.75 | 119 / 0 / +10.9 |
| BP-OSD-0 (conv = BP alone) | 0.0240 ± 0.0015 | 0.976 | 78% | 3.75 | 52 / 0 / +7.2 |
| restart (≤30 decodes) | 0.0202 ± 0.0014 | 0.990 | 51% | 23.13 | 90 / 0 / +9.5 |
| GNN order per syndrome (2b), trained on n=72 [score L2 1e-3] | 0.0303 ± 0.0017 | 0.974 | 85% | 4.01 | 31 / 42 / -1.3 |
| RL-S shared Q (3b), trained on n=144, no early stop | 0.0261 ± 0.0016 | 0.983 | 65% | 3.22 | 78 / 47 / +2.8 |
| GNN order per syndrome (2b), trained on n=144 [score L2 1e-3] | 0.0290 ± 0.0017 | 0.976 | 84% | 3.92 | 43 / 41 / +0.2 |
| ldpc serial_relative (most reliable first) | 0.0280 ± 0.0016 | 0.977 | 83% | 3.93 | 48 / 36 / +1.3 |

### code 90, min-sum scaling 0.9, p = 0.05  (N = 10000)
| method | LER ± SE | converged | non-conv share of failures | iters | vs fixed: fixed / broken / z |
|---|---|---|---|---|---|
| flooding | 0.0989 ± 0.0030 | 0.908 | 93% | 9.90 | 32 / 302 / -14.8 |
| fixed serial | 0.0719 ± 0.0026 | 0.940 | 83% | 6.41 |  |
| random serial | 0.0689 ± 0.0025 | 0.947 | 76% | 6.28 | 106 / 76 / +2.2 |
| static heuristic order | 0.0721 ± 0.0026 | 0.940 | 83% | 5.95 | 82 / 84 / -0.2 |
| per-step heuristic, early stop | 0.0657 ± 0.0025 | 0.957 | 65% | 4.29 | 143 / 81 / +4.1 |
| per-step heuristic, no early stop | 0.0670 ± 0.0025 | 0.950 | 75% | 5.54 | 123 / 74 / +3.5 |
| RL-S shared Q (3b), trained on n=72, early stop | 0.0623 ± 0.0024 | 0.962 | 60% | 4.17 | 178 / 82 / +6.0 |
| RL-S shared Q (3b), trained on n=72, no early stop | 0.0647 ± 0.0025 | 0.960 | 61% | 5.45 | 173 / 101 / +4.3 |
| RL-S shared Q (3b), mixture-trained, no early stop | 0.0647 ± 0.0025 | 0.960 | 61% | 5.45 | 173 / 101 / +4.3 |
| ensemble of 24 random-order decoders (Maan et al. style) | 0.0534 ± 0.0022 | 0.969 | 58% | 153.73 | 185 / 0 / +13.6 |
| BP-OSD-CS order 10 (conv = BP alone) | 0.0483 ± 0.0021 | 0.940 | 75% | 6.41 | 236 / 0 / +15.4 |
| BP-OSD-0 (conv = BP alone) | 0.0618 ± 0.0024 | 0.940 | 80% | 6.41 | 101 / 0 / +10.0 |
| restart (≤30 decodes) | 0.0540 ± 0.0023 | 0.970 | 56% | 60.18 | 179 / 0 / +13.4 |
| GNN order per syndrome (2b), trained on n=72 [score L2 1e-3] | 0.0720 ± 0.0026 | 0.940 | 84% | 6.66 | 88 / 89 / -0.1 |
| RL-S shared Q (3b), trained on n=144, no early stop | 0.0620 ± 0.0024 | 0.960 | 65% | 5.35 | 169 / 70 / +6.4 |
| GNN order per syndrome (2b), trained on n=144 [score L2 1e-3] | 0.0713 ± 0.0026 | 0.940 | 85% | 6.58 | 86 / 80 / +0.5 |
| ldpc serial_relative (most reliable first) | 0.0718 ± 0.0026 | 0.941 | 82% | 6.66 | 90 / 89 / +0.1 |