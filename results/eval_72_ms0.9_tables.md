
### code 72, min-sum scaling 0.9, p = 0.02  (N = 20000)
| method | LER ± SE | converged | non-conv share of failures | iters | vs fixed: fixed / broken / z |
|---|---|---|---|---|---|
| flooding | 0.0137 ± 0.0008 | 0.993 | 52% | 1.62 | 37 / 132 / -7.3 |
| fixed serial | 0.0089 ± 0.0007 | 1.000 | 4% | 1.09 |  |
| random serial | 0.0089 ± 0.0007 | 1.000 | 2% | 1.07 | 69 / 69 / +0.0 |
| restart (≤30 decodes) | 0.0089 ± 0.0007 | 1.000 | 0% | 1.19 | 0 / 0 / +0.0 |
| static heuristic order | 0.0093 ± 0.0007 | 1.000 | 4% | 1.02 | 44 / 52 / -0.8 |
| per-step heuristic, early stop | 0.0104 ± 0.0007 | 1.000 | 0% | 0.22 | 36 / 66 / -3.0 |
| per-step heuristic, no early stop | 0.0099 ± 0.0007 | 1.000 | 2% | 0.98 | 40 / 60 / -2.0 |
| RL-S per-qubit Q (3a), trained on n=72, early stop | 0.0109 ± 0.0007 | 1.000 | 0% | 0.22 | 59 / 99 / -3.2 |
| RL-S shared Q (3b), trained on n=72, early stop | 0.0112 ± 0.0007 | 1.000 | 0% | 0.22 | 45 / 91 / -3.9 |
| RL-S per-qubit Q (3a), trained on n=72, no early stop | 0.0106 ± 0.0007 | 1.000 | 0% | 0.97 | 59 / 93 / -2.8 |
| RL-S shared Q (3b), trained on n=72, no early stop | 0.0107 ± 0.0007 | 1.000 | 0% | 0.97 | 51 / 87 / -3.1 |
| fixed serial, tie-broken priors | 0.0089 ± 0.0007 | 1.000 | 4% | 1.09 | 0 / 1 / -1.0 |
| RL-S shared Q (3b), true-objective reward, trained on n=72, no early stop | 0.0102 ± 0.0007 | 1.000 | 0% | 0.98 | 58 / 84 / -2.2 |
| RL-S per-qubit Q (3a), true-objective reward, trained on n=72, no early stop | 0.0102 ± 0.0007 | 1.000 | 0% | 0.97 | 73 / 99 / -2.0 |
| GNN order per syndrome (2b), trained on n=72 [score L2 1e-2] | 0.0095 ± 0.0007 | 1.000 | 5% | 1.11 | 46 / 58 / -1.2 |
| GNN order per syndrome (2b), trained on n=72 [score L2 1e-3] | 0.0089 ± 0.0007 | 1.000 | 3% | 1.10 | 47 / 46 / +0.1 |
| ensemble of 24 random-order decoders (Maan et al. style) | 0.0088 ± 0.0007 | 1.000 | 0% | 25.67 | 3 / 0 / +1.7 |
| BP-OSD-CS order 10 (conv = BP alone) | 0.0089 ± 0.0007 | 1.000 | 4% | 1.09 | 1 / 0 / +1.0 |
| BP-OSD-0 (conv = BP alone) | 0.0089 ± 0.0007 | 1.000 | 4% | 1.09 | 1 / 0 / +1.0 |
| RL-S shared Q (3b), trained on n=144, no early stop | 0.0104 ± 0.0007 | 1.000 | 0% | 0.97 | 50 / 80 / -2.6 |
| ldpc serial_relative (most reliable first) | 0.0084 ± 0.0006 | 1.000 | 4% | 1.09 | 78 / 68 / +0.8 |

