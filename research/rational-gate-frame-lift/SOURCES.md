# Frozen sources and attribution

This checkpoint is based on the user's fork `main` at `0605a24a28836168ad29d6239b46064b892298fc`, on branch `issue-16-rational-gate-frame-lift`. It reads earlier work from immutable commits; no earlier worktree or branch was modified. External Issue and PR links use GitHub's redirect host.

## Issue 13–15 results read

| Snapshot | Immutable fork commit | Source ledger read | SHA-256 |
|---|---|---|---|
| [Issue 13](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/26ff3802cfa1b4b6ee081703509c394fa71526a0) | `26ff3802cfa1b4b6ee081703509c394fa71526a0` | `research/typed-frame-interface/SOURCES.md` | `dda9e0ff8e4d61cfa4c5a2831e9d0c152631876e58d15ddd030618e8a62e46f9` |
| [Issue 14](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/f772133f2b9e1a6a92bcd55ea5984824f7f79f1a) | `f772133f2b9e1a6a92bcd55ea5984824f7f79f1a` | `research/typed-call-boundary/SOURCES.md` | `d6bdfd3fcf751288e6583f2fbaa6af1b3be403a20c50612d1daab9806852c68a` |
| [Issue 15](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/439d9ed592a0dad93700ceccc70925b6f7f49c80) | `439d9ed592a0dad93700ceccc70925b6f7f49c80` | `research/producer-swap-bridge/SOURCES.md` | `bb75f5890fc041e1b9f1635cbeaa9756745d978e2f341e3dc6ae4291f3c13d6a` |

The three focused predecessor checks were rerun read-only from their existing worktrees; all passed. Issue 15's exact physical-word locator gap remains applicable.

## Frozen PR 63 source

The selected source is [CrocSwap commit `aa7701b68540b7863d3b66a414e4319915d6282d`](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/aa7701b68540b7863d3b66a414e4319915d6282d), the construction pinned by [PR 63](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/63). Hashes are SHA-256 of the exact file bytes at that commit.

| File | SHA-256 | Use |
|---|---|---|
| `research/pair-assembly/pair_graph.py` | `3d47e89d2649c90800a276bdd0480131def50e0bdf92c122a19494b55bf17420` | Source DAG and named `FSa`, `Y2`, and consumer expressions. |
| `research/pair-assembly/original_timeline.py` | `cf152459e080f556931122bc0afa3417835ea4a6d14e541be12c67f317e25f60` | Exact rational envelope bases, containment, and a source-ID-preserving independent role timeline. Same bytes at PR 62. |
| `research/pair-assembly/audit.py` | `dd369a7a6e0be4354c05560d0e1d9750c14839928459f43beeb55970f86e0631` | Exact rational projector formula and envelope checks. Same bytes at PR 62. |
| `research/pair-assembly/producer-receipt.json` | `14873273bddb9aa08f695f9b9b9de3ccd7df940fb396652e863ba31eb9864bb7` | Pinned h=23/h=25 rational-timeline and full-dirty-basis receipts. |
| `research/pair-assembly/PROOF.md` | `30685624bf922bb9d9f7ed4b0d367a660fe373cc9ee28fec33585bd8c7023e75` | PR 62 graph inheritance, mechanism, limits, and source attribution. |
| `research/rank-pair/PROOF.md` | `b61b3cd554114f6eff6747133a980ac6525d1e2cdf0607056bf421dd331a261c` | PR 62/60/57 compiler lineage and whole-profile limits. |
| `research/rank-pair/frame_compile.py` | `c5d11d944d8c6195d7b03efe5adfdde9d1ae508956fa9287b4ca9d3c7de7b750` | Compiler inputs and frozen source hashes. |
| `research/rank-pair/frame-compiler.json` | `e34d155e32b03451d3fd5b39fc39b0aefcf09bc2a8e803ab9cacf21c91ee6ba1` | Aggregate compiled role/profile record. |
| `research/pair-assembly/frame/frame_verify.py` | `fafe25d57166a747eeb847444a2e02dd7eed19038b93a2c495014d147d04a8fb` | Aggregate moment and child-width construction. |
| `scripts/experiments/rank_pair_compiler.py` | `9984aaccf880e4840402322d76678bfddb33ce7e494af78430a43429f51b85fd` | Frozen PR 60 rank-first compiler used by PR 63. |

The logical node IDs in `FRAME_LIFT.md` were obtained by generating only `pair_graph.graph(23)` from this pinned source and its local dependencies. No PR 63 frame compiler or serializer was run.

## PR 62 / PR 60 / PR 57 lineage

- [PR 62 source commit `ad0f25ff7b23cff7f08ad237c2254e6ecf74257e`](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/ad0f25ff7b23cff7f08ad237c2254e6ecf74257e) contains the same `original_timeline.py` and `audit.py` hashes above. This is where the core/cover rational-envelope interpretation is directly available.
- PR 63's `research/rank-pair/PROOF.md` names PR 60 commit `e7a492dd8bee4e6f574ced784a62af2ce735edc4` as the source of its unchanged rank-first compiler. This checkpoint uses the exact PR 63 compiler hash above; the PR 60 role/compiler lineage is not itself a rational projection proof.
- [PR 57 compiler snapshot `b7997845f985432e8f14395ee46de80ad3d7ceaa`](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/b7997845f985432e8f14395ee46de80ad3d7ceaa) records eumemic's joint reversible frame compiler. `scripts/experiments/binary_frame_compiler.py` at that commit has SHA-256 `bc6910c8bbe8224285164323d3c06e9035ad3eaa55416abc2867ae0066454a0c`.

The rational lift comes from the original-envelope basis/projector sources, not from interpreting PR 57's binary `(core,cover)` block key as a matrix by itself.

## Original Section 3–4 source

The manuscript is pinned to OpenAI Math commit [`adc7f1241b42e322a6451854ab7e4b4c146bf78a`](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a). These exact local files match the inherited Issue 14 hash ledger:

| File | SHA-256 | Use |
|---|---|---|
| `upstream/build/sections/03-motifs.tex` | `ed76761194988a01af77ead0ea6469cb5dcd29690ab985a0b5a4006b0f2b69bb` | Common-frame identity, rational projection assignment, and endpoint conditions. |
| `upstream/build/sections/04-swap.tex` | `412b170ccaab38dba96e95e3cbfae09f4876a9818f8d278776a746b0f8044906` | Rational edge ranks, pivot factorization, role-permutation contract, and paid recursive call. |

## Credit and license

The original manuscript identifies OpenAI as its author and retains Apache-2.0 in `upstream/LICENSE`. PR 63 retains the repository Apache-2.0 license and its original notices. Relevant inherited credits include Avi Eisenberg and Claude assistance for the PR 62 pair graph; Chafik Boukhalfa for PR 60; eumemic and OpenAI Codex assistance for PR 57; and Dominik Scholz with substantial OpenAI GPT-6 Astra assistance for the PR 63 composition. `original_timeline.py` retains its RaD / hipotures PR 41 lineage. This checkpoint copies no upstream source code; the new exact checker and notes were prepared with OpenAI Codex assistance.
