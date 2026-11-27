
### code 72, min-sum scaling 1.0, p = 0.02  (N = 20000)
| method | LER ± SE | converged | non-conv share of failures | iters | vs fixed: fixed / broken / z |
|---|---|---|---|---|---|
| flooding | 0.0677 ± 0.0018 | 0.935 | 96% | 4.57 | 63 / 1029 / -29.2 |
| fixed serial | 0.0194 ± 0.0010 | 0.989 | 57% | 2.89 |  |
| random serial | 0.0226 ± 0.0010 | 0.987 | 58% | 2.90 | 214 / 277 / -2.8 |
| restart (≤30 decodes) | 0.0095 ± 0.0007 | 1.000 | 2% | 3.69 | 197 / 0 / +14.0 |
| static heuristic order | 0.0118 ± 0.0008 | 0.996 | 30% | 1.47 | 250 / 97 / +8.2 |
| per-step heuristic, early stop | 0.0199 ± 0.0010 | 1.000 | 0% | 0.19 | 194 / 204 / -0.5 |
| RL-S per-qubit Q (3a), trained on n=72, early stop | 0.0190 ± 0.0010 | 1.000 | 1% | 0.19 | 238 / 229 / +0.4 |
| RL-S shared Q (3b), trained on n=72, early stop | 0.0190 ± 0.0010 | 0.999 | 4% | 0.26 | 199 / 190 / +0.5 |
| GNN order per syndrome (2b), trained on n=72 [run1, unstable] | 0.0112 ± 0.0007 | 0.997 | 24% | 1.20 | 241 / 78 / +9.1 |
| fixed serial, tie-broken priors | 0.0094 ± 0.0007 | 1.000 | 2% | 1.57 | 235 / 35 / +12.2 |
| flooding, tie-broken priors | 0.0141 ± 0.0008 | 0.992 | 60% | 3.03 | 232 / 126 / +5.6 |
| GNN order per syndrome (2b), trained on n=72 [score L2 1e-2] | 0.0096 ± 0.0007 | 0.999 | 14% | 1.09 | 256 / 60 / +11.0 |
| per-step heuristic, no early stop | 0.0138 ± 0.0008 | 0.998 | 17% | 1.30 | 233 / 121 / +6.0 |
| RL-S per-qubit Q (3a), trained on n=72, no early stop | 0.0116 ± 0.0008 | 0.998 | 20% | 1.30 | 271 / 115 / +7.9 |
| RL-S shared Q (3b), trained on n=72, no early stop | 0.0150 ± 0.0009 | 0.996 | 26% | 1.30 | 229 / 142 / +4.5 |
| ensemble of 24 random-order decoders (Maan et al. style) | 0.0086 ± 0.0007 | 1.000 | 1% | 69.75 | 215 / 0 / +14.7 |
| BP-OSD-CS order 10 (conv = BP alone) | 0.0159 ± 0.0009 | 0.989 | 48% | 2.89 | 70 / 0 / +8.4 |
| BP-OSD-0 (conv = BP alone) | 0.0184 ± 0.0009 | 0.989 | 55% | 2.89 | 21 / 0 / +4.6 |
| ldpc serial_relative (most reliable first) | 0.0384 ± 0.0014 | 0.971 | 74% | 3.49 | 153 / 532 / -14.5 |

