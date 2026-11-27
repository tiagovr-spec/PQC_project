"""Number of conflict-free parallel layers of a serial sweep (qubits sharing no check commute)."""
import numpy as np
from bb_code import bb_code_poly, BB_CODES

rng = np.random.default_rng(0)


def n_layers(C, order):
    # layer of a qubit = 1 + latest layer of an earlier qubit it shares a check with
    n = len(order)
    pos = np.empty(n, int); pos[order] = np.arange(n)
    layer = np.zeros(n, int)
    for v in order:
        earlier = [u for u in np.nonzero(C[v])[0] if pos[u] < pos[v]]
        layer[v] = 1 + max((layer[u] for u in earlier), default=0)
    return layer.max()


def greedy_colouring(C, order):
    col = -np.ones(len(order), int)
    for v in order:
        used = set(col[np.nonzero(C[v])[0]])
        c = 0
        while c in used:
            c += 1
        col[v] = c
    return col.max() + 1


for code in ["72", "90", "144"]:
    _, H = bb_code_poly(**BB_CODES[code])
    H = H.astype(int)
    n = H.shape[1]
    C = (H.T @ H) > 0
    np.fill_diagonal(C, False)
    rand = [n_layers(C, rng.permutation(n)) for _ in range(200)]
    col = min(greedy_colouring(C, rng.permutation(n)) for _ in range(300))
    print(f"[[{code}]] {n} qubits: fixed order {n_layers(C, np.arange(n))} layers, "
          f"random order {np.mean(rand):.1f} on average, greedy colouring {col} layers "
          f"(lower bound = check weight {H.sum(1).max()}); flooding = 1 layer")
