# Frozen sources and attribution

This checkpoint starts from fork `main` at
`0605a24a28836168ad29d6239b46064b892298fc` and adds only this research note
and its focused checker. Issue 13 and Issue 14 results are read from their
immutable fork commits; neither predecessor worktree or branch is changed.
External GitHub references use the redirect host as required by Issue 15.

## Predecessor records

| Source | Immutable files used | SHA-256 |
|---|---|---|
| [Issue 13 snapshot](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/26ff3802cfa1b4b6ee081703509c394fa71526a0) | `research/typed-frame-interface/BOUNDARY.md`; `RESULTS.md`; `SOURCES.md`; `check_boundary.py` | `487e7776af7aa42b52224d8ac64a0856a1bddaa654c2537a3a2334aea82574e4`; `095e95970f4654b5047fd1eb5af801bdf80ba3703c81b0b8660edd502afc196c`; `dda9e0ff8e4d61cfa4c5a2831e9d0c152631876e58d15ddd030618e8a62e46f9`; `170cf7c2ad2f500efe30809c7e72f3b7d87bb6363bb68e515dfbe0d5630cbd29` |
| [Issue 14 snapshot](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/f772133f2b9e1a6a92bcd55ea5984824f7f79f1a) | `research/typed-call-boundary/THEOREM_MAP.md`; `CONTRACT.md`; `RESULTS.md`; `SOURCES.md`; `check_call_boundary.py` | `4bea9d522130cae063b442afabbef8cb4fd28a33bee3a449c67df146ee7068d8`; `3d3da4254a97c94d658287d887fd36c2ce063affc75d26c047f98910a37a16e2`; `9ae4cad8302e1fca3b032da4de86a0adffa9f04a46c39004a5fdca05ab9f5783`; `d6bdfd3fcf751288e6583f2fbaa6af1b3be403a20c50612d1daab9806852c68a`; `29053ca65e2983bf2107bf2284dced2c2be3b079a3afe105e4e2d0f2032a8cf8` |

Issue 13 pins the PR 63 construction commit
[`aa7701b68540b7863d3b66a414e4319915d6282d`](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/aa7701b68540b7863d3b66a414e4319915d6282d), linked from [PR 63](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/63).
Its complete source ledger and inherited attribution remain in the frozen
Issue 13 `SOURCES.md`; this checkpoint copies no PR source code.

## Exact files inspected at PR 63 commit

| File | SHA-256 | Use |
|---|---|---|
| `research/pair-assembly/pair_graph.py` | `3d47e89d2649c90800a276bdd0480131def50e0bdf92c122a19494b55bf17420` | Concrete `FSa` and `Y2` producer expressions. |
| `research/pair-assembly/PROOF.md` | `30685624bf922bb9d9f7ed4b0d367a660fe373cc9ee28fec33585bd8c7023e75` | Construction details, inherited limits, and complete contributor credit. |
| `research/rank-pair/frame_compile.py` | `c5d11d944d8c6195d7b03efe5adfdde9d1ae508956fa9287b4ca9d3c7de7b750` | Compiler invocation, source pins, and serialized word creation. |
| `scripts/experiments/rank_pair_compiler.py` | `9984aaccf880e4840402322d76678bfddb33ce7e494af78430a43429f51b85fd` | Block/frame compiler and word serializer. |
| `scripts/experiments/binary_frame_replay.py` | `392e78e62d7685c99a5888a7da743ea6c3dcad631af4a743c91e0c09348442bc` | Independent whole-word replay contract. |
| `research/rank-pair/frame-compiler.json` | `e34d155e32b03451d3fd5b39fc39b0aefcf09bc2a8e803ab9cacf21c91ee6ba1` | Whole-axis role, XOR, rank-mass, and replay records. |
| `research/rank-pair/frame-transitions-23.json` | `e2715ef2ff15abf43ced9a1e1b37fed8383cca9ff3e2ded3260ec5c21bfb88f3` | Aggregate transition counts at `h=23`; no source-edge IDs. |
| `research/rank-pair/frame-profiles-23.json` | `ba810de465295485090c5027bf073cc391e11b36ebf57963adba2e4bc78cfac4` | Aggregate fixed-basis rank histogram at `h=23`. |
| `research/rank-pair/frame-word-23.json.gz` | `1a57c143380a063211653f1f35e7cc9710539523b0b34c90f354a0425c34bd59` | Frozen physical word; its schema is described by the pinned serializer. |
| `research/rank-pair/PROOF.md` | `b61b3cd554114f6eff6747133a980ac6525d1e2cdf0607056bf421dd331a261c` | Rank-first costs, validation limits, and attribution. |

## Original manuscript

The paper is pinned to OpenAI Math commit
[`adc7f1241b42e322a6451854ab7e4b4c146bf78a`](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a).
Issue 14's checked-in hash ledger establishes that the local section files
match that commit. The sections used here are:

| File | SHA-256 | Use |
|---|---|---|
| `upstream/build/sections/02-streams.tex` | `606c80db61cad13aa0c3b6060dc4b88dbbe7ac60cdd831aa93f28d908fd09dab` | Array shape, logical volume, descriptors, and tape operations. |
| `upstream/build/sections/03-motifs.tex` | `ed76761194988a01af77ead0ea6469cb5dcd29690ab985a0b5a4006b0f2b69bb` | Original finite bit network and rational frame interface. |
| `upstream/build/sections/04-swap.tex` | `412b170ccaab38dba96e95e3cbfae09f4876a9818f8d278776a746b0f8044906` | Matrix rank, pivot factorization, `Swap` child, and paid recurrence. |

The PR 63 pair graph retains Avi Eisenberg's and inherited contributors'
notices, including the documented Claude assistance. Its rank-first compiler
retains Chafik Boukhalfa's contribution and its eumemic/OpenAI-assisted PR 57
ancestry; the PR 63 composition records Dominik Scholz and substantial
OpenAI assistance. The frozen source proofs contain the full attribution;
this checkpoint neither changes those files nor makes an independent claim
for their inherited theorem obligations. This note and checker were prepared
with OpenAI Codex assistance.
