# The exact obstruction in the published square

Use good order `x y a b c d e p q`. Write L=2K+2. Independently vary four real numbers Hᵢ in [L,∞). The rows are

```
H₁ L   K K 1 1 K 2 1
L  H₂  1 K K 1 K 1 2
H₃ L   1 1 K K K 2 1
L  H₄  K 1 1 K K 1 2
```

**Classification.** For every real K≥6, if at least one Hᵢ differs from 3K, there is a complete, fully EFX allocation that is Pareto optimal among complete indivisible allocations. If all four equal 3K, the best factor is exactly (2K+3)/(3K). The source states its upper bound for integer K; the certificate below also covers noninteger K.

## The center: why the upper bound is attained

Take `(xb, y, cdpq, ae)`, with agents in row order. Utilities are `(4K, 3K, 2K+3, 2K)`. For each agent, the most valuable remainder of any other bundle after removing one good is respectively `K, 2K+2, 3K, 2K+2`. The binding comparison is agent 3 looking at `xb` after removing `b`. In particular the last ratio, `2K/(2K+2)`, is at least `(2K+3)/(3K)` because `2K²−10K−6≥0` for K≥6. Thus the factor is exact, not just a passing test at 2/3.

The total utility is 11K+3, just one short of the sum of the column maxima, 11K+4. Giving a good to anyone below its column maximum loses at least one: the possible positive losses are K−2, K−1 and 1. Thus even for real K a Pareto improvement must give every good to an agent attaining its maximum. The two large goods and five medium goods then supply eleven units of K in total. Each agent can receive **at most one** small good worth 2 at its column maximum: the odd agents compete for `p`, the even agents for `q`. Keeping the four original utilities requires at least 4, 3, 3 and 2 units of K, respectively. In particular two units plus one small good cannot reach agent 3's old utility of 2K+3. Twelve units are needed and only eleven exist. So the allocation is Pareto optimal, though it does not maximize total welfare.

**Independent upper certificate.** [The paper's §4 Theorem 2](https://arxiv.org/pdf/2610.29201v2) supplies the integer-K upper bound. For a replay covering all real K≥6, `center_upper()` enumerates all 4⁹ assignments. For each observer, choose a good to remove from each rival bundle of size at least two. Let U be the observer's own value, V the trimmed rival value. If all coefficients of `3K·U−(2K+3)·V` in `t=K−6` are nonpositive, the assignment fails every strictly larger factor throughout the half-line (V is positive). The remaining 216 assignments each have a fixed Pareto improvement from a list of sixteen. For each improving assignment every utility difference has nonnegative constant and slope in t, with a positive constant for at least one agent. Exhaustion is over assignments, **not** sampled K. This supplies the matching upper bound including at K=6; it does not reject fairness at equality.

## Off center: proving a continuous claim by a finite certificate

For each agent distinguish four possibilities: `B` means Hᵢ=L; `L` means L<Hᵢ<3K; `E` means Hᵢ=3K; `G` means Hᵢ>3K. These four states include both boundary faces and partition the full allowable interval. (The letter `L` in a cell code denotes the *open* lower interval.) Of 256 combinations only `EEEE` is the published center. Five fixed allocations suffice for the other 255. The [receipt](RECEIPT.json) assigns an allocation to each case. Every one gives `x` and `y` as singletons.

[The checker](check.py) works with each bundle's exact coefficient triple: its value to agent i is `aK+bHᵢ+c`. To test whether a difference can be positive or nonnegative, first maximize it over the allowed Hᵢ at fixed K. A positive coefficient on an unbounded upper interval gives an unbounded supremum. Otherwise the supremum is affine in K and comes from one of `2K+2` and `3K`. If the interval is open, that endpoint is not attained unless `b=0`. An affine function on K≥6 either grows without bound or has its maximum at 6. In particular a supremum of zero on an excluded face is **not** a feasible weak improvement. This calculation uses integers only; it covers irrational values too.

For each witness A and each cell:

1. Reject its fairness certificate if any observer can *strictly* prefer any trimmed rival bundle to their own anywhere in the cell. Each such difference uses only one row.
2. Enumerate all ordered partitions B, pruning a partial partition only when a necessary weak improvement already fails. Reject A's PO certificate if every agent could weakly improve and at least one could strictly improve. This test even lets different rows use **different K** in the same attempted domination; rejection can therefore be spurious, but acceptance cannot. Every actual Pareto improvement would cause rejection. Equal profiles alone do not disqualify a witness.
3. The union of the certified cells has to equal the 255 off-center cases exactly. At the center a separate check certifies PO of `(xb, y, cdpq, ae)` by the same test and verifies all fairness comparisons as quadratic polynomials with nonnegative coefficients in `K−6`, including an identically binding comparison with positive denominator.

This explains why simply nudging a favorite large value to increase envy fails as a counterexample strategy. At 3K a favorite large good is exactly exchangeable for three favorite medium goods. Breaking even one such equality allows a *different* allocation to retain full fairness without being dominated. The certificate is confined to the displayed matrix; it does not say all hard instances rely on ties.
