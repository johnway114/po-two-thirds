"""Seeded annealing over unrestricted positive integer matrices, minimizing exact F*.

python3 hunt2.py N M SEED ITERS INIT HI
  INIT: 'rand' (uniform 1..HI), 'heavy' (few large goods + medium + small tiers), or 'thm2:K' (needs N=4, M=9)
Every improvement is printed as a JSON line with the exact Fraction F* and the matrix.
"""
import json
import math
import random
import sys

from fractions import Fraction

from poefx import evaluate_dfs, thm2

THETA = Fraction(1, 2)


def init_matrix(rng, n, m, kind, hi):
    if kind.startswith("thm2:"):
        # Theorem 2 instance, padded with random extra goods (values 1..K) / extra agents (noisy copies)
        K = int(kind.split(":")[1])
        V = thm2(K)
        for row in V:
            row.extend(rng.randint(1, K) for _ in range(m - 9))
        while len(V) < n:
            base = rng.choice(V[:4])
            V.append([max(1, x + rng.randint(-2, 2)) for x in base])
        return [row[:m] for row in V[:n]]
    if kind == "heavy":
        tiers = [hi, hi // 3, hi // 10, 2]
        V = []
        for i in range(n):
            row = []
            for g in range(m):
                t = tiers[min(3, g * 4 // m)]
                row.append(max(1, int(t * rng.uniform(0.6, 1.0))))
            V.append(row)
        return V
    return [[rng.randint(1, hi) for _ in range(m)] for _ in range(n)]


def main():
    n, m, seed, iters, kind, hi = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], int(sys.argv[6])
    rng = random.Random(seed)
    V = init_matrix(rng, n, m, kind, hi)
    big = 10**6

    def F(W):
        r = evaluate_dfs(W, THETA)
        if r["status"] == 0:
            print(json.dumps({"WITNESS_BELOW_THETA": str(THETA), "V": W}), flush=True)
            return Fraction(0), r
        if r["status"] < 0:
            return big, r
        return (r["Fstar"] if r["Fstar"] is not None else big), r

    cur, info = F(V)
    best = cur
    print(json.dumps({"start": str(cur), "Ff": float(cur), "V": V}), flush=True)
    T = 0.03
    restarts = 0
    since = 0
    for it in range(iters):
        W = [r[:] for r in V]
        for _ in range(rng.choice([1, 1, 2, 3])):
            i, g = rng.randrange(n), rng.randrange(m)
            mode = rng.random()
            if mode < 0.6:
                step = max(1, int(W[i][g] * rng.choice([0.05, 0.15, 0.4])))
                W[i][g] = min(hi, max(1, W[i][g] + rng.choice([-1, 1]) * rng.randint(1, step)))
            elif mode < 0.8:  # copy a value across a column (create ties / shared structure)
                W[i][g] = W[rng.randrange(n)][g]
            else:  # swap two entries in a row
                h = rng.randrange(m)
                W[i][g], W[i][h] = W[i][h], W[i][g]
        s, inf = F(W)
        d = float(s - cur) if s != big and cur != big else (0 if s == cur else (1 if s == big else -1))
        if d <= 0 or rng.random() < math.exp(-d / T):
            V, cur, info = W, s, inf
            if s < best:
                best = s
                since = 0
                print(json.dumps({"it": it, "F": str(s), "Ff": float(s), "V": W, "argmax": inf["argmax_owner"]}), flush=True)
        since += 1
        T = max(0.002, T * 0.9995)
        if since > 3000:  # restart from scratch
            restarts += 1
            since = 0
            V = init_matrix(rng, n, m, kind, hi)
            cur, info = F(V)
            T = 0.03
    print(json.dumps({"final": str(best), "Ff": float(best), "restarts": restarts}), flush=True)


if __name__ == "__main__":
    main()
