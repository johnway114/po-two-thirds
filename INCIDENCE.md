# Rewiring the five medium goods: only the published square loses full EFX

**Result.** In the three families below, for every real K≥6, either there is a fully EFX allocation that maximizes total utility, or the valuation matrix is the published square with the medium goods relabelled. In the latter case the best factor with integral Pareto efficiency is exactly `2/3 + 1/K`. Thus no matrix here breaks the two-thirds guarantee. This is a classification of these families, not of positive additive valuations in general.

## What changed and what stayed fixed

Keep four agents, two large goods `x,y`, five labelled medium goods `a,b,c,d,e`, and two small goods `p,q`. Agents 1 and 3 value `x,y` at `(3K,2K+2)` and `p,q` at `(2,1)`; agents 2 and 4 reverse both pairs. Each person prizes exactly **three** medium goods at K and values the other two at 1. Only **which three** changes. The signature lists the numbers of people who prize each medium good, sorted. We tested four pairs plus a common good; three pairs plus two triples; and one single-agent good, one pair and three triples. The first two signatures exhaust the case where every medium good is prized by at least two people: twelve high valuations must be spread over five columns, each with at least two.

| Signature | Labelled matrices | Full EFX at maximum total utility | Relabellings of the published square |
|---|---:|---:|---:|
| 2,2,2,2,4 | 450 | 330 | 120 |
| 2,2,2,3,3 | 2,040 | 2,040 | 0 |
| 1,2,3,3,3 | 2,160 | 2,160 | 0 |

Counts treat people and medium goods as labelled. They are not probabilities about real preferences. The claims about fairness hold on a continuous parameter range, not just at the K used to discover the witnesses.

## Why a pair of people can settle the whole allocation

Choose one person who favors `x` and one who favors `y`. If between them they prize all five medium goods, their two sets of three favorites overlap in exactly one good. Give the first person all three of their favorites and `p`, and the second person their two exclusive favorites and `q`. Give `x` and `y` as singletons to the two remaining people who favor them.

Every good went to someone who values it most, so the allocation maximizes total utility and is Pareto optimal. It is fully EFX as well:

- Each singleton holder gets 3K. A rival has at most four goods worth at most K each to the observer, so after deleting any good the remainder is worth at most 3K.
- The three-medium holder gets 3K+2 and cannot envy the other medium bundle after one removal: at most two goods remain, each worth at most K. A trimmed singleton is empty.
- The two-medium holder gets 2K+2. They prize only one of the other person's three medium goods, and value that person's small good at 1. Even the *untrimmed* bundle is worth only K+3 to them.

These checks need only K≥2. The classification uses K≥6 to invoke the exact result for the one exceptional matrix. Maximizing total utility is stronger than the PO requirement here; we do not assume it suffices on arbitrary inputs.

## Why only the original square escapes this construction

There are four ways to choose one person from each of the two large-good camps. A medium good **blocks** a pair if neither person prizes it. If `u` people from the first camp and `v` from the second do not prize a good, it blocks `uv` pairs. A good prized by one, two, three or four people can therefore block at most **2, 1, 0 or 0** pairs respectively.

For `2,2,2,3,3` and `1,2,3,3,3` the sum of these bounds is only three. At least one of the four pairs is unblocked and the construction works. For `2,2,2,2,4` the sum is four. To block every pair, each of the four pair goods must block a **different** mixed pair. Its two high valuers are the complementary mixed pair. The four high-valuer sets must therefore be precisely `{1,2}`, `{1,4}`, `{3,2}`, `{3,4}`, each once, and the fifth good is common. This is the published square. There are exactly `5! = 120` ways to label its five distinct columns. Conversely, it blocks all four pairs. Our [previous certificate](FAMILY.md) and [receipt](RECEIPT.json) give its exact optimum and efficient witness, including after relabelling. That factor is strictly between two-thirds and one for K≥6.

## Replay and stop decision

From `econ-research/`:

```sh
PYTHONPATH=econ-lab/src python3 -m econ_lab verify --receipt po-two-thirds/INCIDENCE-RECEIPT.json po-two-thirds/incidence.py
```

[The checker](incidence.py) enumerates all `10^4` choices of three favorites per person and filters by the three signatures. It groups only by permutations of the five medium labels and by agent relabellings that preserve or exchange the two entire camps (exchanging `x,y` and `p,q` in the latter case). The [receipt](INCIDENCE-RECEIPT.json) gives bundles for each of the 14 representatives. In those records bit 0 in a high-valuer mask denotes person 1. For the square the checker requires the actual source matrix and allocation up to a column permutation; for all others it checks every good attains its column maximum. It checks every trimmed-bundle inequality by its **value at 6 and its slope**. Both are exact integers, and each inequality is affine in K. The proof above does not depend on the enumeration for existence.

**Stop this branch.** Testing more assignments or more K values in these three families cannot find an endpoint failure. To revisit the negative direction, change an assumption that the proof uses. For example, with six medium goods and three favorites per person, two sets of three cover everything only if they are disjoint. First check whether *every* mixed pair leaves an uncovered good; otherwise the easy allocation may still work. Lack of a covering pair is a screening condition, not a counterexample. No claim of priority or external review.
