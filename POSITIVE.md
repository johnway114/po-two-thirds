# Positive cases for PO + EFX / (2/3)-EFX with positive additive goods

Status: **written proof, independently reviewed internally, unrefereed.** The counterexamples below test proof strategies, not the unrestricted existence question. See the [audit](AUDIT.md) for the scope and the qualifications corrected after review.

## Model and exact quantifiers

- Agents `N = {1..n}`, goods `M`, `|M| = m`. Each `v_i` is additive and `v_i(g) > 0` for every `i, g`. Values are real.
- Allocation: a partition `A = (A_1..A_n)` of all of `M`. Empty bundles are allowed.
- `alpha`-EFX (`0 < alpha <= 1`): for all `i != j` and all `g in A_j`, `v_i(A_i) >= alpha * v_i(A_j \ {g})`. EFX = 1-EFX.
- PO: no allocation `B` has `v_i(B_i) >= v_i(A_i)` for all `i`, with strict inequality for some `i`.
- **Strict singleton preferences:** for each agent `i`, `v_i(g) != v_i(h)` for distinct goods `g != h`. Any set of real values outside a measure-zero set has this property.
- With `m = n + 1`, an allocation `A` with holder `j` and pair `P` means `|A_j| = 2`, `A_j = P`, and every other agent `l` has one good `a_l`.

