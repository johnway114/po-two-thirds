"""Two-scale ("chamber") annealing: V = K*A + B with coarse A in {0..AMAX}, fine B in {0..BMAX}, V > 0.

The coarse layer explores degenerate (zero-allowed) incidence structures; the fine layer is the
positive tie-breaking that the positivity hypothesis forces.  Theorem 2 is A = its K-coefficients,
B = its constants.  Objective: exact F* from the DFS evaluator (theta = 1/2).

python3 hunt3.py N M SEED ITERS K AMAX BMAX [start=thm2|rand]
"""
import json
import math
import random
import sys
from fractions import Fraction

from poefx import evaluate_dfs

THETA = Fraction(1, 2)
BIG = Fraction(10**6)

THM2_A = [
    [3, 2, 1, 1, 0, 0, 1, 0, 0],
    [2, 3, 0, 1, 1, 0, 1, 0, 0],
    [3, 2, 0, 0, 1, 1, 1, 0, 0],
    [2, 3, 1, 0, 0, 1, 1, 0, 0],
]
THM2_B = [
    [0, 2, 0, 0, 1, 1, 0, 2, 1],
    [2, 0, 1, 0, 0, 1, 0, 1, 2],
    [0, 2, 1, 1, 0, 0, 0, 2, 1],
    [2, 0, 0, 1, 1, 0, 0, 1, 2],
]


def build(A, B, K):
    return [[K * a + b for a, b in zip(ra, rb)] for ra, rb in zip(A, B)]


def F(A, B, K):
    V = build(A, B, K)
    r = evaluate_dfs(V, THETA)
    if r["status"] == 0:
        return Fraction(0), r, V
    if r["status"] < 0 or r["Fstar"] is None:
        return BIG, r, V
    return r["Fstar"], r, V


def main():
    n, m, seed, iters, K, amax, bmax = map(int, sys.argv[1:8])
    start = sys.argv[8] if len(sys.argv) > 8 else "thm2"
    rng = random.Random(seed)

    def fresh():
        if start == "thm2":
            A = [r[:] + [rng.randint(0, 1) for _ in range(m - 9)] for r in THM2_A]
            B = [r[:] + [rng.randint(1, bmax) for _ in range(m - 9)] for r in THM2_B]
            while len(A) < n:
                A.append([rng.randint(0, amax) for _ in range(m)])
                B.append([rng.randint(1, bmax) for _ in range(m)])
            return [r[:m] for r in A[:n]], [r[:m] for r in B[:n]]
        A = [[rng.randint(0, amax) for _ in range(m)] for _ in range(n)]
        B = [[rng.randint(1, bmax) for _ in range(m)] for _ in range(n)]
        return A, B

    A, B = fresh()
    cur, info, V = F(A, B, K)
    best = cur
    print(json.dumps({"start": str(cur), "Ff": float(cur), "A": A, "B": B}), flush=True)
    T, since = 0.02, 0
    for it in range(iters):
        A2, B2 = [r[:] for r in A], [r[:] for r in B]
        for _ in range(rng.choice([1, 1, 2])):
            i, g = rng.randrange(n), rng.randrange(m)
            u = rng.random()
            if u < 0.45:
                A2[i][g] = min(amax, max(0, A2[i][g] + rng.choice([-1, 1])))
            elif u < 0.85:
                B2[i][g] = min(bmax, max(0, B2[i][g] + rng.choice([-1, 1])))
            else:  # swap two goods' columns for one agent (re-wire incidence)
                h = rng.randrange(m)
                A2[i][g], A2[i][h] = A2[i][h], A2[i][g]
                B2[i][g], B2[i][h] = B2[i][h], B2[i][g]
            if A2[i][g] == 0 and B2[i][g] == 0:
                B2[i][g] = 1
        s, inf, V2 = F(A2, B2, K)
        if s == 0:
            print(json.dumps({"WITNESS_BELOW_THETA": str(THETA), "V": V2, "A": A2, "B": B2}), flush=True)
        d = float(s - cur) if BIG not in (s, cur) else (0.0 if s == cur else (1.0 if s == BIG else -1.0))
        if d <= 0 or rng.random() < math.exp(-d / T):
            A, B, cur = A2, B2, s
            if s < best:
                best, since = s, 0
                print(json.dumps({"it": it, "F": str(s), "Ff": float(s), "A": A, "B": B, "argmax": inf["argmax_owner"]}), flush=True)
        since += 1
        T = max(0.001, T * 0.9995)
        if since > 4000:
            since, T = 0, 0.02
            A, B = fresh()
            cur, info, V = F(A, B, K)
    print(json.dumps({"final": str(best), "Ff": float(best)}), flush=True)


if __name__ == "__main__":
    main()
