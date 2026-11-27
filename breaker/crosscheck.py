"""Cross-check the DFS evaluator against the brute-force frontier evaluator on seeded random instances."""
import random
import sys
from fractions import Fraction

from poefx import evaluate, evaluate_dfs

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
bad = 0
tot = 0
for trial in range(int(sys.argv[2]) if len(sys.argv) > 2 else 300):
    n = rng.choice([2, 3, 4])
    m = rng.randint(n + 1, {2: 12, 3: 10, 4: 8}[n])
    hi = rng.choice([3, 10, 100])
    V = [[rng.randint(1, hi) for _ in range(m)] for _ in range(n)]
    if rng.random() < 0.3:  # add structure: a big good
        for i in range(n):
            V[i][0] = hi * rng.randint(2, 5)
    a = evaluate(V)["Fstar"]
    th = Fraction(1, 2)
    b = evaluate_dfs(V, th)
    tot += 1
    if a is None:
        ok = b["status"] == 1 and b["Fstar"] is None
    elif a >= th:
        ok = b["status"] == 1 and b["Fstar"] == a
    else:
        ok = b["status"] == 0
    if not ok:
        bad += 1
        print("MISMATCH", V, a, b)
print("trials", tot, "mismatches", bad)