The [source paper](https://arxiv.org/pdf/2610.29201v2) uses four agents with eight goods for incompatibility of full EFX and efficiency, and four with nine goods for the upper bound on approximate fairness. Here we instead restrict the surplus of goods over agents, with no bound on disagreement about their values.

## Result summary

| Class | Claim | Status |
|---|---|---|
| `m <= n` | A PO allocation that is EFX always exists. | Proof below (elementary; likely folklore) |
| `m = n+1` with strict singleton preferences | Every allocation that weakly Pareto-dominates an EFX allocation is EFX, and it keeps the same two-good bundle. Therefore a PO allocation that is EFX, and hence (2/3)-EFX, exists. | Proof below |
| `m = n+1` with an allocation where each non-holder **strictly** prefers its good to both pair goods | A PO EFX allocation exists; closure is guaranteed above that strongly EFX allocation, not above arbitrary EFX allocations. | Proof below |
| `m = n+1` with ties | The upward-closure lemma fails (exact witness). PO + EFX existence remains open in this work. | Exact witness; existence open |
| `m = n+2` | The upward-closure route fails even with strict preferences (exact witness). Existence is open here. | Exact witness |
| Maximum Nash welfare at `m = n+1` | Can be only (1/2)-EFX with `n = 2`. | Exact check by hand |

Under strict singleton preferences, the instances with no PO allocation that is EFX, or no PO (2/3+)-EFX allocation, therefore need at least two surplus goods. Published witnesses use four surplus goods (exact EFX) and five surplus goods (`alpha > 2/3`). Surpluses 2 and 3, and surplus 1 with ties, are still unresolved here.

## Basic facts (positive values)

**F1.** If `m >= n` and `A` is `alpha`-EFX for some `alpha > 0`, then every bundle is nonempty.
Proof: suppose `A_i` is empty. The other `n-1` agents hold `m >= n` goods, so some `A_j` has at least two goods. For any `g in A_j`, `v_i(A_j \ {g}) > 0 = v_i(A_i)`. This violates `alpha`-EFX.

**F2.** Suppose every agent has positive utility in `A`. If `v(B) >= v(A)` componentwise, then every `B_i` is nonempty.
Proof: `v_i(B_i) >= v_i(A_i) > 0`.

For `m = n+1`, F1 and F2 imply that all EFX allocations, and all allocations weakly dominating them, consist of one two-good bundle and `n-1` singletons. If the pair is `P` and its holder is `j`, then for every other agent `l`:
EFX is equivalent to `v_l(a_l) >= max_{p in P} v_l(p)`, and `alpha`-EFX is equivalent to `v_l(a_l) >= alpha * max_{p in P} v_l(p)`. The holder `j` cannot violate EFX against a singleton.

## Theorem 0 (`m <= n`)

For every positive additive instance with `m <= n`, some allocation is PO and EFX.

Proof. Fix any set `T` of `m` agents. Among the bijections `T -> M`, choose one, `sigma`, that maximizes `sum_{i in T} v_i(sigma(i))`. Agents outside `T` receive nothing. Every bundle has at most one good, so EFX holds vacuously.
Suppose `B` dominates this allocation. Every agent in `T` has positive utility, so each of those `m` agents receives at least one of the `m` goods in `B`. Hence each receives exactly one, and agents outside `T` receive nothing. Thus `B` is a bijection `T -> M` with weakly larger utilities and one strict increase. Its sum is larger, which contradicts the choice of `sigma`. ∎

## Theorem 1 (`m = n+1`, strong EFX is upward closed)

Call an allocation with holder `j` and pair `P` **strongly EFX** if every `l != j` satisfies `v_l(a_l) > v_l(p)` for both `p in P`.

**Lemma 1.** Let `m = n+1`, with all values positive. Let `A` be strongly EFX, with holder `j` and pair `P`. Let `B` be any allocation with `v_i(B_i) >= v_i(A_i)` for all `i`. Then `B` is strongly EFX, and its two-good bundle is exactly `P`. Its holder may differ from `j`.

Proof. By F2, `B` has one pair `Q` held by some `h` and singletons `b_i`. Let `S = N \ {j, h}`. These agents have singletons in both `A` and `B`.

1. No agent `l in S` holds a good of `P` in `B`. If `b_l = p in P`, then `v_l(b_l) >= v_l(a_l) > v_l(p)` gives a contradiction.
2. If `h != j`, agent `j` has a singleton `b_j` in `B`, and `b_j` is not in `P`. If `b_j = p in P`, then `v_j(b_j) >= v_j(P) = v_j(p) + v_j(p') > v_j(p)` because `v_j(p') > 0`. This is a contradiction.
3. Steps 1 and 2 imply that no singleton in `B` contains a good of `P`. Therefore `P ⊆ Q`. Because `|P| = |Q| = 2`, `Q = P`.
4. Strong EFX for `B`: let `i != h` and `p in P`. If `i in S`, then `v_i(b_i) >= v_i(a_i) > v_i(p)`. If `i = j` (only possible when `h != j`), then `v_j(b_j) >= v_j(P) > v_j(p)`. ∎

**Theorem 1.** Let `m = n+1` and all values be positive. Suppose some allocation is strongly EFX. Then a PO allocation exists that is strongly EFX, hence EFX and (2/3)-EFX. More strongly, every PO allocation that weakly dominates a strongly EFX allocation is strongly EFX.

Proof. Let `A` be strongly EFX. The set of allocations weakly dominating `A` is finite and nonempty. Take one whose utility profile is maximal under Pareto dominance in this set. Dominance is transitive, so this allocation is PO. By Lemma 1, it is strongly EFX. The "more strongly" statement is Lemma 1 applied directly. ∎

**Corollary 1 (strict singleton preferences).** Let `m = n+1`, with all values positive and strict singleton preferences. Then a PO allocation that is EFX exists. Consequently, every PO allocation that weakly dominates any EFX allocation is EFX.

Proof. Under strict singleton preferences, EFX implies strong EFX when `m = n+1`: if `v_l(a_l) >= v_l(p)` and `a_l != p`, then the inequality is strict. Strongly EFX allocations exist. Fix any order of agents. The first `n-1` agents each take their favorite remaining good, and the last agent takes the remaining two goods. When agent `l` picks, both eventual pair goods are still available. Therefore `l` prefers `a_l` to each of them, strictly by assumption. Then apply Theorem 1. ∎

**Corollary 2 (Pareto improvements).** Under the hypotheses of Lemma 1, every Pareto improvement of a strongly EFX allocation keeps the bundle `P` intact. A Pareto-improvement procedure starting from the picking-order allocation therefore never leaves the EFX set **if the starting allocation is strongly EFX**, in particular under strict singleton preferences.

## Scope limits and obstructions

### Ties at `m = n+1`: the upward-closure lemma fails

The witness below was found by exhaustive enumeration with exact arithmetic (integers and `Fraction`). It was also checked by hand. Agents are numbered 1–3 and goods `g0..g3`:

```
v1 = [1,5,6,2]   v2 = [4,6,4,6]   v3 = [5,3,5,4]
A = (g0g3, g1, g2)   utilities (3,6,5)    EFX (agent 2: max(v2(g0),v2(g3)) = 6 <= 6, tie)
B = (g1, g3, g0g2)   utilities (5,6,10)   weakly dominates A; B is PO (exhaustive)
B is only 5/6-EFX: agent 1 has 5 < v1(g2) = 6
```

Mechanism: agent 2 moves to `g3`, a pair good that she values exactly as much as her own good. This is the step that strictness rules out in Lemma 1. This example does not rule out a different efficient EFX allocation. Our existence proof does not settle `m = n+1` with ties.

### `m = n+2`: the upward-closure route fails even with strict preferences

Exact witness (`n=3`, `m=5`, each row has distinct values; checked by hand):

```
v1 = [10,5,12,6,11]   v2 = [15,9,1,8,4]   v3 = [11,1,3,2,6]
A = (g1g4, g2g3, g0)    utilities (16,9,11)   EFX (agent 1 vs g2g3: 12 <= 16; agent 2 vs g1g4: 9 <= 9; agent 3: 6, 3 <= 11)
B = (g2g3g4, g1, g0)    utilities (29,9,11)   weakly dominates A; B is PO (exhaustive)
B is only 3/4-EFX: agent 2 has 9 vs v2({g3,g4}) = 12
```

At `m = n+2`, a PO allocation that dominates an EFX allocation can therefore lose EFX. Lemma 1 has no direct extension. This witness says nothing about non-existence.

### Other routes that fail at `m = n+1`

- **Maximum Nash welfare is not EFX.** With two agents and goods `(a,g,h)`, take `v1 = (10,20,1)` and `v2 = (1,100,40)`. The six nonempty splits give Nash products 1400, 1200, 1100, 820, 101 and 21, and an empty bundle gives zero. The maximum is `a | gh`. Agent 1 values `g` at 20 and `a` at 10: this efficient allocation is only 1/2-EFX. A different allocation, `g | ah`, is EFX and PO. So one cannot prove even 2/3 by equating PO with Nash maximization.
- **Fractional PO is too strong.** See the exact two-agent example in [SOURCES.md](SOURCES.md). Weighted leximin with positive weights, in contrast, always gives integral PO; the question is its fairness.

## Relation to prior and parallel work

- Plaut–Roughgarden ([SIDMA 2020 / arXiv:1707.04769](https://arxiv.org/abs/1707.04769)): PO + EFX under nonzero marginal utility for two agents (leximin after normalization) and for identical valuations. Corollary 1 covers `n=2`, `m=3` only for generic values, so it adds nothing new for two agents.
- Amanatidis et al. (TCS 2021, MNW and EFX), and Garg–Murhekar (TCS 2023): bivalued instances. Hosseini et al. (AAAI 2021): lexicographic preferences. Davidiuk et al. ([AAAI 2026](https://ojs.aaai.org/index.php/AAAI/article/view/38723)): two types of goods. These classes are orthogonal to the surplus restriction used here.
- Lim–Neoh–Teh ([arXiv:2601.12849](https://arxiv.org/abs/2601.12849)): in the few-surplus setting `m = n + c`, `c <= 3`, deciding whether an allocation that is both EFX and PO exists is NP-hard when zero values are allowed (Thm 5.2). Under nonzero marginal utility, they compute an EFX allocation that maximizes p-mean welfare among EFX allocations (Thm 6.1). That result does **not** imply PO. Theorem 1 addresses the positive-value PO + EFX question at `c = 1` under strict singleton preferences, which the paper leaves open. Their NP-hardness relies on zero values, so it does not conflict with this result.
- Amanatidis–Filos-Ratsikas–Sgouritsa (EC 2024): (2/3)-EFX in special cases, without PO.
- No explicit statement of Theorem 1 was found in this search. The search was limited: two web searches plus reading the MRT and LNT papers. Treat novelty as unverified.
- **Complementary sufficient condition, with any number of goods.** Let `R_ij=max_g v_i(g)/v_j(g)` for a nonempty goods set. If every directed cycle has product of `(2/3)R_ij` at most 1, there exist positive multipliers satisfying `lambda_j >= (2/3)R_ij lambda_i`: take the maximum product along paths to each vertex starting anywhere with weight 1. Deleting a cycle cannot decrease a path's product, so finite simple paths suffice. Conversely multiplying the inequalities proves necessity for these multipliers. Maximize the sorted vector of normalized utilities `lambda_i v_i(A_i)` lexicographically, from smallest to largest. This is PO because a Pareto improvement strictly increases the sorted vector. If agent i violated 2/3-EFX toward j after deleting g, j's normalized utility **even without g** would exceed i's current normalized utility by the multiplier inequalities and additivity. Moving g to i strictly raises i and leaves j above i's old level. That strictly improves the sorted vector, a contradiction. This condition restricts disagreement, not surplus. It is sufficient, not necessary for existence.

## Suggested next steps

1. Prove or refute PO + EFX at `m = n+1` with ties. One candidate is to choose an EFX allocation that is Pareto-maximal among EFX allocations. The tie witness shows that an arbitrary PO dominator does not work.
2. For `m = n+2` with strict preferences, test PO + (2/3)-EFX existence by exhaustive search over all allocations. Use structured instances built around pair and triple bundles instead of local search, which lacked the power to find known counterexamples.
