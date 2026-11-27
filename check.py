"""Certify the four independent large-value perturbations, over reals, with integers only."""
from itertools import product
import json

GOODS = 'xyabcdepq'
# A row entry is the triple of coefficients of K, H_i, 1.
K, H, L = (1, 0, 0), (0, 1, 0), (2, 0, 2)
ONE, TWO = (0, 0, 1), (0, 0, 2)
ROWS = ((H,L,K,K,ONE,ONE,K,TWO,ONE), (L,H,ONE,K,K,ONE,K,ONE,TWO),
        (H,L,ONE,ONE,K,K,K,TWO,ONE), (L,H,K,ONE,ONE,K,K,ONE,TWO))
CASES = tuple(map(''.join, product('BLEG', repeat=4)))
ALL = (1 << len(CASES)) - 1
CENTER = 1 << CASES.index('EEEE')
WITNESSES = ('abe x cdpq y', 'x bce y adpq', 'x beq acdp y',
             'y bcpq x ade', 'abpq y cde x')
FULL = (1 << len(GOODS)) - 1


def submasks(mask):
    sub = mask
    while True:
        yield sub
        if not sub:
            return
        sub = (sub - 1) & mask


def coefficients(row, mask):
    return tuple(sum(v[t] for g, v in enumerate(row) if mask & (1 << g)) for t in range(3))


VALUES = [[coefficients(row, mask) for mask in range(FULL + 1)] for row in ROWS]


def diff(v, w):
    return tuple(a - b for a, b in zip(v, w))


def possible(d, case, strict):
    """Can a*K+b*H+c be positive (strict) or nonnegative anywhere in this row's cell?"""
    a, b, c = d
    if case == 'G' and b > 0:
        return True  # H unbounded above
    # Choose the endpoint maximizing the affine function for fixed K.
    base = case == 'B' or (case == 'L' and b < 0)
    slope = a + (2 if base else 3) * b
    at_six = 6 * slope + c + (2 * b if base else 0)
    attained = case in 'BE' or b == 0
    return slope > 0 or at_six > 0 or (at_six == 0 and attained and not strict)


def chamber_masks(i):
    return {c: sum(1 << j for j, s in enumerate(CASES) if s[i] == c) for c in 'BLEG'}


def mask_allocation(text):
    if sorted(text.replace(' ', '')) != sorted(GOODS) or len(text.split()) != 4:
        raise ValueError(text)
    return tuple(sum(1 << GOODS.index(g) for g in s) for s in text.split())


def comparisons(A):
    for i, own in enumerate(A):
        for j, other in enumerate(A):
            if i != j:
                for g in range(len(GOODS)):
                    if other & (1 << g):
                        yield i, VALUES[i][own], VALUES[i][other ^ (1 << g)]


def efx_cases(A):
    valid = ALL
    for i, own, remainder in comparisons(A):
        d = diff(remainder, own)
        for c, mask in chamber_masks(i).items():
            if possible(d, c, True):
                valid &= ~mask
    return valid


def po_cases(A, eligible):
    """Drop a cell even if different agents need incompatible K's for the rival. Safe for PO proof."""
    weak, strict = [], []
    for i, own in enumerate(A):
        masks = chamber_masks(i)
        gaps = [diff(v, VALUES[i][own]) for v in VALUES[i]]
        for table, positive in ((weak, False), (strict, True)):
            table.append([sum(m for c, m in masks.items() if possible(d, c, positive)) for d in gaps])
    # Enumerate ordered disjoint bundles. If a weak comparison is impossible, every extension fails.
    def visit(i, unused, tied_or_better, improved):
        if i == 3:
            return tied_or_better & weak[i][unused] & (improved | strict[i][unused])
        eliminated = 0
        for take in submasks(unused):
            keep = tied_or_better & weak[i][take]
            if keep:
                eliminated |= visit(i + 1, unused ^ take, keep, improved | strict[i][take])
        return eliminated
    return eligible & ~visit(0, FULL, eligible, 0)


def shifted(v):
    """At H=3K, constant and linear coefficients in t=K-6."""
    slope = v[0] + 3*v[1]
    return 6*slope + v[2], slope


def factor_gap(u, v):
    """Coefficients of 3K*own - (2K+3)*remainder in t=K-6."""
    return (18*u[0]-15*v[0], 3*u[0]+18*u[1]-2*v[0]-15*v[1], 3*u[1]-2*v[1])


def center(A):
    tight = False
    for _, own, remaining in comparisons(A):
        u, v = shifted(own), shifted(remaining)
        p = factor_gap(u, v)
        if min(p) < 0:
            raise ValueError('unproved center comparison')
        tight |= p == (0, 0, 0) and v[0] > 0
    if not tight or po_cases(A, CENTER) != CENTER:
        raise ValueError('center witness failed')


