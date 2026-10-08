# Issue #6 search round 2: FAST record

Date: 2026-10-08 UTC
Branch: `issue-6-paid-clone-search`
Producer and clone criteria: pinned PR 53 commit `3ffd4021995c959ac02d12920e0279ae97dd03c7` and PR 54 commit `7210de7d0f9ccaeb64c3f60f188419e02be08d95`.

This follow-up preserves the producer graph and the paid whole-chain clone invariants. The prior `screening.json` sample used final-round seeds `1`–`8`; this round covers the previously unsearched first clone round and adds final-round seeds `9` and `10`.

## Search conditions

- First clone round: SHA-256 choice seeds `101` and `102`, plus one all-jobs `shortest-chain` strategy. Each choice is selected from the three complete continuation chains returned by the existing chain enumerator.
- Final clone round: new SHA-256 choice seeds `9` and `10`, plus `shortest-chain`.
- Candidate choice hashes include the round, seed, dimension, and job index. The new seed sets do not overlap the previous `1`–`8` sample.
- Every candidate passed `cloned_graph.replay_round` before its matching screen. This checks distinct provider capacity, the exact disjoint source partition, chronology, the original core/cover envelope, complete continuation-chain replacement, source graph pins, and exact scalar outputs. All 12 dimension-specific candidate graphs passed; none was rejected by these invariants.
- FAST comparison uses the existing C++ maximum-cardinality matching screen and its `R` and `rank_sum` outputs. `W` is computed from the h=23 and h=25 `R` values. These values are discovery screens, not exact `kappa` certificates.

## First clone round

The baseline after only the first clone round is `R23=32705`, `R25=43069`, and partial-graph `W=159643299`, with 241 h=23 and 340 h=25 clones. Every tested strategy produced the same screen:

| Strategy | Seed | Changed chains h=23 / h=25 | R23 | R25 | Partial W |
|---|---:|---:|---:|---:|---:|
| SHA-256 choice | 101 | 162 / 226 | 32,705 | 43,069 | 159,643,299 |
| SHA-256 choice | 102 | 155 / 230 | 32,705 | 43,069 | 159,643,299 |
| Shortest chain | — | 92 / 51 | 32,705 | 43,069 | 159,643,299 |

All had `rank_sum=753227` for h=23 and `1077925` for h=25, the same as the baseline first-round graph. These are intermediate graphs only. Because a first-round change invalidates the stored second-round pre-matching, these candidates would need a fresh matching and later clone schedule. They were not extended because none showed an immediate FAST gain; this does not rule out interaction with a rebuilt later round.

## Final clone round

The pinned complete schedule baseline is `R23=32693`, `R25=43056`, and `W=159592676`, with 253 h=23 and 353 h=25 clones. Each new final-round candidate tied it:

| Strategy | Seed | Changed chains h=23 / h=25 | R23 | R25 | W |
|---|---:|---:|---:|---:|---:|
| SHA-256 choice | 9 | 10 / 5 | 32,693 | 43,056 | 159,592,676 |
| SHA-256 choice | 10 | 7 / 10 | 32,693 | 43,056 | 159,592,676 |
| Shortest chain | — | 8 / 3 | 32,693 | 43,056 | 159,592,676 |

The new final candidates each had `rank_sum=752951` for h=23 and `1077600` for h=25. No final candidate improved FAST `W`, so no candidate was promoted to FOCUSED replay. The prior seed-1 candidate remains the only focused candidate; its exact `kappa=141532521/3125000000000` equaled the PR 54 baseline. This round made no new exact `kappa` claim.

## Verification boundary and reproduction

- FAST: complete for the 6 paired strategy/seed variants (12 dimension-specific graphs), including strict clone replay and maximum-matching screens.
- FOCUSED: not run for this round; there was no FAST improvement.
- FULL / `make verify`: not run, as requested.
- The earlier milestone's `replay-receipt.json` preserves the seed-1 exact replay and 11 focused tests.

Reproduce this round with:

```sh
python3 research/skip-clone-search/round-2-fast.py
```

`round-2-fast.json` records per-candidate metrics, graph hashes, comparisons, decisions, pins, and any invariant rejection reasons. This is a bounded negative result; it is neither an exhaustive search nor a global optimality claim.
