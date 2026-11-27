"""Check that our serial BP gives the same output as ldpc (same shots, same orders).
Run: python -m rls.validate_bp
"""
import numpy as np
from ldpc import BpDecoder, mod2
from bb_code import bb_code, is_failure
from rls.bp import SerialBP

H_X, H_Z = bb_code()
n = H_Z.shape[1]
rank_HX = mod2.rank(H_X)

for p in (0.03, 0.04):
    rng = np.random.default_rng(7)
    N = 1000
    E = (rng.random((N, n)) < p).astype(np.uint8)
    S = ((E @ H_Z.T) % 2).astype(np.uint8)
    ours = SerialBP(H_Z, error_rate=p, max_iter=50)

    orders = {"fixed 0..71": np.arange(n)}
    perm_rng = np.random.default_rng(99)
    for k in range(3):
        orders[f"random #{k}"] = perm_rng.permutation(n)

    for name, order in orders.items():
        ref = BpDecoder(H_Z, error_rate=p, max_iter=50, bp_method="minimum_sum",
                        schedule="serial", serial_schedule_order=order.tolist())
        same_dec = same_conv = same_iter = 0
        f_ref = f_ours = 0
        for i in range(N):
            d_ref = ref.decode(S[i]); c_ref, it_ref = ref.converge, ref.iter
            d_our = ours.decode(S[i], order); c_our, it_our = ours.converge, ours.iter
            same_dec += np.array_equal(d_ref, d_our)
            same_conv += (c_ref == c_our)
            same_iter += (it_ref == it_our) or not c_ref
            f_ref += is_failure(H_X, rank_HX, E[i], d_ref, c_ref)
            f_ours += is_failure(H_X, rank_HX, E[i], d_our, c_our)
        print(f"p={p} {name:12s} same correction {same_dec}/{N}  same converged {same_conv}/{N}"
              f"  same iters {same_iter}/{N}  LER ldpc {f_ref/N:.4f}  ours {f_ours/N:.4f}")