### code 72, min-sum scaling 1.0, p = 0.03  (N = 20000)
| method | LER ± SE | converged | non-conv share of failures | iters | vs fixed: fixed / broken / z |
|---|---|---|---|---|---|
| flooding | 0.1867 ± 0.0028 | 0.819 | 97% | 10.71 | 131 / 2557 / -46.8 |
| fixed serial | 0.0654 ± 0.0017 | 0.961 | 60% | 6.79 |  |
| random serial | 0.0728 ± 0.0018 | 0.955 | 62% | 6.84 | 610 / 759 / -4.0 |
| restart (≤30 decodes) | 0.0366 ± 0.0013 | 1.000 | 1% | 9.82 | 576 / 0 / +24.0 |
| static heuristic order | 0.0411 ± 0.0014 | 0.984 | 40% | 3.32 | 702 / 217 / +16.0 |
| per-step heuristic, early stop | 0.0612 ± 0.0017 | 1.000 | 0% | 0.57 | 583 / 500 / +2.5 |
| RL-S per-qubit Q (3a), trained on n=72, early stop | 0.0623 ± 0.0017 | 1.000 | 0% | 0.56 | 650 / 588 / +1.8 |
| RL-S shared Q (3b), trained on n=72, early stop | 0.0605 ± 0.0017 | 0.998 | 3% | 0.73 | 585 / 487 / +3.0 |
| GNN order per syndrome (2b), trained on n=72 [run1, unstable] | 0.0391 ± 0.0014 | 0.988 | 30% | 2.58 | 749 / 224 / +16.8 |
| fixed serial, tie-broken priors | 0.0352 ± 0.0013 | 0.997 | 8% | 3.08 | 705 / 100 / +21.3 |
| flooding, tie-broken priors | 0.0440 ± 0.0015 | 0.974 | 58% | 6.93 | 691 / 264 / +13.8 |
| GNN order per syndrome (2b), trained on n=72 [score L2 1e-2] | 0.0355 ± 0.0013 | 0.992 | 21% | 2.13 | 762 / 163 / +19.7 |
| per-step heuristic, no early stop | 0.0437 ± 0.0014 | 0.991 | 22% | 2.69 | 702 / 267 / +14.0 |
| RL-S per-qubit Q (3a), trained on n=72, no early stop | 0.0433 ± 0.0014 | 0.990 | 24% | 2.65 | 736 / 295 / +13.7 |
| RL-S shared Q (3b), trained on n=72, no early stop | 0.0481 ± 0.0015 | 0.986 | 29% | 2.73 | 662 / 316 / +11.1 |
| ensemble of 24 random-order decoders (Maan et al. style) | 0.0338 ± 0.0013 | 1.000 | 1% | 162.66 | 631 / 0 / +25.1 |
| BP-OSD-CS order 10 (conv = BP alone) | 0.0544 ± 0.0016 | 0.961 | 51% | 6.79 | 221 / 0 / +14.9 |
| BP-OSD-0 (conv = BP alone) | 0.0609 ± 0.0017 | 0.961 | 57% | 6.79 | 91 / 0 / +9.5 |
| ldpc serial_relative (most reliable first) | 0.1099 ± 0.0022 | 0.913 | 79% | 8.18 | 445 / 1334 / -21.1 |

### code 72, min-sum scaling 1.0, p = 0.04  (N = 20000)
| method | LER ± SE | converged | non-conv share of failures | iters | vs fixed: fixed / broken / z |
|---|---|---|---|---|---|
| flooding | 0.3363 ± 0.0033 | 0.673 | 97% | 18.04 | 478 / 2114 / -32.1 |
| fixed serial | 0.2545 ± 0.0031 | 0.773 | 89% | 14.10 |  |
| random serial | 0.2530 ± 0.0031 | 0.776 | 88% | 13.76 | 1265 / 1235 / +0.6 |
| restart (≤30 decodes) | 0.0948 ± 0.0021 | 0.973 | 29% | 102.43 | 3195 / 0 / +56.5 |
| static heuristic order | 0.1503 ± 0.0025 | 0.888 | 74% | 7.55 | 2339 / 255 / +40.9 |
| per-step heuristic, early stop | 0.1500 ± 0.0025 | 0.998 | 1% | 1.09 | 2480 / 391 / +39.0 |
| RL-S per-qubit Q (3a), trained on n=72, early stop | 0.1504 ± 0.0025 | 0.998 | 1% | 1.02 | 2658 / 576 / +36.6 |
| RL-S shared Q (3b), trained on n=72, early stop | 0.1464 ± 0.0025 | 0.991 | 6% | 1.56 | 2516 / 354 / +40.4 |
| GNN order per syndrome (2b), trained on n=72 [run1, unstable] | 0.1210 ± 0.0023 | 0.918 | 68% | 5.89 | 2951 / 280 / +47.0 |
| fixed serial, tie-broken priors | 0.0819 ± 0.0019 | 0.990 | 12% | 5.19 | 3519 / 68 / +57.6 |
| flooding, tie-broken priors | 0.1054 ± 0.0022 | 0.938 | 59% | 12.03 | 3251 / 269 / +50.3 |
| GNN order per syndrome (2b), trained on n=72 [score L2 1e-2] | 0.1019 ± 0.0021 | 0.940 | 59% | 4.87 | 3228 / 176 / +52.3 |
| per-step heuristic, no early stop | 0.1447 ± 0.0025 | 0.907 | 64% | 6.40 | 2498 / 302 / +41.5 |
| RL-S per-qubit Q (3a), trained on n=72, no early stop | 0.1411 ± 0.0025 | 0.912 | 63% | 6.18 | 2709 / 440 / +40.4 |
| RL-S shared Q (3b), trained on n=72, no early stop | 0.1428 ± 0.0025 | 0.911 | 62% | 6.17 | 2505 / 271 / +42.4 |
| ensemble of 24 random-order decoders (Maan et al. style) | 0.0928 ± 0.0021 | 0.968 | 34% | 339.32 | 3234 / 0 / +56.9 |
| BP-OSD-CS order 10 (conv = BP alone) | 0.2137 ± 0.0029 | 0.773 | 87% | 14.10 | 815 / 0 / +28.5 |
| BP-OSD-0 (conv = BP alone) | 0.2472 ± 0.0031 | 0.773 | 89% | 14.10 | 147 / 0 / +12.1 |
| ldpc serial_relative (most reliable first) | 0.2821 ± 0.0032 | 0.746 | 90% | 15.29 | 1008 / 1560 / -10.9 |