### code 72, min-sum scaling 0.9, p = 0.03  (N = 20000)
| method | LER ± SE | converged | non-conv share of failures | iters | vs fixed: fixed / broken / z |
|---|---|---|---|---|---|
| flooding | 0.0433 ± 0.0014 | 0.981 | 43% | 3.18 | 112 / 306 / -9.5 |
| fixed serial | 0.0336 ± 0.0013 | 0.998 | 6% | 1.76 |  |
| random serial | 0.0346 ± 0.0013 | 0.999 | 3% | 1.65 | 184 / 204 / -1.0 |
| restart (≤30 decodes) | 0.0335 ± 0.0013 | 1.000 | 0% | 2.16 | 3 / 0 / +1.7 |
| static heuristic order | 0.0318 ± 0.0012 | 0.998 | 6% | 1.56 | 156 / 119 / +2.2 |
| per-step heuristic, early stop | 0.0374 ± 0.0013 | 1.000 | 1% | 0.50 | 132 / 208 / -4.1 |
| per-step heuristic, no early stop | 0.0355 ± 0.0013 | 0.999 | 2% | 1.42 | 137 / 176 / -2.2 |
| RL-S per-qubit Q (3a), trained on n=72, early stop | 0.0374 ± 0.0013 | 1.000 | 0% | 0.48 | 202 / 277 / -3.4 |
| RL-S shared Q (3b), trained on n=72, early stop | 0.0380 ± 0.0014 | 1.000 | 0% | 0.47 | 132 / 220 / -4.7 |
| RL-S per-qubit Q (3a), trained on n=72, no early stop | 0.0359 ± 0.0013 | 1.000 | 0% | 1.37 | 176 / 222 / -2.3 |
| RL-S shared Q (3b), trained on n=72, no early stop | 0.0369 ± 0.0013 | 1.000 | 0% | 1.36 | 142 / 207 / -3.5 |
| fixed serial, tie-broken priors | 0.0336 ± 0.0013 | 0.998 | 6% | 1.76 | 2 / 2 / +0.0 |
| RL-S shared Q (3b), true-objective reward, trained on n=72, no early stop | 0.0355 ± 0.0013 | 1.000 | 1% | 1.40 | 180 / 217 / -1.9 |
| RL-S per-qubit Q (3a), true-objective reward, trained on n=72, no early stop | 0.0355 ± 0.0013 | 1.000 | 0% | 1.36 | 191 / 229 / -1.9 |
| GNN order per syndrome (2b), trained on n=72 [score L2 1e-2] | 0.0343 ± 0.0013 | 0.998 | 6% | 1.81 | 145 / 159 / -0.8 |
| GNN order per syndrome (2b), trained on n=72 [score L2 1e-3] | 0.0335 ± 0.0013 | 0.998 | 5% | 1.82 | 172 / 169 / +0.2 |
| ensemble of 24 random-order decoders (Maan et al. style) | 0.0334 ± 0.0013 | 1.000 | 1% | 41.59 | 4 / 0 / +2.0 |
| BP-OSD-CS order 10 (conv = BP alone) | 0.0333 ± 0.0013 | 0.998 | 6% | 1.76 | 5 / 0 / +2.2 |
| BP-OSD-0 (conv = BP alone) | 0.0333 ± 0.0013 | 0.998 | 6% | 1.76 | 5 / 0 / +2.2 |
| RL-S shared Q (3b), trained on n=144, no early stop | 0.0365 ± 0.0013 | 1.000 | 0% | 1.37 | 138 / 196 / -3.2 |
| ldpc serial_relative (most reliable first) | 0.0328 ± 0.0013 | 0.999 | 4% | 1.78 | 221 / 206 / +0.7 |

### code 72, min-sum scaling 0.9, p = 0.04  (N = 20000)
| method | LER ± SE | converged | non-conv share of failures | iters | vs fixed: fixed / broken / z |
|---|---|---|---|---|---|
| flooding | 0.0975 ± 0.0021 | 0.957 | 44% | 5.70 | 296 / 594 / -10.0 |
| fixed serial | 0.0826 ± 0.0019 | 0.992 | 10% | 2.77 |  |
| random serial | 0.0823 ± 0.0019 | 0.997 | 4% | 2.53 | 418 / 411 / +0.2 |
| restart (≤30 decodes) | 0.0819 ± 0.0019 | 0.999 | 1% | 5.93 | 14 / 0 / +3.7 |
| static heuristic order | 0.0825 ± 0.0019 | 0.992 | 9% | 2.50 | 314 / 312 / +0.1 |
| per-step heuristic, early stop | 0.0896 ± 0.0020 | 0.998 | 2% | 0.98 | 296 / 435 / -5.1 |
| per-step heuristic, no early stop | 0.0866 ± 0.0020 | 0.995 | 5% | 2.12 | 300 / 379 / -3.0 |
| RL-S per-qubit Q (3a), trained on n=72, early stop | 0.0923 ± 0.0020 | 0.999 | 1% | 0.91 | 378 / 572 / -6.3 |
| RL-S shared Q (3b), trained on n=72, early stop | 0.0909 ± 0.0020 | 1.000 | 1% | 0.89 | 343 / 508 / -5.7 |
| RL-S per-qubit Q (3a), trained on n=72, no early stop | 0.0878 ± 0.0020 | 0.999 | 2% | 1.91 | 392 / 496 / -3.5 |
| RL-S shared Q (3b), trained on n=72, no early stop | 0.0894 ± 0.0020 | 0.999 | 1% | 1.84 | 334 / 470 / -4.8 |
| fixed serial, tie-broken priors | 0.0825 ± 0.0019 | 0.992 | 9% | 2.76 | 7 / 5 / +0.6 |
| RL-S shared Q (3b), true-objective reward, trained on n=72, no early stop | 0.0862 ± 0.0020 | 0.998 | 2% | 2.00 | 400 / 471 / -2.4 |
| RL-S per-qubit Q (3a), true-objective reward, trained on n=72, no early stop | 0.0866 ± 0.0020 | 0.999 | 2% | 1.88 | 407 / 486 / -2.6 |
| GNN order per syndrome (2b), trained on n=72 [score L2 1e-2] | 0.0832 ± 0.0020 | 0.992 | 9% | 2.87 | 331 / 343 / -0.5 |
| GNN order per syndrome (2b), trained on n=72 [score L2 1e-3] | 0.0811 ± 0.0019 | 0.992 | 9% | 2.89 | 369 / 339 / +1.1 |
| ensemble of 24 random-order decoders (Maan et al. style) | 0.0814 ± 0.0019 | 0.998 | 2% | 65.71 | 23 / 0 / +4.8 |
| BP-OSD-CS order 10 (conv = BP alone) | 0.0819 ± 0.0019 | 0.992 | 9% | 2.77 | 15 / 0 / +3.9 |
| BP-OSD-0 (conv = BP alone) | 0.0820 ± 0.0019 | 0.992 | 10% | 2.77 | 11 / 0 / +3.3 |
| RL-S shared Q (3b), trained on n=144, no early stop | 0.0878 ± 0.0020 | 0.999 | 1% | 1.91 | 342 / 446 / -3.7 |
| ldpc serial_relative (most reliable first) | 0.0821 ± 0.0019 | 0.994 | 7% | 2.81 | 450 / 440 / +0.3 |

