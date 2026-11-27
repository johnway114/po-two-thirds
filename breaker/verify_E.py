"""Independent pure-Python (Fraction) recheck of the common-good experiment (no C code used).

For the square family of arXiv:2610.29201 Thm 2 at K=20 (side goods K/1, smalls 2/1), vary the
common good e's value E and report exact F* = max alpha over PO allocations, by full enumeration
of 4^9 allocations and the exact Pareto frontier of utility profiles.
"""
import itertools
import json
from fractions import Fraction

from families import square
from obstacles import alloc_alpha

CASES = [  # (E, X1, X2): paper point, best E=18 grid point, and E>K points
    (20, 60, 42),
    (18, 58, 42),
    (22, 62, 42),
    (24, 64, 42),
    (40, 80, 60),
]


def fstar(V):
    n, m = len(V), len(V[0])
    rows = []
    for own in itertools.product(range(n), repeat=m):
        a, u, B = alloc_alpha(V, own)
        rows.append((tuple(u), a, own))
    profs = sorted({r[0] for r in rows}, reverse=True)
    front = []
    for p in profs:
        if not any(all(f[i] >= p[i] for i in range(n)) for f in front):
            front.append(p)
    fs = set(front)
    best = None
    for u, a, own in rows:
        if u in fs:
            key = Fraction(10**9) if a is None else a
            if best is None or key > best[0]:
                best = (key, own, u)
    return best


if __name__ == "__main__":
    out = []
    for E, X1, X2 in CASES:
        V = square(20, X1, X2, commons=(E,))
        F, own, u = fstar(V)
        rec = {"K": 20, "E": E, "X1": X1, "X2": X2, "Fstar": str(F), "witness_owner": list(own), "profile": list(u)}
        print(json.dumps(rec), flush=True)
        out.append(rec)
    with open("RECEIPT_E.json", "w") as f:
        json.dump(out, f, indent=1)
