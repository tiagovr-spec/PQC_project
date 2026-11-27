"""GNN on the Tanner graph: syndrome -> score per qubit -> order for ldpc.
Same weights for every node, so it runs on any BB code."""
import torch
import torch.nn as nn


def mlp(i, o):
    return nn.Sequential(nn.Linear(i, o), nn.ReLU(), nn.Linear(o, o))


class TannerGNN(nn.Module):
    def __init__(self, d=32, rounds=4):
        super().__init__()
        self.q0 = nn.Linear(2, d)
        self.c0 = nn.Embedding(2, d)
        self.c_upd = nn.ModuleList([mlp(2 * d, d) for _ in range(rounds)])
        self.q_upd = nn.ModuleList([mlp(2 * d, d) for _ in range(rounds)])
        self.out = nn.Linear(d, 1)

    def forward(self, S, H, block):
        """S (B, m), H (m, n), block (n, 2) -> scores (B, n)"""
        B = S.shape[0]
        degc = H.sum(1).clamp(min=1)[None, :, None]
        degq = H.sum(0).clamp(min=1)[None, :, None]
        hq = self.q0(block).unsqueeze(0).expand(B, -1, -1)
        hc = self.c0(S)
        for cu, qu in zip(self.c_upd, self.q_upd):
            aq = torch.einsum("mn,bnd->bmd", H, hq) / degc
            hc = hc + cu(torch.cat([hc, aq], -1))
            ac = torch.einsum("mn,bmd->bnd", H, hc) / degq
            hq = hq + qu(torch.cat([hq, ac], -1))
        return self.out(hq).squeeze(-1)


def sample_orders(scores, K):
    """K random orders per syndrome (Gumbel noise + sort)."""
    u = torch.rand(scores.shape[0], K, scores.shape[1]).clamp(1e-10, 1 - 1e-10)
    g = -torch.log(-torch.log(u))
    return torch.argsort(-(scores.unsqueeze(1) + g), dim=-1)


def pl_logprob(scores, orders):
    """log P(order | scores), Plackett-Luce."""
    s = torch.gather(scores.unsqueeze(1).expand_as(orders), 2, orders)
    lse = torch.flip(torch.logcumsumexp(torch.flip(s, [2]), 2), [2])
    return (s - lse).sum(-1)


def greedy_orders(scores):
    """Highest score first."""
    return torch.argsort(-scores, dim=-1, stable=True)


def block_onehot(n):
    b = torch.zeros(n, 2)
    b[: n // 2, 0] = 1
    b[n // 2:, 1] = 1
    return b
