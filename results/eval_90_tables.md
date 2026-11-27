
### code 90, min-sum scaling 1.0, p = 0.03  (N = 10000)
| method | LER ± SE | converged | non-conv share of failures | iters | vs fixed: fixed / broken / z |
|---|---|---|---|---|---|
| flooding | 0.2083 ± 0.0041 | 0.792 | 100% | 12.35 | 83 / 1722 / -38.6 |
| fixed serial | 0.0444 ± 0.0021 | 0.956 | 98% | 8.11 |  |
| random serial | 0.0514 ± 0.0022 | 0.950 | 98% | 8.27 | 290 / 360 / -2.7 |
| fixed serial, tie-broken priors | 0.0088 ± 0.0009 | 0.993 | 84% | 3.79 | 366 / 10 / +18.4 |
| static heuristic order | 0.0240 ± 0.0015 | 0.977 | 98% | 4.35 | 324 / 120 / +9.7 |
| per-step heuristic, early stop | 0.0231 ± 0.0015 | 0.984 | 69% | 2.91 | 345 / 132 / +9.8 |
| per-step heuristic, no early stop | 0.0219 ± 0.0015 | 0.979 | 95% | 4.32 | 339 / 114 / +10.6 |
| RL-S shared Q (3b), trained on n=72, early stop | 0.0320 ± 0.0018 | 0.973 | 84% | 3.15 | 327 / 203 / +5.4 |
| RL-S shared Q (3b), trained on n=72, no early stop | 0.0341 ± 0.0018 | 0.967 | 96% | 4.53 | 315 / 212 / +4.5 |
| RL-S shared Q (3b), mixture-trained, no early stop | 0.0352 ± 0.0018 | 0.966 | 96% | 4.65 | 310 / 218 / +4.0 |
| GNN order per syndrome (2b), trained on n=72 [score L2 1e-2] | 0.0127 ± 0.0011 | 0.988 | 95% | 2.62 | 348 / 31 / +16.3 |
| ensemble of 24 random-order decoders (Maan et al. style) | 0.0043 ± 0.0007 | 0.998 | 53% | 191.53 | 401 / 0 / +20.0 |
| BP-OSD-CS order 10 (conv = BP alone) | 0.0236 ± 0.0015 | 0.956 | 97% | 8.11 | 208 / 0 / +14.4 |
| BP-OSD-0 (conv = BP alone) | 0.0354 ± 0.0018 | 0.956 | 98% | 8.11 | 90 / 0 / +9.5 |

### code 90, min-sum scaling 1.0, p = 0.04  (N = 10000)
| method | LER ± SE | converged | non-conv share of failures | iters | vs fixed: fixed / broken / z |
|---|---|---|---|---|---|
| flooding | 0.3803 ± 0.0049 | 0.620 | 100% | 20.87 | 387 / 1274 / -21.8 |
| fixed serial | 0.2916 ± 0.0045 | 0.709 | 100% | 17.37 |  |
| random serial | 0.2860 ± 0.0045 | 0.715 | 100% | 17.06 | 895 / 839 / +1.3 |
| fixed serial, tie-broken priors | 0.0340 ± 0.0018 | 0.970 | 88% | 6.83 | 2588 / 12 / +50.5 |
| static heuristic order | 0.1578 ± 0.0036 | 0.843 | 99% | 10.13 | 1517 / 179 / +32.5 |
| per-step heuristic, early stop | 0.1502 ± 0.0036 | 0.879 | 81% | 7.78 | 1614 / 200 / +33.2 |
| per-step heuristic, no early stop | 0.1594 ± 0.0037 | 0.842 | 99% | 10.06 | 1536 / 214 / +31.6 |
| RL-S shared Q (3b), trained on n=72, early stop | 0.1470 ± 0.0035 | 0.869 | 89% | 8.06 | 1622 / 176 / +34.1 |
| RL-S shared Q (3b), trained on n=72, no early stop | 0.1575 ± 0.0036 | 0.844 | 99% | 10.03 | 1530 / 189 / +32.3 |
| RL-S shared Q (3b), mixture-trained, no early stop | 0.1717 ± 0.0038 | 0.829 | 99% | 10.54 | 1440 / 241 / +29.2 |
| GNN order per syndrome (2b), trained on n=72 [score L2 1e-2] | 0.0795 ± 0.0027 | 0.922 | 98% | 6.17 | 2185 / 64 / +44.7 |
| ensemble of 24 random-order decoders (Maan et al. style) | 0.0476 ± 0.0021 | 0.956 | 92% | 415.05 | 2440 / 0 / +49.4 |
| BP-OSD-CS order 10 (conv = BP alone) | 0.2227 ± 0.0042 | 0.709 | 100% | 17.37 | 689 / 0 / +26.2 |
| BP-OSD-0 (conv = BP alone) | 0.2768 ± 0.0045 | 0.709 | 100% | 17.37 | 148 / 0 / +12.2 |

### code 90, min-sum scaling 1.0, p = 0.05  (N = 10000)
| method | LER ± SE | converged | non-conv share of failures | iters | vs fixed: fixed / broken / z |
|---|---|---|---|---|---|
| flooding | 0.5645 ± 0.0050 | 0.435 | 100% | 29.71 | 537 / 1042 / -12.7 |
| fixed serial | 0.5140 ± 0.0050 | 0.486 | 100% | 26.70 |  |
| random serial | 0.5056 ± 0.0050 | 0.495 | 100% | 26.30 | 932 / 848 / +2.0 |
| fixed serial, tie-broken priors | 0.0809 ± 0.0027 | 0.929 | 88% | 10.78 | 4332 / 1 / +65.8 |
| static heuristic order | 0.3351 ± 0.0047 | 0.665 | 100% | 17.71 | 1913 / 124 / +39.6 |
| per-step heuristic, early stop | 0.3204 ± 0.0047 | 0.736 | 83% | 14.55 | 2099 / 163 / +40.7 |
| per-step heuristic, no early stop | 0.3383 ± 0.0047 | 0.663 | 100% | 17.74 | 1932 / 175 / +38.3 |
| RL-S shared Q (3b), trained on n=72, early stop | 0.3158 ± 0.0046 | 0.717 | 90% | 14.95 | 2156 / 174 / +41.1 |
| RL-S shared Q (3b), trained on n=72, no early stop | 0.3345 ± 0.0047 | 0.667 | 99% | 17.57 | 1982 / 187 / +38.5 |
| RL-S shared Q (3b), mixture-trained, no early stop | 0.3463 ± 0.0048 | 0.655 | 100% | 18.12 | 1873 / 196 / +36.9 |
| GNN order per syndrome (2b), trained on n=72 [score L2 1e-2] | 0.2335 ± 0.0042 | 0.767 | 100% | 12.64 | 2874 / 69 / +51.7 |
| ensemble of 24 random-order decoders (Maan et al. style) | 0.2234 ± 0.0042 | 0.778 | 100% | 640.66 | 2906 / 0 / +53.9 |
| BP-OSD-CS order 10 (conv = BP alone) | 0.4136 ± 0.0049 | 0.486 | 100% | 26.70 | 1004 / 0 / +31.7 |
| BP-OSD-0 (conv = BP alone) | 0.4964 ± 0.0050 | 0.486 | 100% | 26.70 | 176 / 0 / +13.3 |