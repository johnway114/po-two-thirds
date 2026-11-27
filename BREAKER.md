# BREAKER — negative-direction hunt below 2/3 (A04)

Date: 2026-11-27. Agent: BreakEndpoint (Claude). Status: **no witness found**. This is a bounded hunt.
It does **not** show that every positive instance has a PO 2/3-EFX allocation.

## Question attacked

Find a finite additive goods instance with all values strictly positive in which
`F* := max over complete Pareto-optimal (PO) allocations A of alpha(A) < 2/3`, where
`alpha(A) = min_{i != j, |A_j| >= 2} v_i(A_i) / (v_i(A_j) - min_{g in A_j} v_i(g))`.
This is an **uncapped ratio**; in the paper the EFX factor is capped at 1. A ratio above 1 therefore certifies full EFX, not a distinct fairness guarantee. At the 2/3 threshold the two tests coincide.
PO means no allocation weakly improves every agent and strictly improves at least one.

Primary source: Mahabadi, Ramakrishnan, Tarnawski, *Pareto Inefficiency of EFX*, arXiv:2610.29201v2 (2 Nov 2026).
Theorem 2 gives a 4-agent, 9-good family with parameter `K >= 6` and no PO alpha-EFX allocation for `alpha > 2/3 + 1/K`.
Open Problem 1 asks whether any constant `alpha > 0` is always achievable.

## Tools (all in `breaker/`)

| File | Role |
| --- | --- |
| `poefx.c` + `poefx.py:evaluate` | Brute force over all `n^m` allocations. Computes the exact integer Pareto frontier of utility profiles. Returns exact `F*`. Ratios are compared by 128-bit cross-multiplication. |
| `poefx_dfs.c` + `poefx.py:evaluate_dfs` | Fast discovery code: threshold search followed by a dominator search. Do not use a floating-point pruning decision to certify a counterexample; replay any candidate with the independent exact enumerator. |
| `crosscheck.py` | Seeded agreement test between the two evaluators. Seed 1 covered 300 random instances with n=2–4 and m≤12: **0 mismatches**. |
| `obstacles.py` | Pure-Python list of the PO allocations with `alpha >= theta`, called the obstacle set. |
| `verify_E.py` → `RECEIPT_E.json` | Independent Fraction-based recheck of the common-good experiment. It uses no C code. |
| `families.py`, `grid_E.py` | Generator for the square or dihedral family, and the sweep over the common good's value. |
| `hunt.py`, `hunt2.py`, `hunt3.py` | Seeded annealers. `hunt3` searches `V = K*A + B`: a coarse, zero-allowed incidence layer `A` plus a positive tie-break layer `B`. |

Sanity replay with exact `F*`: the Theorem 2 instance has `F* = 2/3 + 1/K` **exactly** for K = 6, 7, 8, 10, 12, 20, 50, 100, 1000.
So the paper's bound is tight on its own family, and the family's infimum is 2/3 but is never reached.

## Experiment 1 — obstacle set of Theorem 2 (K = 100, θ = 0.6)

`python3 breaker/obstacles.py 100 3 5` writes `breaker/runs/obstacles_K100_0.6.txt`.

The saved list has 384 PO allocations with `alpha >= 0.6`. Of these, **252 have `alpha >= 2/3`** (counting the reduced fractions, not their decimal printouts):

| alpha | count |
| --- | --- |
| 203/300 (= `F*`) | 16 |
| 101/150 | 24 |
| 202/301 | 16 |
| 67/100 | 24 |
| 101/151 | 8 |
| exactly 2/3 | 164 |

There is not a single bundle shape to break. In 136 of those 252 assignments exactly one large good has a companion; in 116 both do. For example, `(xb, y, cepq, ad)` pairs a large good with a medium good, but `(x, bce, yp, adq)` pairs one only with a small good.

A successful change would need to eliminate all 252 witnesses, and also check that no formerly dominated allocation became efficient. An assignment at exactly 2/3 is already a witness **against** endpoint failure.

## Experiment 2 — change the non-large incidence: the common good `e` (bounded, reproducible)

