import numpy as np
from ldpc import mod2


def shift_matrix(l):
    # l x l identity with columns shifted by one (cyclic)
    return np.roll(np.eye(l, dtype=int), 1, axis=1)


def bb_code(l=6, m=6):
    # [[72,12,6]] bivariate bicycle code: A = x^3 + y + y^2, B = y^3 + x + x^2
    S_l, S_m = shift_matrix(l), shift_matrix(m)
    x = np.kron(S_l, np.eye(m, dtype=int))
    y = np.kron(np.eye(l, dtype=int), S_m)
    A = np.linalg.matrix_power(x, 3) + y + np.linalg.matrix_power(y, 2)
    B = np.linalg.matrix_power(y, 3) + x + np.linalg.matrix_power(x, 2)
    H_X = np.hstack([A, B]) % 2
    H_Z = np.hstack([B.T, A.T]) % 2
    return H_X, H_Z


def bb_code_poly(l, m, A_terms, B_terms):
    # General BB code. Each term (i, j) is the monomial x^i y^j.
    S_l, S_m = shift_matrix(l), shift_matrix(m)
    x = np.kron(S_l, np.eye(m, dtype=int))
    y = np.kron(np.eye(l, dtype=int), S_m)
    mono = lambda i, j: np.linalg.matrix_power(x, i) @ np.linalg.matrix_power(y, j)
    A = sum(mono(i, j) for i, j in A_terms) % 2
    B = sum(mono(i, j) for i, j in B_terms) % 2
    return np.hstack([A, B]) % 2, np.hstack([B.T, A.T]) % 2


# Bravyi et al., Nature 627 (2024)
BB_CODES = {
    "72":  dict(l=6,  m=6, A_terms=[(3, 0), (0, 1), (0, 2)], B_terms=[(0, 3), (1, 0), (2, 0)]),  # [[72,12,6]]
    "90":  dict(l=15, m=3, A_terms=[(9, 0), (0, 1), (0, 2)], B_terms=[(0, 0), (2, 0), (7, 0)]),  # [[90,8,10]]
    "144": dict(l=12, m=6, A_terms=[(3, 0), (0, 1), (0, 2)], B_terms=[(0, 3), (1, 0), (2, 0)]),  # [[144,12,12]]
}


def is_failure(H_X, rank_HX, e, e_hat, converged):
    # Fail if BP did not converge, or if the residual e + e_hat is not a stabilizer
    if not converged:
        return True
    r = (e + e_hat) % 2
    if not r.any():
        return False
    return mod2.rank(np.vstack([H_X, r])) > rank_HX
