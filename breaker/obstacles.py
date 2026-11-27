"""List the Pareto-optimal allocations of an instance with alpha >= theta (the 'obstacle set' a
sub-2/3 modification must destroy).  Brute force over n^m (small instances only); exact arithmetic.

python3 obstacles.py K THETA_NUM THETA_DEN   (Theorem 2 instance at K)
"""
import itertools
import sys
from fractions import Fraction

from poefx import thm2

NAMES = "xyabcdepq"


def alloc_alpha(V, own):
    n, m = len(V), len(V[0])
    B = [[g for g in range(m) if own[g] == i] for i in range(n)]
    u = [sum(V[i][g] for g in B[i]) for i in range(n)]
    a = None
    for j in range(n):
        if len(B[j]) < 2:
            continue
        for i in range(n):
            if i == j:
                continue
            r = Fraction(u[i], sum(V[i][g] for g in B[j]) - min(V[i][g] for g in B[j]))
            if a is None or r < a:
                a = r
    return a, u, B


def po_filter(V, cands):
    """Return the candidates whose profile is maximal among all n^m profiles (pure Python)."""
    n, m = len(V), len(V[0])
    profiles = set()
    for own in itertools.product(range(n), repeat=m):
        u = [0] * n
        for g, i in enumerate(own):
            u[i] += V[i][g]
        profiles.add(tuple(u))
    prof = sorted(profiles, reverse=True)
    front = []
    for p in prof:
        if not any(all(f[i] >= p[i] for i in range(n)) for f in front):
            front.append(p)
    fs = set(front)
    return [c for c in cands if tuple(c[1]) in fs]


if __name__ == "__main__":
    K = int(sys.argv[1])
    th = Fraction(int(sys.argv[2]), int(sys.argv[3]))
    V = thm2(K)
    cands = []
    for own in itertools.product(range(4), repeat=9):
        a, u, B = alloc_alpha(V, own)
        if a is None or a >= th:
            cands.append((a, u, B))
    po = po_filter(V, cands)
    po.sort(key=lambda c: (c[0] is None, c[0] or 0), reverse=True)
    for a, u, B in po:
        print(a, float(a) if a else None, u, ["".join(NAMES[g] for g in b) for b in B])
    print("count", len(po))
