# Paid cost comparison

The main comparison is the frozen PR 63 h=23 word versus a complete recompile forcing both legal carry edges for value 62985: group 52185→51875 and group 52187→51855. The pinned graph, compiler, matching/reclaim policy, and terminal set are unchanged.

## Whole-word totals

| Metric | Frozen baseline | Two-edge carry | Change |
|---|---:|---:|---:|
| Physical XORs | 149,172 | 149,167 | −5 |
| Physical roles | 27,918 | 27,920 | +2 |
| Event-plus-endpoint rank mass | 642,620 | 642,666 | +46 |
| Terminal outputs | same | same | 0 |

The baseline canonical word hash is `640696dd7cd893add9d6e12d0d587956fecf113b2eff8c29547b82e5a6f3c0ad`, with deterministic gzip hash `1a57c143380a063211653f1f35e7cc9710539523b0b34c90f354a0425c34bd59`. The alternative is a new word: canonical SHA-256 `efbc7f212f82a660ac9e35125639d848eda8fdb2b521c020af5f5514b77c1ae6`; deterministic gzip SHA-256 `4be13195eba52e1949add16a7345e0d08c44e820ca357022e21efdb1ce879771`.

Both target compiler uses were unmatched in the baseline and matched in the alternative. Each carried event is exact Q23 rank 1. The candidate's producer duplicate-use copies fall from five to three.

## Operation changes

The saved candidate copies do not equal the whole-word XOR change:

| Operation cause | Group | Change in XOR count |
|---|---:|---:|
| Candidate duplicate-use copies | 51779 | −2 |
| Other duplicate-use copies | 17098 and 21996 | +2 total |
| Block synthesis | 52185 and 52187 | −2 total |
| Retired-slot clears for duplicate-use copies | 51779 | −5 |
| Retired-slot clears for duplicate-use copies | 51781 | +2 |

The clear changes net −3; all listed causes sum to the observed −5 physical XORs. Matching at groups 52185 and 52187 also displaces baseline carries for values 19903/use 112285 and 25809/use 112291. The resulting role reuse, extra copies elsewhere, and all downstream operation changes are included in the complete alternative word.

## Rank and endpoint charges

The complete rank histogram was rebuilt from every frame event plus every output or retirement endpoint. Its nonzero delta is:

| Q23 rank bin | Change in count |
|---:|---:|
| 0 | −9 |
| 2 | +2 |
| 5 | +1 |
| 7 | −2 |
| 10 | −3 |
| 15 | +3 |
| 18 | +2 |

The rank mass increases by 46, equal to two additional roles at h=23. This rank profile is a separate measured cost from the five fewer physical XORs. It does not compute a complete child-cost histogram, recurrence moment, or κ. Role lifetimes in the receipt include each tested carrier's full history and its retirement/output endpoint; no frame raise, clear, reconstruction, role occupation, or endpoint is waived.

## PR 74-style reconstruction screen

For value 62985, current other-role fresh forms span the target at all six demand points. The chosen Gaussian witnesses use 5, 6, 5, 5, 5, and 10 roles. An exact subset check finds no one-, two-, or three-carrier representation among the currently eligible retired roles at any demand point. This rejects the direct small-retired-span primitive for this candidate in the current schedule. It does not rule out a schedule that first reserves or changes other roles.

For value 21, no current eligible-role span witness exists at any of its twelve demand points. No h=23 reconstruction schedule was priced because neither focused case produced a small current retired-carrier witness; a new reservation schedule would need to pay its destination role, clears, raises, reservation interval, reconstruction XORs, and endpoints.

The local dirty checks apply each affected block's M sequence and exact inverse to every touched role basis vector. They pass. A full global dirty-basis replay was not run.
