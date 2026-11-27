"""RL-S (Moradi et al., arXiv 2603.10192): a Q-table picks the next qubit to update.
Reward = drop in unsatisfied checks / degree, +1 when solved.
per-qubit: state = which of 3 checks are unsatisfied, 8 x n table.
shared:    state = (#unsatisfied checks, current bit), 8 numbers."""
import numpy as np
from numba import njit
from rls.bp import init_state, update_vn

MODE_BITS = 0     # per-qubit
MODE_COUNT = 1    # shared


@njit(cache=True)
def vn_state(v, mode, e_row, col_ptr, col_edges, s, cand, dec):
    st = 0
    if mode == MODE_BITS:
        b = 0
        for k in range(col_ptr[v], col_ptr[v + 1]):
            c = e_row[col_edges[k]]
            if s[c] != cand[c]:
                st |= (1 << b)
            b += 1
    else:
        cnt = 0
        for k in range(col_ptr[v], col_ptr[v + 1]):
            c = e_row[col_edges[k]]
            if s[c] != cand[c]:
                cnt += 1
        st = cnt * 2 + dec[v]
    return st


@njit(cache=True)
def _best(remaining, n_rem, Q, slot, mode, e_row, col_ptr, col_edges, s, cand, dec):
    """Best remaining qubit (index into remaining) and its Q value."""
    best_j = 0
    best_q = -1e300
    for j in range(n_rem):
        v = remaining[j]
        q = Q[vn_state(v, mode, e_row, col_ptr, col_edges, s, cand, dec), slot[v]]
        if q > best_q:
            best_q = q
            best_j = j
    return best_j, best_q


@njit(cache=True)
def decode_policy(s, Q, slot, mode, llr0, alpha, max_iter,
                  e_row, e_col, col_ptr, col_edges, row_ptr, row_edges,
                  learn, lr, gamma, eps, early_stop, reward_mode, e_true, K):
    """One decode, Q-table picks every update; learn=True: epsilon-greedy Q-learning.
    early_stop: stop when solved instead of at the end of the sweep.
    reward_mode 0 = RL-S reward, 1 = +1/-1 logically correct/wrong (training only)."""
    n = len(llr0)
    E = len(e_row)
    m = len(s)
    b2c = np.empty(E); c2b = np.empty(E); lpr = llr0.copy()
    dec = np.zeros(n, np.uint8); cand = np.zeros(m, np.uint8)
    init_state(llr0, e_col, b2c, c2b, dec, cand)

    w = 0
    for c in range(m):
        w += s[c]
    if w == 0:
        return dec, True, 0

    remaining = np.empty(n, np.int64)
    steps = 0
    for it in range(max_iter):
        for v in range(n):
            remaining[v] = v
        n_rem = n
        while n_rem > 0:
            j, _ = _best(remaining, n_rem, Q, slot, mode, e_row, col_ptr, col_edges, s, cand, dec)
            if learn and np.random.random() < eps:
                j = np.random.randint(n_rem)
            v = remaining[j]
            st = vn_state(v, mode, e_row, col_ptr, col_edges, s, cand, dec)

            flipped = update_vn(v, s, llr0, alpha, e_row, col_ptr, col_edges,
                                row_ptr, row_edges, b2c, c2b, lpr, dec, cand)
            steps += 1
            remaining[j] = remaining[n_rem - 1]
            n_rem -= 1

            w_new = w
            if flipped:
                w_new = 0
                for c in range(m):
                    if s[c] != cand[c]:
                        w_new += 1
            done = (w_new == 0)
            terminal = done and (early_stop or n_rem == 0)

            last = (it == max_iter - 1) and (n_rem == 0)
            if learn:
                if reward_mode == 0:
                    deg = col_ptr[v + 1] - col_ptr[v]
                    r = (w - w_new) / deg
                    if terminal:
                        r += 1.0
                else:
                    r = 0.0
                    if terminal or last:
                        ok = terminal
                        if ok:
                            for a_ in range(K.shape[0]):
                                acc = 0
                                for i_ in range(n):
                                    acc ^= K[a_, i_] & (e_true[i_] ^ dec[i_])
                                if acc:
                                    ok = False
                                    break
                        r = 1.0 if ok else -1.0
                        terminal = True
                future = 0.0
                if not terminal and n_rem > 0:
                    _, future = _best(remaining, n_rem, Q, slot, mode, e_row, col_ptr,
                                      col_edges, s, cand, dec)
                Q[st, slot[v]] += lr * (r + gamma * future - Q[st, slot[v]])

            w = w_new
            if done and early_stop:
                return dec, True, steps
        if w == 0:
            return dec, True, steps
    return dec, False, steps


@njit(cache=True)
def train(Q, slot, mode, H_err, ps, n_episodes, alpha, max_iter,
          e_row, e_col, col_ptr, col_edges, row_ptr, row_edges,
          lr, gamma, eps0, eps_min, seed, early_stop, reward_mode, K):
    """Q-learning on random errors, epsilon decays linearly."""
    np.random.seed(seed)
    m, n = H_err.shape
    s = np.zeros(m, np.uint8)
    e = np.zeros(n, np.uint8)
    llr0 = np.empty(n)
    n_conv = 0
    for ep in range(n_episodes):
        p = ps[np.random.randint(len(ps))]
        for i in range(n):
            e[i] = 1 if np.random.random() < p else 0
            llr0[i] = np.log((1 - p) / p)
        for c in range(m):
            acc = 0
            for i in range(n):
                acc ^= H_err[c, i] & e[i]
            s[c] = acc
        eps = eps0 + (eps_min - eps0) * ep / max(1, n_episodes - 1)
        _, conv, _ = decode_policy(s, Q, slot, mode, llr0, alpha, max_iter,
                                   e_row, e_col, col_ptr, col_edges, row_ptr, row_edges,
                                   True, lr, gamma, eps, early_stop, reward_mode, e, K)
        n_conv += conv
    return n_conv / n_episodes


class PolicyDecoder:
    """Trained Q-table with an ldpc-like decode(s)."""

    def __init__(self, H, error_rate, Q, slot, mode, max_iter=50, ms_scaling_factor=1.0, early_stop=True):
        self.early_stop = early_stop
        from rls.bp import build_graph
        self.g = build_graph(H)
        self.n = self.g["n"]
        self.llr0 = np.full(self.n, np.log((1 - error_rate) / error_rate))
        self.Q, self.slot, self.mode = Q, np.asarray(slot, np.int64), mode
        self.alpha, self.max_iter = float(ms_scaling_factor), max_iter

    def decode(self, s):
        g = self.g
        dec, self.converge, self.steps = decode_policy(
            np.asarray(s, np.uint8), self.Q, self.slot, self.mode, self.llr0, self.alpha,
            self.max_iter, g["e_row"], g["e_col"], g["col_ptr"], g["col_edges"],
            g["row_ptr"], g["row_edges"], False, 0.0, 0.0, 0.0, self.early_stop,
            0, np.zeros(self.n, np.uint8), np.zeros((1, self.n), np.uint8))
        self.iter = self.steps / self.n
        return dec