Hypothesis: raising E above w lowers the binding ratio `2w/(2w+E)`, but it may break the value-neutral trade that the paper's domination step uses.

Grid (`python3 breaker/grid_E.py 20`, output `breaker/runs/grid_E_K20.txt`):

- Fixed: K = w = 20, side goods K/1, smalls in {(2,1), (1,1), (3,1)}.
- Swept: E ∈ {10, 12, …, 42}; X1 ∈ [2K, 4K+E) in steps of 2; X2 ∈ [K, X1] in steps of 2.
- The run was stopped after E = 42; the planned range went up to E = 80.
- The C evaluator was used, and its results were cross-checked.

| E | min F* on grid |
| --- | --- |
| 10–16 | 1 (an exact PO EFX allocation exists at the best grid point) |
| 18 | 43/58 ≈ 0.741 |
| 20 (paper) | 43/60 ≈ 0.717 |
| 22–42 | 1 |

The independent Fraction recheck (`breaker/RECEIPT_E.json`; `python3 breaker/verify_E.py`, about 11 min under heavy load) agrees with the C evaluator at every point it covers:

| (E, X1, X2) | exact F* |
| --- | --- |
| (20, 60, 42), the paper point | 43/60 |
| (18, 58, 42) | 43/58 |
| (22, 62, 42) | 31/21 |
| (24, 64, 42) | 64/43 |
| (40, 80, 60) | 11/10 |

**Mechanism at E=24, X1=64, X2=42.** The allocation `(x, y, ce, abdpq)` has profile (64, 64, 44, 44). It is PO and has uncapped ratio `64/43`, hence is fully EFX.

The paper's trade would move to `(x, bce, yp, adq)`. That move needs agent 4 to keep at least 44, but `adq` is worth only 42 to her.

The e-holder's extra value `E - w` unbalances the two unlucky agents, so the value-neutral swap "large good ↔ three favourites" no longer covers both of them.

**Conclusion of Experiment 2.** The best result on the *tested grid* occurs at the published point. Raising E disrupted a particular Pareto-improving trade. The grid does not exclude counterexamples at untested values of E or for other choices of trades.

## Experiment 3 — seeded annealing (bounded, negative)

The runs were stopped after a few minutes each, with machine load around 100–200. Logs are in `breaker/runs/*.jsonl`; only improvements were logged, and no witness lines appeared.

| Runs | Shape / start | Best F* found |
| --- | --- | --- |
| `hunt2` | n=3, m=8–10, random or tiered starts | ≥ 1 |
| `hunt2` | n=4, m=8 | ≥ 1 |
| `hunt2` | n=5, m=9–10, padded Theorem 2 starts | ≥ 1 |
| `hunt2` | n=4, m=9, from Theorem 2 at K=20 and K=40 | no improving move found |
| `hunt3` (two-scale, K=1000) | from Theorem 2 | stayed at 2003/3000 |
| `hunt3` (two-scale, K=1000) | m = 10–11, and n = 5 | ≥ 1 + O(1/K) |
| `hunt.py` | symmetric parameter annealing (sym9/sym10) | only rescaled K, i.e. the trivial 2/3 + 1/K route; superseded |

The attempted moves did not improve the bound; this is not a proof of a strict local minimum. The unsuccessful random starts do not estimate how common counterexamples are.

## Verdict

- **No positive instance with `F* < 2/3` was found.** Nothing here supports "always 2/3", "never below 2/3", or anything else in general.
- Finite observations:
  1. `F* = 2/3 + 1/K` exactly on Theorem 2 for the K values listed above.
  2. There are 252 PO allocations with `alpha >= 2/3` at K=100, including 164 exactly at the endpoint.
  3. The five independently enumerated common-good examples in Experiment 2 contain no endpoint failure.
- **Suggested next step:** try a different pattern of who values which medium goods, in which the large-good recipients compete for several goods that the other agents value very little (but positively). Require explicit whole-good improvements for the fair assignments; do not assume the trade from the original square still works.
  - Test with `evaluate_dfs`, which handles 10–12 goods in milliseconds.
  - Stopping condition: stop if three structurally different incidences all give `F* >= 2/3` on their obstacle sets.