### code 72, min-sum scaling 0.9, p = 0.05  (N = 20000)
| method | LER ± SE | converged | non-conv share of failures | iters | vs fixed: fixed / broken / z |
|---|---|---|---|---|---|
| flooding | 0.1710 ± 0.0027 | 0.925 | 44% | 8.73 | 440 / 883 / -12.2 |
| fixed serial | 0.1489 ± 0.0025 | 0.980 | 14% | 4.19 |  |
| random serial | 0.1485 ± 0.0025 | 0.989 | 8% | 3.75 | 673 / 667 / +0.2 |
| restart (≤30 decodes) | 0.1470 ± 0.0025 | 0.997 | 2% | 13.00 | 37 / 0 / +6.1 |
| static heuristic order | 0.1470 ± 0.0025 | 0.981 | 13% | 3.84 | 537 / 501 / +1.1 |
| per-step heuristic, early stop | 0.1598 ± 0.0026 | 0.996 | 3% | 1.58 | 533 / 752 / -6.1 |
| per-step heuristic, no early stop | 0.1549 ± 0.0026 | 0.989 | 7% | 2.99 | 541 / 662 / -3.5 |
| RL-S per-qubit Q (3a), trained on n=72, early stop | 0.1608 ± 0.0026 | 0.998 | 1% | 1.45 | 645 / 884 / -6.1 |
| RL-S shared Q (3b), trained on n=72, early stop | 0.1585 ± 0.0026 | 0.998 | 1% | 1.40 | 538 / 731 / -5.4 |
| RL-S per-qubit Q (3a), trained on n=72, no early stop | 0.1557 ± 0.0026 | 0.996 | 2% | 2.57 | 626 / 763 / -3.7 |
| RL-S shared Q (3b), trained on n=72, no early stop | 0.1562 ± 0.0026 | 0.998 | 1% | 2.41 | 545 / 693 / -4.2 |
| fixed serial, tie-broken priors | 0.1487 ± 0.0025 | 0.980 | 13% | 4.19 | 15 / 13 / +0.4 |
| RL-S shared Q (3b), true-objective reward, trained on n=72, no early stop | 0.1560 ± 0.0026 | 0.996 | 3% | 2.77 | 605 / 747 / -3.9 |
| RL-S per-qubit Q (3a), true-objective reward, trained on n=72, no early stop | 0.1562 ± 0.0026 | 0.998 | 1% | 2.48 | 616 / 764 / -4.0 |
| GNN order per syndrome (2b), trained on n=72 [score L2 1e-2] | 0.1517 ± 0.0025 | 0.980 | 13% | 4.35 | 514 / 572 / -1.8 |
| GNN order per syndrome (2b), trained on n=72 [score L2 1e-3] | 0.1487 ± 0.0025 | 0.980 | 13% | 4.42 | 570 / 566 / +0.1 |
| ensemble of 24 random-order decoders (Maan et al. style) | 0.1469 ± 0.0025 | 0.996 | 3% | 101.43 | 40 / 0 / +6.3 |
| BP-OSD-CS order 10 (conv = BP alone) | 0.1474 ± 0.0025 | 0.980 | 13% | 4.19 | 30 / 0 / +5.5 |
| BP-OSD-0 (conv = BP alone) | 0.1475 ± 0.0025 | 0.980 | 13% | 4.19 | 26 / 0 / +5.1 |
| RL-S shared Q (3b), trained on n=144, no early stop | 0.1531 ± 0.0025 | 0.996 | 3% | 2.55 | 557 / 642 / -2.5 |
| ldpc serial_relative (most reliable first) | 0.1489 ± 0.0025 | 0.984 | 11% | 4.27 | 639 / 641 / -0.1 |