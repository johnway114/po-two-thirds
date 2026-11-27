"""Grid over the square family: side goods K/1, common good E, large X1 (lovers)/X2, smalls S1/S2.
Prints the minimum F* found per E (exact)."""
import sys
from fractions import Fraction
from families import square
from poefx import evaluate_dfs
K = int(sys.argv[1]) if len(sys.argv) > 1 else 20
best_overall = None
for E in range(K // 2, 4 * K + 1, max(1, K // 10)):
    best = None
    for X1 in range(2 * K, 2 * K + E + 2 * K, max(1, K // 10)):
        for X2 in range(K, X1 + 1, max(1, K // 10)):
            for (S1, S2) in [(2, 1), (1, 1), (3, 1)]:
                V = square(K, X1, X2, commons=(E,), S1=S1, S2=S2)
                r = evaluate_dfs(V, Fraction(1, 2))
                F = Fraction(0) if r["status"] == 0 else r["Fstar"]
                if r["status"] < 0 or F is None:
                    continue
                if best is None or F < best[0]:
                    best = (F, X1, X2, S1, S2)
    print("E", E, "best", best[0], float(best[0]), best[1:], flush=True)
    if best_overall is None or best[0] < best_overall[0]:
        best_overall = (best[0], E) + best[1:]
print("overall", best_overall, float(best_overall[0]))