### code 72, min-sum scaling 1.0, p = 0.05  (N = 20000)
| method | LER ± SE | converged | non-conv share of failures | iters | vs fixed: fixed / broken / z |
|---|---|---|---|---|---|
| flooding | 0.4980 ± 0.0035 | 0.511 | 98% | 25.89 | 833 / 1979 / -21.6 |
| fixed serial | 0.4406 ± 0.0035 | 0.579 | 95% | 22.17 |  |
| random serial | 0.4364 ± 0.0035 | 0.591 | 94% | 21.63 | 1660 / 1575 / +1.5 |
| restart (≤30 decodes) | 0.2027 ± 0.0028 | 0.873 | 62% | 280.54 | 4759 / 0 / +69.0 |
| static heuristic order | 0.2787 ± 0.0032 | 0.760 | 86% | 13.09 | 3414 / 174 / +54.1 |
| per-step heuristic, early stop | 0.2547 ± 0.0031 | 0.996 | 2% | 1.74 | 3928 / 210 / +57.8 |
| RL-S per-qubit Q (3a), trained on n=72, early stop | 0.2524 ± 0.0031 | 0.997 | 1% | 1.60 | 4204 / 439 / +55.3 |
| RL-S shared Q (3b), trained on n=72, early stop | 0.2497 ± 0.0031 | 0.979 | 8% | 2.76 | 4006 / 187 / +59.0 |
| GNN order per syndrome (2b), trained on n=72 [run1, unstable] | 0.2352 ± 0.0030 | 0.809 | 81% | 10.61 | 4378 / 269 / +60.3 |
| fixed serial, tie-broken priors | 0.1514 ± 0.0025 | 0.974 | 17% | 7.90 | 5798 / 13 / +75.9 |
| flooding, tie-broken priors | 0.1829 ± 0.0027 | 0.887 | 62% | 17.85 | 5380 / 225 / +68.9 |
| GNN order per syndrome (2b), trained on n=72 [score L2 1e-2] | 0.2067 ± 0.0029 | 0.838 | 79% | 9.16 | 4855 / 176 / +66.0 |
| per-step heuristic, no early stop | 0.2657 ± 0.0031 | 0.803 | 74% | 10.96 | 3709 / 211 / +55.9 |
| RL-S per-qubit Q (3a), trained on n=72, no early stop | 0.2590 ± 0.0031 | 0.809 | 74% | 10.65 | 4052 / 419 / +54.3 |
| RL-S shared Q (3b), trained on n=72, no early stop | 0.2607 ± 0.0031 | 0.811 | 73% | 10.59 | 3790 / 192 / +57.0 |
| ensemble of 24 random-order decoders (Maan et al. style) | 0.2066 ± 0.0029 | 0.860 | 68% | 534.75 | 4682 / 0 / +68.4 |
| BP-OSD-CS order 10 (conv = BP alone) | 0.3697 ± 0.0034 | 0.579 | 95% | 22.17 | 1419 / 0 / +37.7 |
| BP-OSD-0 (conv = BP alone) | 0.4303 ± 0.0035 | 0.579 | 95% | 22.17 | 207 / 0 / +14.4 |
| ldpc serial_relative (most reliable first) | 0.4722 ± 0.0035 | 0.551 | 95% | 23.54 | 1346 / 1976 / -10.9 |