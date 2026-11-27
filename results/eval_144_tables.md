
### code 144, min-sum scaling 1.0, p = 0.03  (N = 10000)
| method | LER ± SE | converged | non-conv share of failures | iters | vs fixed: fixed / broken / z |
|---|---|---|---|---|---|
| flooding | 0.2137 ± 0.0041 | 0.786 | 100% | 13.10 | 29 / 2002 / -43.8 |
| fixed serial | 0.0164 ± 0.0013 | 0.984 | 98% | 7.29 |  |
| random serial | 0.0222 ± 0.0015 | 0.978 | 98% | 7.77 | 126 / 184 / -3.3 |
| fixed serial, tie-broken priors | 0.0033 ± 0.0006 | 0.997 | 85% | 3.72 | 135 / 4 / +11.1 |
| static heuristic order | 0.0083 ± 0.0009 | 0.992 | 98% | 3.85 | 122 / 41 / +6.3 |
| per-step heuristic, early stop | 0.0096 ± 0.0010 | 0.992 | 83% | 2.55 | 131 / 63 / +4.9 |
| per-step heuristic, no early stop | 0.0104 ± 0.0010 | 0.990 | 94% | 3.89 | 132 / 72 / +4.2 |
| RL-S shared Q (3b), trained on n=72, early stop | 0.0138 ± 0.0012 | 0.988 | 87% | 2.50 | 122 / 96 / +1.8 |
| RL-S shared Q (3b), trained on n=72, no early stop | 0.0144 ± 0.0012 | 0.987 | 93% | 3.78 | 121 / 101 / +1.3 |
| RL-S shared Q (3b), mixture-trained, no early stop | 0.0203 ± 0.0014 | 0.980 | 97% | 4.30 | 116 / 155 / -2.4 |
| GNN order per syndrome (2b), trained on n=72 [score L2 1e-2] | 0.0044 ± 0.0007 | 0.996 | 91% | 2.32 | 133 / 13 / +9.9 |
| ensemble of 24 random-order decoders (Maan et al. style) | 0.0015 ± 0.0004 | 0.999 | 47% | 179.88 | 149 / 0 / +12.2 |
| BP-OSD-CS order 10 (conv = BP alone) | 0.0102 ± 0.0010 | 0.984 | 96% | 7.29 | 62 / 0 / +7.9 |
| BP-OSD-0 (conv = BP alone) | 0.0130 ± 0.0011 | 0.984 | 97% | 7.29 | 34 / 0 / +5.8 |

### code 144, min-sum scaling 1.0, p = 0.04  (N = 10000)
| method | LER ± SE | converged | non-conv share of failures | iters | vs fixed: fixed / broken / z |
|---|---|---|---|---|---|
| flooding | 0.4307 ± 0.0050 | 0.569 | 100% | 23.71 | 442 / 1739 / -27.8 |
| fixed serial | 0.3010 ± 0.0046 | 0.699 | 100% | 18.96 |  |
| random serial | 0.3002 ± 0.0046 | 0.701 | 100% | 19.16 | 1058 / 1050 / +0.2 |
| fixed serial, tie-broken priors | 0.0191 ± 0.0014 | 0.984 | 86% | 6.70 | 2828 / 9 / +52.9 |
| static heuristic order | 0.1412 ± 0.0035 | 0.860 | 99% | 10.26 | 1841 / 243 / +35.0 |
| per-step heuristic, early stop | 0.1471 ± 0.0035 | 0.856 | 98% | 8.95 | 1859 / 320 / +33.0 |
| per-step heuristic, no early stop | 0.1555 ± 0.0036 | 0.845 | 99% | 10.52 | 1798 / 343 / +31.4 |
| RL-S shared Q (3b), trained on n=72, early stop | 0.1355 ± 0.0034 | 0.867 | 98% | 8.38 | 1928 / 273 / +35.3 |
| RL-S shared Q (3b), trained on n=72, no early stop | 0.1419 ± 0.0035 | 0.860 | 99% | 9.84 | 1879 / 288 / +34.2 |
| RL-S shared Q (3b), mixture-trained, no early stop | 0.1726 ± 0.0038 | 0.828 | 100% | 11.20 | 1703 / 419 / +27.9 |
| GNN order per syndrome (2b), trained on n=72 [score L2 1e-2] | 0.0533 ± 0.0022 | 0.948 | 98% | 5.81 | 2545 / 68 / +48.5 |
| ensemble of 24 random-order decoders (Maan et al. style) | 0.0249 ± 0.0016 | 0.977 | 93% | 462.26 | 2761 / 0 / +52.5 |
| BP-OSD-CS order 10 (conv = BP alone) | 0.2714 ± 0.0044 | 0.699 | 100% | 18.96 | 296 / 0 / +17.2 |
| BP-OSD-0 (conv = BP alone) | 0.2941 ± 0.0046 | 0.699 | 100% | 18.96 | 69 / 0 / +8.3 |

### code 144, min-sum scaling 1.0, p = 0.05  (N = 10000)
| method | LER ± SE | converged | non-conv share of failures | iters | vs fixed: fixed / broken / z |
|---|---|---|---|---|---|
| flooding | 0.6484 ± 0.0048 | 0.352 | 100% | 33.97 | 604 / 990 / -9.7 |
| fixed serial | 0.6098 ± 0.0049 | 0.390 | 100% | 31.49 |  |
| random serial | 0.5970 ± 0.0049 | 0.403 | 100% | 30.88 | 993 / 865 / +3.0 |
| fixed serial, tie-broken priors | 0.0647 ± 0.0025 | 0.942 | 90% | 11.10 | 5451 / 0 / +73.8 |
| static heuristic order | 0.4003 ± 0.0049 | 0.600 | 100% | 21.14 | 2224 / 129 / +43.2 |
| per-step heuristic, early stop | 0.3876 ± 0.0049 | 0.617 | 99% | 19.44 | 2411 / 189 / +43.6 |
| per-step heuristic, no early stop | 0.4088 ± 0.0049 | 0.591 | 100% | 21.35 | 2219 / 209 / +40.8 |
| RL-S shared Q (3b), trained on n=72, early stop | 0.3651 ± 0.0048 | 0.638 | 99% | 18.40 | 2575 / 128 / +47.1 |
| RL-S shared Q (3b), trained on n=72, no early stop | 0.3839 ± 0.0049 | 0.617 | 100% | 20.18 | 2406 / 147 / +44.7 |
| RL-S shared Q (3b), mixture-trained, no early stop | 0.4198 ± 0.0049 | 0.581 | 100% | 21.86 | 2132 / 232 / +39.1 |
| GNN order per syndrome (2b), trained on n=72 [score L2 1e-2] | 0.2682 ± 0.0044 | 0.732 | 100% | 14.54 | 3488 / 72 / +57.3 |
| ensemble of 24 random-order decoders (Maan et al. style) | 0.2939 ± 0.0046 | 0.707 | 100% | 755.45 | 3159 / 0 / +56.2 |
| BP-OSD-CS order 10 (conv = BP alone) | 0.5667 ± 0.0050 | 0.390 | 100% | 31.49 | 431 / 0 / +20.8 |
| BP-OSD-0 (conv = BP alone) | 0.6037 ± 0.0049 | 0.390 | 100% | 31.49 | 61 / 0 / +7.8 |