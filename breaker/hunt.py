"""Seeded local-search hunt for positive additive instances with small PO alpha-EFX optimum F*.

Usage: python3 hunt.py MODE SEED ITERS [extra]
Modes:
  sym9   : D4-symmetric 9-good family generalizing Theorem 2 (parameters annealed)
  sym10  : sym9 plus a tenth good z with D4-invariant values (common to all agents)
  free   : unrestricted n x m integer matrix, started from Theorem 2 (K given) and perturbed
Writes improving records (exact Fractions) to stdout as JSON lines.
"""
import json
import math
import random
import sys
from fractions import Fraction

from poefx import evaluate, thm2

# D4 family: agents 1..4 at square corners in cyclic order.  Sides: a=(1,4)?  Follow paper:
# a: agents 1,4 high; b: 1,2; c: 2,3; d: 3,4; x,p: diagonal {1,3}; y,q: diagonal {2,4}.
SIDES = {"a": (0, 3), "b": (0, 1), "c": (1, 2), "d": (2, 3)}
DIAG = {0: (0, 2), 1: (1, 3)}


def sym_matrix(P, with_z=False):
    """P keys: X1,X2 (large: incident/non-incident), M1,M2 (side goods), E (common), S1,S2 (small), Z (optional)."""
    rows = []
    for i in range(4):
        r = []
        for diag, lo in ((0, None), (1, None)):  # x then y
            r.append(P["X1"] if i in DIAG[diag] else P["X2"])
        for s in "abcd":
            r.append(P["M1"] if i in SIDES[s] else P["M2"])
        r.append(P["E"])
        for diag in (0, 1):  # p then q
            r.append(P["S1"] if i in DIAG[diag] else P["S2"])
        if with_z:
            r.append(P["Z"])
        rows.append(r)
    return rows


def score(V):
    r = evaluate(V)
    F = r["Fstar"] if r["Fstar"] is not None else Fraction(10**9)
    return F, r


def anneal_params(P0, keys, seed, iters, with_z, lo=1, hi=400):
    rng = random.Random(seed)
    P = dict(P0)
    cur, info = score(sym_matrix(P, with_z))
    best = (cur, dict(P))
    T = 0.02
    for it in range(iters):
        Q = dict(P)
        k = rng.choice(keys)
        step = max(1, int(abs(Q[k]) * rng.choice([0.02, 0.05, 0.1, 0.25])))
        Q[k] = min(hi, max(lo, Q[k] + rng.choice([-1, 1]) * rng.randint(1, step)))
        if rng.random() < 0.15:  # rescale move
            f = rng.choice([1.1, 0.9])
            Q = {kk: max(lo, min(hi, int(round(vv * f)))) for kk, vv in Q.items()}
        s, inf = score(sym_matrix(Q, with_z))
        if s <= cur or rng.random() < math.exp(-float(s - cur) / T):
            P, cur, info = Q, s, inf
            if s < best[0]:
                best = (s, dict(Q))
                print(json.dumps({"it": it, "F": str(s), "Ff": float(s), "P": Q, "argmax": inf["argmax_owner"], "po": inf["po_count"]}), flush=True)
        T *= 0.999
    return best


def anneal_free(V0, seed, iters, lo=1, hi=400):
    rng = random.Random(seed)
    V = [row[:] for row in V0]
    n, m = len(V), len(V[0])
    cur, info = score(V)
    best = (cur, [r[:] for r in V])
    print(json.dumps({"start": str(cur), "Ff": float(cur)}), flush=True)
    T = 0.01
    for it in range(iters):
        W = [r[:] for r in V]
        for _ in range(rng.choice([1, 1, 1, 2, 3])):
            i, g = rng.randrange(n), rng.randrange(m)
            step = max(1, int(W[i][g] * rng.choice([0.02, 0.05, 0.15, 0.4])))
            W[i][g] = min(hi, max(lo, W[i][g] + rng.choice([-1, 1]) * rng.randint(1, step)))
        s, inf = score(W)
        if s < cur or (s == cur and rng.random() < 0.5) or rng.random() < math.exp(-float(s - cur) / T):
            V, cur, info = W, s, inf
            if s < best[0]:
                best = (s, [r[:] for r in W])
                print(json.dumps({"it": it, "F": str(s), "Ff": float(s), "V": W, "argmax": inf["argmax_owner"]}), flush=True)
        T *= 0.999
    return best


if __name__ == "__main__":
    mode, seed, iters = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    if mode in ("sym9", "sym10"):
        K = 30
        P0 = {"X1": 3 * K, "X2": 2 * K + 2, "M1": K, "M2": 1, "E": K, "S1": 2, "S2": 1}
        keys = list(P0)
        if mode == "sym10":
            P0["Z"] = int(sys.argv[4]) if len(sys.argv) > 4 else K
            keys.append("Z")
        best = anneal_params(P0, keys, seed, iters, mode == "sym10")
    else:
        K = int(sys.argv[4]) if len(sys.argv) > 4 else 30
        best = anneal_free(thm2(K), seed, iters)
    print(json.dumps({"final": str(best[0]), "Ff": float(best[0]), "best": best[1]}), flush=True)
