"""Structured instance families for the PO alpha-EFX breaker hunt.

A family is described by an incidence structure: each good has a set of 'incident' agents
(value hi) and everyone else gets value lo.  This generalizes Theorem 2 of arXiv:2610.29201
(square / dihedral incidence) to other graphs and to extra common or large goods.
"""
from fractions import Fraction

from poefx import evaluate


def incidence_matrix(n, goods):
    """goods: list of (incident_set, hi, lo). Returns n x m integer matrix."""
    return [[hi if i in inc else lo for (inc, hi, lo) in goods] for i in range(n)]


def square(K, X1, X2, M1=None, M2=1, commons=(), S1=2, S2=1, extra=()):
    """Paper square: agents 0..3 cyclic; x,p on diagonal {0,2}; y,q on {1,3};
    sides a=(0,3), b=(0,1), c=(1,2), d=(2,3).  commons: list of values valued by all.
    extra: list of additional (incident_set, hi, lo) goods."""
    M1 = K if M1 is None else M1
    goods = [({0, 2}, X1, X2), ({1, 3}, X1, X2)]
    goods += [({0, 3}, M1, M2), ({0, 1}, M1, M2), ({1, 2}, M1, M2), ({2, 3}, M1, M2)]
    goods += [(set(range(4)), c, c) for c in commons]
    goods += [({0, 2}, S1, S2), ({1, 3}, S1, S2)]
    goods += list(extra)
    return incidence_matrix(4, goods)


def describe(V, own):
    n = len(V)
    bundles = [[g for g, o in enumerate(own) if o == i] for i in range(n)]
    worst = None
    for i in range(n):
        ui = sum(V[i][g] for g in bundles[i])
        for j in range(n):
            if i == j or len(bundles[j]) < 2:
                continue
            d = sum(V[i][g] for g in bundles[j]) - min(V[i][g] for g in bundles[j])
            r = Fraction(ui, d)
            if worst is None or r < worst[0]:
                worst = (r, i, j)
    return bundles, worst


if __name__ == "__main__":
    import sys
    K = 30
    rows = []
    for X1, X2, commons in [
        (3 * K, 2 * K + 2, (K,)),
        (4 * K, 3 * K, (K, K)),
        (4 * K, 3 * K + 2, (K, K)),
        (4 * K, 2 * K + 2, (K, K)),
        (4 * K, 3 * K + 2, (K,)),
    ]:
        V = square(K, X1, X2, commons=commons)
        r = evaluate(V)
        b, w = describe(V, r["argmax_owner"])
        print(X1, X2, commons, "F*", r["Fstar"], float(r["Fstar"]), "bundles", b, "binding", w, flush=True)
