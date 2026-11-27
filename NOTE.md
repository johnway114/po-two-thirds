# The published PO + α-EFX construction is exact at 2/3 + 1/K

**Status.** Computer-checked, unrefereed, not independently reviewed by a human. The unrestricted question remains open.

When indivisible goods are valued positively, can they always be assigned so that the allocation is Pareto optimal and each person values their bundle at least two-thirds as much as any other bundle after any one good is removed (PO + 2/3-EFX)? Mahabadi, Ramakrishnan and Tarnawski ([arXiv:2610.29201v2](https://arxiv.org/abs/2610.29201)) rule out every strictly larger universal factor. Their four-person, nine-good family does not settle equality. This note characterises that family, closes two nearby perturbations and a five-medium-good rewiring class, and records a separate positive result with one surplus good. None of these statements is a general existence or impossibility theorem.

## Results on the source construction

For the paper's four-agent, nine-good table and every real K ≥ 6, the best factor among Pareto-optimal allocations is exactly 2/3 + 1/K, attained by one explicit integral allocation. The paper states the upper bound for integer K; the checker proves both directions on the whole real interval. Of all 262,144 allocations, treated as functions of K, 261,928 have a binding or worse fairness comparison, and each of the remaining 216 admits a fixed integral Pareto improvement. See [FAMILY.md](FAMILY.md) and [RECEIPT.json](RECEIPT.json).

Two routes to a counterexample inside or near that table are closed, for every real K ≥ 6:

- If the rest of the table is held fixed and the four favourite large-good values vary independently through [2K+2, ∞), then whenever even one differs from 3K, there is a fully EFX Pareto-optimal allocation, including ties at the lower endpoint. The efficient allocation can change as an exact trade ceases to be a Pareto improvement.
- If every one of the 36 entries moves independently by an amount of absolute value strictly less than 1/3, at least one allocation remains 2/3-EFX and Pareto optimal. The efficient allocation need not stay the same. An explicit example at radius exactly 1/3 breaks the two-allocation proof used here, not necessarily the guarantee. See [NEIGHBORHOOD.md](NEIGHBORHOOD.md).

## Five-medium-good incidence classification

Changing who prizes which medium goods, while keeping three favourites per person, was classified completely in the signatures 22224, 22233 and 12333. Of 4,650 labelled matrices, 4,530 admit full EFX while assigning every good to a highest valuer. The remaining 120 are the published square with its five medium goods relabelled. The classification covers every such rewiring in which each medium good has at least two high valuers, for every real K ≥ 6. The decisive test is whether one person from each large-good camp together prizes all five medium goods. See [INCIDENCE.md](INCIDENCE.md) and [INCIDENCE-RECEIPT.json](INCIDENCE-RECEIPT.json).

## A positive result outside that construction

For any number of people, if there is exactly one more good than people and nobody ties two individual goods, a fully EFX Pareto-optimal allocation exists. The last two unpicked goods must stay together under any Pareto improvement. Ties between individual goods break this particular argument, not necessarily the existence conclusion. See [POSITIVE.md](POSITIVE.md).

## Archived receipts

Figures below are copied from the receipt files. Both checkers use the Python standard library only, with integer coefficients of inequalities over real intervals, not a grid of floating-point values.

From [RECEIPT.json](RECEIPT.json), produced by `check.py` on 27 November 2026 at 14:10:01 UTC. The script SHA-256 was `14d0cd12f1e1f67da5ed9db82b05410475e219daab70d80ad43b7d9378d0345c`. The run passed with exit code 0 in 1.2841 seconds on Python 3.14.7, platform `macOS-26.5.2-arm64-arm-64bit-Mach-O`. The parsed certificate records:

- centre witness allocation `xb y cdpq ae`, factor `(2K+3)/(3K)`;
- centre upper bound over real K ≥ 6: 262,144 allocations, 261,928 excluded by fairness, 216 excluded by a Pareto improvement, 16 fixed improvements;
- exclusive tube radius `1/3`; 255 off-centre cells certified.

From [INCIDENCE-RECEIPT.json](INCIDENCE-RECEIPT.json), produced by `incidence.py` on 27 November 2026 at 14:19:58 UTC. The script SHA-256 was `96f8db5f201bce81d74ff78ec71fc3da4c7f8e8a153c7adfd6177022944ae476`. The run passed with exit code 0 in 0.0571 seconds on the same platform. Parsed output: 10,000 row choices examined, 4,650 in scope, 14 orbits, and class counts `12333_full` 2160, `22224_full` 330, `22224_square` 120, `22233_full` 2040.

## How to reproduce

From this directory (Python 3.10 or later; only the standard library):

```sh
python3 check.py
python3 incidence.py
```

Alternatively, from the parent `econ-research/` directory if `econ-lab` is present: `PYTHONPATH=econ-lab/src python3 -m econ_lab verify po-two-thirds/check.py`.

## Limitations and risks

- The general PO + 2/3-EFX question is still open. A complete analysis of the published family, and of some nearby and incidence variants, is not a universal guarantee or a counterexample.
- Coverage is complete over the displayed parameter domains, not over arbitrary positive additive matrices.
- The neighbourhood argument uses an exclusive radius of 1/3 and two weak improvers; it does not claim the largest possible radius.
- The one-surplus theorem requires strict rankings of individual goods and at most one extra good. It is not a characterisation of all feasible instances.
- These are computer-checked written proofs, not formalisations in a theorem prover. Internal AI-assisted audits recorded in [AUDIT.md](AUDIT.md) are not outside confirmation. The literature check in [SOURCES.md](SOURCES.md) is bounded and is not a priority certificate.

## Credit

The source construction and the exclusion of every factor strictly above two-thirds belong to Mahabadi, Ramakrishnan and Tarnawski. Local research, code and audit used an OpenAI GPT-6.2 Astra (Codex) lead, with configured Claude research and audit roles, as recorded in the project ledger and session. Computational independence here means separate implementations and contexts, not outside human review.

## References

- Mahabadi, Ramakrishnan and Tarnawski, [arXiv:2610.29201v2](https://arxiv.org/abs/2610.29201).