def center_upper():
    # Fixed Pareto improvements for the allocations not uniformly excluded by fairness.
    rivals = tuple(map(mask_allocation, (
        'abp xq cde y', 'abe y cdp xq', 'abe xq cdp y', 'bep yc x adq',
        'aep bcq xd y', 'aep bcq x yd', 'yp bcq x ade', 'xa beq cdp y',
        'x beq cdp ya', 'x bcq yp ade', 'bep y xc adq', 'yp bce x adq',
        'abp y cde xq', 'x bce yp adq', 'xb y cep adq', 'x yb cep adq')))
    subsets = tuple(tuple(submasks(s)) for s in range(FULL + 1))
    excluded, weak, strict = [], [], []
    for i, row in enumerate(VALUES):
        values = list(map(shifted, row))
        veto = [set() for _ in row]
        for other in range(1, FULL + 1):
            if other.bit_count() < 2:
                continue
            # Any one removed good can certify an upper bound. Choose a least
            # valuable one at K=6; the polynomial, not this choice, proves it for all K.
            drop = min((1 << g for g in range(len(GOODS)) if other >> g & 1),
                       key=lambda bit: values[bit][0])
            v = values[other ^ drop]
            for own in subsets[FULL ^ other]:
                if max(factor_gap(values[own], v)) <= 0:
                    veto[own].add(other)
        excluded.append(veto)
        flags = [[(values[B[i]][0]-u, values[B[i]][1]-s) for B in rivals] for u,s in values]
        weak.append([sum(1 << j for j,(c,s) in enumerate(ds) if c >= 0 and s >= 0) for ds in flags])
        strict.append([sum(1 << j for j,(c,s) in enumerate(ds) if c > 0 and s >= 0) for ds in flags])
    tested = dominated = 0
    for x in subsets[FULL]:
        for y in subsets[FULL ^ x]:
            rest = FULL ^ x ^ y
            for z in subsets[rest]:
                A = (x, y, z, rest ^ z)
                tested += 1
                if any(other in excluded[i][own] for i, own in enumerate(A) for other in A if other != own):
                    continue
                w, s = (1 << len(rivals))-1, 0
                for i, own in enumerate(A):
                    w &= weak[i][own]
                    s |= strict[i][own]
                if not w & s:
                    raise ValueError(('no upper certificate', A))
                dominated += 1
    if tested != 4**len(GOODS):
        raise ValueError('incomplete enumeration')
    return {'allocations': tested, 'excluded_by_fairness': tested-dominated,
            'excluded_by_pareto_improvement': dominated, 'fixed_improvements': len(rivals)}


def perturbation_tube(anchor):
    """Allow every entry, independently, to move by strictly less than 1/3."""
    candidates = []
    for row, t in zip(VALUES, anchor):
        allowed = []
        for m, v in enumerate(row):
            a, b, c = diff(v, row[t])
            # Contributions of common goods cancel in the utility difference.
            allowed.append(m == t or possible((3*a, 3*b, 3*c + (m ^ t).bit_count()), 'E', True))
        candidates.append(allowed)
    protected = []

    def visit(prefix, unused):
        i = len(prefix)
        for m in (submasks(unused) if i < 3 else (unused,)):
            if not candidates[i][m]:
                continue
            A = (*prefix, m)
            if i < 3:
                visit(A, unused ^ m)
                continue
            for observer, t in enumerate(A):
                for j, other in enumerate(A):
                    if observer == j:
                        continue
                    for g in range(len(GOODS)):
                        if not other & (1 << g):
                            continue
                        r = other ^ (1 << g)
                        u, v = VALUES[observer][t], VALUES[observer][r]
                        a, b, c = (9*x - 6*y for x, y in zip(u, v))
                        c -= 3*t.bit_count() + 2*r.bit_count()
                        if possible((-a, -b, -c), 'E', True):
                            raise ValueError('unprotected Pareto improvement')
            protected.append(A)

    visit((), FULL)
    if set(protected) != {anchor, mask_allocation('xb y cepq ad')}:
        raise ValueError('unexpected possible dominator of the anchor')
    return len(protected)


def main():
    anchor = mask_allocation('xb y cdpq ae')
    center(anchor)
    protected = perturbation_tube(anchor)
    covered = 0
    certificate = {}
    for text in WITNESSES:
        A = mask_allocation(text)
        valid = po_cases(A, efx_cases(A))
        certificate[text] = [s for j, s in enumerate(CASES) if ((valid & ~covered) >> j) & 1]
        covered |= valid
    if covered != ALL ^ CENTER:
        raise ValueError('incorrect coverage: ' + str([s for j,s in enumerate(CASES) if not covered >> j & 1]))
    print(json.dumps({'center_allocation': 'xb y cdpq ae', 'center_witness_factor': '(2K+3)/(3K)',
                      'center_upper_real_K_at_least_6': center_upper(),
                      'tube_radius_exclusive': '1/3', 'possible_weak_dominators_in_tube': protected,
                      'off_center_cells_certified': covered.bit_count(), 'efx_po_witness_by_cell': certificate}))


if __name__ == '__main__':
    main()
