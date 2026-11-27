# A04 — Can two-thirds fairness coexist with efficiency?

**The unrestricted question remains open in the sources checked.** When goods are indivisible and everyone values every good positively, can we always allocate them so that nobody can be made better off without hurting someone, and everyone values their share at least two-thirds as much as any other share after *any* one good is removed? [Definitions and sources](SOURCES.md).

A short unrefereed research note, with the archived receipts, reproduction instructions and limitations, is in [NOTE.md](NOTE.md).

[Mahabadi, Ramakrishnan and Tarnawski](https://arxiv.org/pdf/2610.29201v2) constructed a family that rules out every larger universal factor. We found where that construction stops and which changes cannot push it further:

| Valuations (four agents, nine goods) | Supported conclusion |
|---|---|
| Original §4 table, real K≥6 | The best factor among Pareto-optimal allocations is **exactly 2/3 + 1/K**. A single explicit allocation attains it. The paper states the upper bound for integer K; the checker proves both directions on the whole real interval. |
| Keep the table except for the four favorite large values; vary each independently from 2K+2 to infinity, real K≥6 | If even one differs from 3K, an allocation satisfies **full EFX** and is Pareto optimal. This includes ties at the lower endpoint. |
| Start at the original table and change **all 36 entries** independently by amounts of absolute value **less than 1/3**, real K≥6 | At least one allocation is **2/3-EFX and Pareto optimal**. The efficient allocation need not stay the same after perturbation. |

**Changing who prizes the medium goods:** [classification and construction](INCIDENCE.md). Across 4,650 labelled rewirings with three favorites per person, 4,530 admit full EFX while assigning *every* good to a highest valuer. The remaining 120 are just the original square with its five medium goods relabelled. The classification includes every rewiring in which all five medium goods are contested by at least two high valuers. [Witness receipt](INCIDENCE-RECEIPT.json).

[Proof of the exact factor and the four-value result](FAMILY.md) · [Proof of the all-entry neighborhood](NEIGHBORHOOD.md) · [Research ledger and next experiment](STATE.md) · [Audit](AUDIT.md).

**A positive result beyond that construction:** for any number of people, if there is exactly one more good than people and nobody ties two individual goods, a fully EFX, Pareto-optimal allocation exists. The proof uses a picking order and shows why the last pair of goods must stay together under every Pareto improvement. [Proof, tie obstruction, and a separate bounded-disagreement guarantee](POSITIVE.md).

## Exact replay

From `econ-research/`, run:

```sh
PYTHONPATH=econ-lab/src python3 -m econ_lab verify po-two-thirds/check.py
```

Only the Python standard library is needed. The [checker](check.py) works with integer coefficients of inequalities over real intervals, not a grid of floating-point values. It enumerates whole-good reassignments, including empty bundles, and records a witness for each of 255 off-center cases in [RECEIPT.json](RECEIPT.json). Its upper-bound check independently covers all 262,144 center assignments for the entire parameter range. These are local, unrefereed results, not a claim of priority or outside confirmation.

Credit: source construction and the exclusion of every factor strictly above two-thirds belong to the cited authors. Local research, code and audit used an OpenAI GPT-6.2 Astra (Codex) lead, with configured Claude research and audit roles. This repository accompanies the unrefereed note [NOTE.md](NOTE.md).
