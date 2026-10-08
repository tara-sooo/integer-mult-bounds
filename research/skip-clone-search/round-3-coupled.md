# Issue #6: two-round coupled paid-clone search

This round keeps the PR #53 producer graph (`3ffd4021995c959ac02d12920e0279ae97dd03c7`) and PR #54 paid-clone rules (`7210de7d0f9ccaeb64c3f60f188419e02be08d95`) pinned by the prior Issue #6 artifacts. It changes 1–3 first-round clone chains, rebuilds each intermediate graph and matching, enumerates second-round provider pairs for the mapped source partitions, reserves their capacities, regenerates complete continuation chains, and replays both rounds. The existing proof files and replay receipt were not edited.

## Reproduction and inputs

- Command: `python research/skip-clone-search/round-3-coupled.py`
- Deterministic key: `issue6-coupled-v1`; cases run in the order `n1` through `n4`, then dimensions 23 and 25, with jobs in baseline JSON order.
- Environment: Python 3.14.6 on Android 15 aarch64; matching profiler uses `CXX` or defaults to `c++`.
- Input SHA-256: `1b4d4e86fe7f9aa9131198679fb2c800860b83617eba2b94877584a0e7538986`
- Run time: 182.762 seconds (about 3m 03s), including the temporary C++ matching profiler build.
- Results and candidate-level hashes: [`round-3-coupled.json`](round-3-coupled.json)
- Reproduction script: [`round-3-coupled.py`](round-3-coupled.py)

The no-change control replays the saved schedule, recomputes the intermediate maximum matching, reproduces the pinned intermediate graph and matching, and returns the same final graph and FAST baseline. The matching is also compared edge-for-edge with the pinned one. The control and all changed candidates enumerated two admissible provider pairs per second-round job; the control retained every pinned pair.

## Neighborhoods and FAST results

Baseline final FAST values are R23=32693, R25=43056, W=159592676, with 253 and 353 clones and rank sums 752951 and 1077600. The saved baseline κ is 141532521/3125000000000; no new κ proof was attempted.

All four candidates rebuilt both rounds. Intermediate values were identical across candidates: R23=32705, R25=43069, W=159643299, with rank sums 753227 and 1077925. “Matching Δ” counts the symmetric difference from the remapped pinned matching at the intermediate graph or from the no-change final matching. These counts show changed matching edges, not changed matching cardinality.

| Case | First-round job indices changed (h=23 / h=25) | Intermediate matching Δ (23 / 25) | Second-round provider pairs changed (23 / 25) | Final matching Δ (23 / 25) | Final W, Δ from baseline |
|---|---:|---:|---:|---:|---:|
| n1: one first job; preserve providers; shortest chain | 0 / 0 | 2 / 2 | 0 / 0 | 6506 / 12012 | 159592676, 0 |
| n2: one last job; alternate last provider pair; longest chain | 240 / 339 | 2 / 2 | 1 / 1 | 6646 / 130 | 159592676, 0 |
| n3: two jobs at thirds; SHA-256 provider/chain choice | 80,160 / 113,226 | 16 / 12 | 8 / 6 | 10796 / 19870 | 159592676, 0 |
| n4: three jobs at quarters; prefer alternate providers; shortest chain | 60,120,180 / 85,170,255 | 28 / 26 | 12 / 13 | 6960 / 12734 | 159592676, 0 |

Every final candidate returned R23=32693, R25=43056, W=159592676, clone counts 253/353, and rank sums 752951/1077600. Provider schedules and matching edges did change, but none increased final matching cardinality or reduced W. The best candidate ties the PR #54 baseline; there is no FAST improvement.

## Checks and scope

- FAST: completed for all four paired h=23/h=25 candidates. Provider capacities were distinct and reserved from matching; source partitions, chronology, core/cover, and actual operand ownership were checked before or during strict replay. The recomputed matching was validated against the changed intermediate graph before rebuilding its continuation schedule.
- Negative controls: stale intermediate matching rejected for not preserving an actual operand; illegal clone move rejected; duplicate matching edge rejected; unpaid provider rejected for already-used capacity.
- FOCUSED: skipped because no final FAST candidate improved the baseline. No physical-word replay, dirty-state replay, fixed-basis profile, exact moment or new κ certificate was generated.
- FULL: skipped. `make verify`, full CRT regeneration, and all-candidate physical-word replay were not run.

The next useful search is to choose first-round edits by matching sensitivity: prioritize clone-chain changes that alter provider neighborhoods or lie on augmenting paths of the intermediate matching, then vary only the affected second-round provider pairs. This round changed many matching edges without changing cardinality, so further blind seed variation is unlikely to help.
