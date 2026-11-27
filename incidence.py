"""A04: constructive census of three medium-good incidence signatures (no solver)."""
import json
from collections import Counter
from itertools import combinations, permutations, product

GOODS = 'xyabcdepq'
SHAPES = ((2, 2, 2, 2, 4), (2, 2, 2, 3, 3), (1, 2, 3, 3, 3))
# Each bit denotes a high valuer; a..e in the order of the source paper.
SQUARE = (9, 3, 6, 12, 15)
MIXED = tuple(product((0, 2), (1, 3)))
# These permutations preserve the two camps or interchange them as whole sets.
# In the latter case also interchange x with y and p with q.
RELABEL = tuple(tuple(sum(1 << p[i] for i in range(4) if mask >> i & 1) for mask in range(16))
                for p in permutations(range(4)) if p[0] % 2 == p[2] % 2)


def canonical(cols):
    return min(tuple(sorted(relabel[m] for m in cols)) for relabel in RELABEL)


def values(cols, i, k):
    large = (3*k, 2*k+2) if i % 2 == 0 else (2*k+2, 3*k)
    small = (2, 1) if i % 2 == 0 else (1, 2)
    return (*large, *(k if m >> i & 1 else 1 for m in cols), *small)


def witness(cols):
    for i, j in MIXED:
        if all(m & ((1 << i) | (1 << j)) for m in cols):
            # Give the shared favorite to i. The other member of i's (j's)
            # camp gets the singleton x (y). i gets p, j gets q.
            return 'full', (2-i, 4-j, *(i if m >> i & 1 else j for m in cols), i, j)
    if sorted(cols) != sorted(SQUARE):
        raise ValueError(('new obstruction to the mixed-pair construction', cols))
    # Port (xb, y, cdpq, ae) by permuting the five medium goods only.
    source_owners = dict(zip(SQUARE, (3, 0, 2, 2, 3), strict=True))
    return 'square', (0, 1, *(source_owners[m] for m in cols), 2, 2)


def margins(cols, kind, owner, k):
    """Every margin below is affine in k; nonnegative means the obligation holds."""
    v = [values(cols, i, k) for i in range(4)]
    bundles = [[g for g, h in enumerate(owner) if h == i] for i in range(4)]
    if kind == 'full':
        for g, h in enumerate(owner):
            for i in range(4):
                yield v[h][g] - v[i][g]  # Every good at its column maximum => PO.
    else:
        # Require actual equality with the published matrix AND its certified PO
        # witness, not merely the same column sizes, totals or fairness factor.
        indices = [0, 1, *(2 + SQUARE.index(m) for m in cols), 7, 8]
        if sorted(indices) != list(range(9)):
            raise ValueError('not a column permutation')
        for i in range(4):
            source = values(SQUARE, i, k)
            if v[i] != tuple(source[g] for g in indices):
                raise ValueError('not the original instance')
        if owner != tuple((0, 1, 3, 0, 2, 2, 3, 2, 2)[g] for g in indices):
            raise ValueError('not the original efficient witness')
    n, d = (1, 1) if kind == 'full' else (2, 3)
    for i, own in enumerate(bundles):
        utility = sum(v[i][g] for g in own)
        for j, other in enumerate(bundles):
            if i != j:
                for removed in other:
                    remainder = sum(v[i][g] for g in other if g != removed)
                    yield d*utility - n*remainder


def main():
    counts = Counter()
    for rows in product(combinations(range(5), 3), repeat=4):
        cols = tuple(sum(1 << i for i, row in enumerate(rows) if g in row) for g in range(5))
        if tuple(sorted(m.bit_count() for m in cols)) in SHAPES:
            counts[canonical(cols)] += 1

    records = []
    classes = Counter()
    for cols, size in sorted(counts.items()):
        kind, owner = witness(cols)
        # For f(k)=a*k+b, f(6)>=0 and f(7)>=f(6) prove f(k)>=0 on [6,infinity).
        if any(at6 < 0 or at7 < at6 for at6, at7 in
               zip(margins(cols, kind, owner, 6), margins(cols, kind, owner, 7), strict=True)):
            raise ValueError(('uncertified witness', cols, owner))
        signature = ''.join(map(str, sorted(m.bit_count() for m in cols)))
        classes[signature,kind] += size
        records.append({'signature': signature, 'medium_high_valuer_masks': cols, 'labelled_count': size,
                        'kind': kind, 'bundles': [''.join(g for g,h in zip(GOODS, owner) if h == i)
                                                  for i in range(4)]})
    print(json.dumps({'row_choices_examined': len(tuple(combinations(range(5), 3)))**4,
                      'in_scope': sum(counts.values()), 'orbits': len(records),
                      'classes': {s+'_'+k: v for (s,k),v in sorted(classes.items())},
                      'certificates': records}))


if __name__ == '__main__':
    main()
