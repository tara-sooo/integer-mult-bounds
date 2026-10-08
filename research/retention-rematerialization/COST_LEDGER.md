# Physical cost ledger

All event and operation indices below refer to the canonical h=23 word with SHA-256 `640696dd7cd893add9d6e12d0d587956fecf113b2eff8c29547b82e5a6f3c0ad`. Exact machine-readable details are in [FOCUSED_RECEIPT.json](FOCUSED_RECEIPT.json).

## Baseline operations and copies

The complete group 1929 operation slice is:

| `ops[]` | Physical XOR `(target, control, group)` | Role in the observed basis/copy sequence |
|---:|---|---|
| 75969 | `(21455,17581,1929)` | Joint output-basis transform |
| 75970 | `(17581,1078,1929)` | Basis transform that uses the temporary `Y2` form |
| 75971 | `(21455,1078,1929)` | Produces the `Y2048` output role |
| 75972 | `(17581,21455,1929)` | Restores slot 17581 to input 1952 |
| 75973 | `(22506,21455,1929)` | Copy for child group 1974 |
| 75974 | `(22507,21455,1929)` | Copy for child group 2066 |
| 75975 | `(22508,21455,1929)` | Copy for child group 2086 |

The first four operations are a joint basis change and restoration; they are not charged solely to one logical value. The last three are the exact outgoing duplicate-use copies. The compiler records 149,172 XORs across the whole word; this local seven-operation slice is included in that total. No local clear XOR is identified in this slice. The Issue 19 compiler receipt's 1,612 whole-word clearing XORs are not apportioned to `Y2048` without a value-specific event.

## Frames, role occupation, and endpoints

The source group 1929 has rank 14. Each destination group has rank 16, and exact rational projector subtraction gives rank 2 for each actual edge. The edge-rank sum is `2+2+2+2=8`; these are four distinct events, not one combined transition.

| Slot | Allocation | Actual outgoing edge(s) | Later frame edge | Retirement endpoint | Role rank mass |
|---:|---:|---|---|---:|---:|
| 21455 | Group 1891, rank 8 | 1891→1929: 6; 1929→1954: 2 | 1954→2139: 2 | Rank 5 | 23 |
| 22506 | Group 1929, rank 14 | 1929→1974: 2 | 1974→2141: 2 | Rank 5 | 23 |
| 22507 | Group 1929, rank 14 | 1929→2066: 2 | 2066→2138: 2 | Rank 5 | 23 |
| 22508 | Group 1929, rank 14 | 1929→2086: 2 | 2086→2141: 2 | Rank 5 | 23 |

Each row's role mass includes its allocation rank, every frame raise, and its retirement cleanup endpoint (`23 − final frame rank = 5`). Same-frame events have rank zero. The four roles contribute 92 rank units in this ledger and are simultaneously occupied at peak. This is part of, not additional to, the full word's 642,620 rank mass across 27,918 roles; the receipt rebuilds the complete histogram from events plus output/retirement endpoints.

## Dirty-state restoration accounting

The exact `ops[75969..75975]` slice passes a selected-block reversible wrapper check in both orientations over 13 basis vectors: 3 source input bits, 4 demanded output bits, and 6 arbitrary dirty role bits. The wrapper applies the seven-operation `M` slice four times (28 XOR gate occurrences, including 12 occurrences of the three copy operations), exposes four carriers with `J` twice (8 XORs), and seeds/restores the three source inputs with `V` twice (6 XORs). The constructed wrapper therefore contains 42 XOR gates total and restores the tested input and dirty-role bits.

Those `J`/`V` operations are wrapper scaffolding, and the 42-gate figure is a checked local wrapper count, not a newly compiled candidate or a saving against the 149,172-XOR baseline. Full h=23 forward/reverse physical-word replay was not run.

## Alternative charges

One-carrier retention across the four child groups is inadmissible because the destination frames are pairwise incomparable. Four separate roles reproduce the existing baseline and its edge, occupation, and endpoint costs. Rematerialization has no source in the checked local inputs or compatible-role spans, so no legal XOR/frame/cleanup schedule can be priced from this evidence. In particular, none of the frame edges or cleanup endpoints is waived in either option.
