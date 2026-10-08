# Sources, hashes, and attribution

## Pins

- Fork base: `tara-sooo/integer-mult-bounds` `origin/main` at `0605a24a28836168ad29d6239b46064b892298fc`.
- Branch: `issue-18-producer-event-provenance`.
- Task: [redirected Issue 18](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/18).
- Issue 17 audit: fork commit [`8d4fb37796f9eb2badeca1ef0dd1c810ae23245c`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/8d4fb37796f9eb2badeca1ef0dd1c810ae23245c).
- Issue 16 local frame lift: fork commit [`cf0f30e932416a35147ec2e69f28b87a48e18b31`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/cf0f30e932416a35147ec2e69f28b87a48e18b31).
- PR 63 source snapshot: [redirected PR 63](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/63), commit [aa7701b68540b7863d3b66a414e4319915d6282d](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/aa7701b68540b7863d3b66a414e4319915d6282d).
- Section 3-4 manuscript: OpenAI Math commit [adc7f1241b42e322a6451854ab7e4b4c146bf78a](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a).

All SHA-256 values below were computed from the exact pinned Git objects with `git show <commit>:<path> | sha256sum`. The h=23/h=25 gzip hashes identify the frozen words; no word was regenerated or replayed.

## Issue 17 audit files

| File at commit `8d4fb37796f9eb2badeca1ef0dd1c810ae23245c` | SHA-256 |
|---|---|
| `research/global-role-frame-audit/RESULTS.md` | `ec6ad8194b9b82dce37a281aada3629dc7d71820f8b360706d75199a65315ce6` |
| `research/global-role-frame-audit/ROLE_MAP.md` | `7f0f159a0fbdf4986e029fb874e4d1f3d876108ea13326e5127ef1b6ebd804dd` |
| `research/global-role-frame-audit/ENDPOINTS.md` | `28219018338e7161b00ce3a7838db40d8e0863ea2033034262d1bc178bc80e53` |
| `research/global-role-frame-audit/RANK_LEDGER.md` | `fe876f417f7b3cf0dc939fc071868cc13a9bda3c72fe3ad7a0c5aca92791d3e2` |
| `research/global-role-frame-audit/SOURCES.md` | `c02d1c977fdf3df5b4246d1f1e13aef120fa96bc20ebf8ec0dc9d672e4250e11` |

## Issue 16 files

| File at commit `cf0f30e932416a35147ec2e69f28b87a48e18b31` | SHA-256 |
|---|---|
| `research/rational-gate-frame-lift/FRAME_LIFT.md` | `4b360315a0b6e52a415dac4229485a5706e724473c309ae5e9eaa641dc0f6c38` |
| `research/rational-gate-frame-lift/OBLIGATIONS.md` | `bd5af49008e84f91c920f24862c767f375affcd9e016874a7c9b8d448cf6661a` |
| `research/rational-gate-frame-lift/RESULTS.md` | `447add62ad312b14a31dffae187303b2287313b3a33706c4993b24d8152196aa` |
| `research/rational-gate-frame-lift/SOURCES.md` | `f13765f899e33e8164568bb38ae82aeaca7d8a7ff0ad4dd216872952d0fbb90d` |
| `research/rational-gate-frame-lift/check_local.py` | `3c3debb4e835e86deb4e63bd54813e996bb8a9c4790acacbe56b9c163a31a311` |

## Frozen PR 63 source files

| File | SHA-256 | Relevance |
|---|---|---|
| `research/pair-assembly/pair_graph.py` | `3d47e89d2649c90800a276bdd0480131def50e0bdf92c122a19494b55bf17420` | Logical DAG, selected nodes, and source operand occurrences. |
| `research/pair-assembly/original_timeline.py` | `cf152459e080f556931122bc0afa3417835ea4a6d14e541be12c67f317e25f60` | Independent logical role timeline and rational envelopes; not the rank-first word slot map. |
| `research/pair-assembly/audit.py` | `dd369a7a6e0be4354c05560d0e1d9750c14839928459f43beeb55970f86e0631` | Exact envelope projector formula and checks. |
| `research/pair-assembly/producer-receipt.json` | `14873273bddb9aa08f695f9b9b9de3ccd7dfcf940fb396652e863ba31eb9864bb7` | Producer/timeline counts and receipt. |
| `research/pair-assembly/PROOF.md` | `30685624bf922bb9d9f7ed4b0d367a660fe373cc9ee28fec33585bd8c7023e75` | Graph inheritance, carrier links, physical timeline, and source attribution. |
| `research/rank-pair/PROOF.md` | `b61b3cd554114f6eff6747133a980ac6525d1e2cdf0607056bf421dd331a261c` | Rank-first compiler lineage and complete paid-profile boundary. |
| `research/rank-pair/frame_compile.py` | `c5d11d944d8c6195d7b03efe5adfdde9d1ae508956fa9287b4ca9d3c7de7b750` | Hash-pinned driver; compiles full h=23/h=25 axes. |
| `scripts/experiments/rank_pair_compiler.py` | `9984aaccf880e4840402322d76678bfddb33ce7e494af78430a43429f51b85fd` | Block grouping, matching, carrier/slot allocation, XOR/raise/clear emission. Unmodified. |
| `research/rank-pair/frame-compiler.json` | `e34d155e32b03451d3fd5b39fc39b0aefcf09bc2a8e803ab9cacf21c91ee6ba1` | Frozen aggregate compiler and orientation receipt. |
| `research/rank-pair/frame-word-23.json.gz` | `1a57c143380a063211653f1f35e7cc9710539523b0b34c90f354a0425c34bd59` | Frozen h=23 word; hash checked, not regenerated or replayed. |
| `research/rank-pair/frame-word-25.json.gz` | `fff17e3f6742e0810247747c3bbf393eb6b1b2b5a6c9887c83adeecd298d1bfe` | Frozen h=25 word; hash checked, not regenerated or replayed. |
| `research/rank-pair/screen.py` | `507f709e9e3a8781a2efaf6b4e31f936b9b9ba26d25dae9a24b9f51717b09b7c` | Replays words and reconstructs aggregate paid profiles. Not run. |
| `research/rank-pair/screen-certificate.json` | `4aea9e9a2610f26f28872e2918c94c402bc93aa2203796af77021982e9120d8e` | Frozen aggregate rank total, deficit, and child multiplicities. |
| `research/pair-assembly/frame/frame_verify.py` | `fafe25d57166a747eeb847444a2e02dd7eed19038b93a2c495014d147d04a8fb` | Inherited rational-frame/profile constructor and replay protocol. |
| `upstream/build/sections/03-motifs.tex` | `ed76761194988a01af77ead0ea6469cb5dcd29690ab985a0b5a4006b0f2b69bb` | Common-frame identity, role map, and rational matrix interface. |
| `upstream/build/sections/04-swap.tex` | `412b170ccaab38dba96e95e3cbfae09f4876a9818f8d278776a746b0f8044906` | Rational edge ranks and paid `Swap` recursion. |

## Attribution and license

The pair-assembly graph is credited in its pinned proof to Avi Eisenberg with Claude assistance. The unchanged rank-first compiler derives from Chafik Boukhalfa's PR 60 and eumemic's PR 57 work. The PR 63 composition is credited there to Dominik Scholz with substantial OpenAI GPT-6 Astra assistance; the inherited sources retain the earlier contributor credits. The Section 3-4 manuscript is attributed to OpenAI. This pilot copies no frozen source code and leaves the repository's Apache-2.0 license and inherited notices applicable.

Prepared with substantial OpenAI Codex assistance.
