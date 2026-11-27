"""Serial min-sum BP, one qubit at a time (ldpc has no single-qubit update; needed for RL-S).
Bit-identical to ldpc (validate_bp.py). b2c = qubit->check, c2b = check->qubit messages."""
import numpy as np
from numba import njit


def build_graph(H):
    """Tanner graph edges, grouped by qubit and by check."""
    H = np.asarray(H, dtype=np.uint8)
    m, n = H.shape
    cols, rows = np.nonzero(H.T)            # edges sorted by qubit
    e_row, e_col = rows.astype(np.int64), cols.astype(np.int64)
    E = len(e_row)
    col_ptr = np.zeros(n + 1, np.int64)
    np.add.at(col_ptr, e_col + 1, 1)
    col_ptr = np.cumsum(col_ptr)
    col_edges = np.arange(E, dtype=np.int64)
    order = np.argsort(e_row, kind="stable")
    row_ptr = np.zeros(m + 1, np.int64)
    np.add.at(row_ptr, e_row + 1, 1)
    row_ptr = np.cumsum(row_ptr)
    row_edges = order.astype(np.int64)
    return dict(n=n, m=m, e_row=e_row, e_col=e_col, col_ptr=col_ptr,
                col_edges=col_edges, row_ptr=row_ptr, row_edges=row_edges)


@njit(cache=True)
def init_state(llr0, e_col, b2c, c2b, dec, cand):
    """Messages = prior LLR, guess = no error."""
    for e in range(len(e_col)):
        b2c[e] = llr0[e_col[e]]
        c2b[e] = 0.0
    dec[:] = 0
    cand[:] = 0   # syndrome of current guess


@njit(cache=True)
def update_vn(i, s, llr0, alpha, e_row, col_ptr, col_edges, row_ptr, row_edges,
              b2c, c2b, lpr, dec, cand):
    """Update qubit i. Returns True if its bit flipped."""
    # Same float addition order as ldpc: at alpha = 1 many sums are exactly 0.
    lpr[i] = llr0[i]
    for k in range(col_ptr[i], col_ptr[i + 1]):
        e = col_edges[k]
        c = e_row[e]
        sgn = s[c]
        mn = 1e300
        for kk in range(row_ptr[c], row_ptr[c + 1]):
            g = row_edges[kk]
            if g != e:
                a = abs(b2c[g])
                if a < mn:
                    mn = a
                if b2c[g] <= 0:
                    sgn ^= 1
        c2b[e] = -alpha * mn if sgn else alpha * mn
        b2c[e] = lpr[i]
        lpr[i] += c2b[e]
    temp = 0.0
    for k in range(col_ptr[i + 1] - 1, col_ptr[i] - 1, -1):
        e = col_edges[k]
        b2c[e] += temp
        temp += c2b[e]
    new = 1 if lpr[i] <= 0 else 0
    if new != dec[i]:
        dec[i] = new
        for k in range(col_ptr[i], col_ptr[i + 1]):
            cand[e_row[col_edges[k]]] ^= 1
        return True
    return False


@njit(cache=True)
def syndrome_ok(s, cand):
    for c in range(len(s)):
        if s[c] != cand[c]:
            return False
    return True


@njit(cache=True)
def decode_order(s, order, llr0, alpha, max_iter, e_row, e_col, col_ptr, col_edges,
                 row_ptr, row_edges):
    """Serial BP with a fixed order (convergence checked after each sweep, as ldpc)."""
    n = len(llr0)
    E = len(e_row)
    b2c = np.empty(E); c2b = np.empty(E); lpr = llr0.copy()
    dec = np.zeros(n, np.uint8); cand = np.zeros(len(s), np.uint8)
    init_state(llr0, e_col, b2c, c2b, dec, cand)
    if syndrome_ok(s, cand):
        return dec, True, 0
    for it in range(1, max_iter + 1):
        for i in order:
            update_vn(i, s, llr0, alpha, e_row, col_ptr, col_edges, row_ptr,
                      row_edges, b2c, c2b, lpr, dec, cand)
        if syndrome_ok(s, cand):
            return dec, True, it
    return dec, False, max_iter


class SerialBP:
    """decode(s, order), like ldpc."""

    def __init__(self, H, error_rate, max_iter=50, ms_scaling_factor=1.0):
        self.g = build_graph(H)
        self.n = self.g["n"]
        self.llr0 = np.full(self.n, np.log((1 - error_rate) / error_rate))
        self.alpha = float(ms_scaling_factor)
        self.max_iter = max_iter

    def decode(self, s, order=None):
        g = self.g
        if order is None:
            order = np.arange(self.n)
        dec, self.converge, self.iter = decode_order(
            np.asarray(s, np.uint8), np.asarray(order, np.int64), self.llr0, self.alpha,
            self.max_iter, g["e_row"], g["e_col"], g["col_ptr"], g["col_edges"],
            g["row_ptr"], g["row_edges"])
        return dec
