# Frozen source and attribution ledger

## Pins

- Fork base: tara-sooo/integer-mult-bounds main at
  0605a24a28836168ad29d6239b46064b892298fc.
- Issue #17 task:
  [redirected Issue #17](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/17).
- Immediate predecessor: Issue 16 frozen at
  cf0f30e932416a35147ec2e69f28b87a48e18b31,
  [redirected commit](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/cf0f30e932416a35147ec2e69f28b87a48e18b31).
- PR #63 proof snapshot:
  CrocSwap/integer-mult-bounds commit
  aa7701b68540b7863d3b66a414e4319915d6282d,
  [redirected PR](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/63),
  [redirected commit](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/aa7701b68540b7863d3b66a414e4319915d6282d).
- Original manuscript:
  openai/math commit adc7f1241b42e322a6451854ab7e4b4c146bf78a,
  [redirected commit](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a).

SHA-256 values below are for exact file bytes at the pinned PR #63 commit.

## Current graph, role compiler and certificate

| Pinned file | SHA-256 | Used for |
|---|---|---|
| research/pair-assembly/PROOF.md | 30685624bf922bb9d9f7ed4b0d367a660fe373cc9ee28fec33585bd8c7023e75 | Current interval-strip/pair graph facts and inherited proof map. |
| research/pair-assembly/pair_graph.py | 3d47e89d2649c90800a276bdd0480131def50e0bdf92c122a19494b55bf17420 | Current logical producer DAG. |
| research/pair-assembly/original_timeline.py | cf152459e080f556931122bc0afa3417835ea4a6d14e541be12c67f317e25f60 | Rational envelope containment, role timeline, terminal uniqueness and bounded dirty checks. |
| research/pair-assembly/audit.py | dd369a7a6e0be4354c05560d0e1d9750c14839928459f43beeb55970f86e0631 | Exact rational envelope projector formula and canonical cases. |
| research/pair-assembly/producer-receipt.json | 14873273bddb9aa08f695f9b9b9de3ccd7dfcf940fb396652e863ba31eb9864bb7 | Existing current graph/timeline receipt. |
| research/rank-pair/PROOF.md | b61b3cd554114f6eff6747133a980ac6525d1e2cdf0607056bf421dd331a261c | PR #60 rank-first method, paid clears, pinned replay/profile scope. |
| research/rank-pair/frame_compile.py | c5d11d944d8c6195d7b03efe5adfdde9d1ae508956fa9287b4ca9d3c7de7b750 | Current pair graph and rank-first word compiler wrapper. |
| scripts/experiments/rank_pair_compiler.py | 9984aaccf880e4840402322d76678bfddb33ce7e494af78430a43429f51b85fd | Physical XOR/frame-group and clear/reuse semantics. |
| research/rank-pair/frame-compiler.json | e34d155e32b03451d3fd5b39fc39b0aefcf09bc2a8e803ab9cacf21c91ee6ba1 | Word/replay hashes and complete-basis receipt for both axes. |
| research/rank-pair/frame-word-23.json.gz | 1a57c143380a063211653f1f35e7cc9710539523b0b34c90f354a0425c34bd59 | Frozen h=23 physical word. |
| research/rank-pair/frame-word-25.json.gz | fff17e3f6742e0810247747c3bbf393eb6b1b2b5a6c9887c83adeecd298d1bfe | Frozen h=25 physical word. |
| research/rank-pair/screen.py | 507f709e9e3a8781a2efaf6b4e31f936b9b9ba26d25dae9a24b9f51717b09b7c | Reconstructs current per-axis word profiles and whole 575 profile. |
| research/rank-pair/screen-certificate.json | 4aea9e9a2610f26f28872e2918c94c402bc93aa2203796af77021982e9120d8e | Current W, m, N, L, rank sum, deficit and full child multiplicities. |
| research/pair-assembly/frame/frame_verify.py | fafe25d57166a747eeb847444a2e02dd7eed19038b93a2c495014d147d04a8fb | Inherited complete profile constructor and frame-word replay protocol. |

## Inherited endpoint and product-basis proof

| Pinned file | SHA-256 | Use and boundary |
|---|---|---|
| research/copied-fixed/PROOF.md | 142326b82ea68e274b3495551b38005b7f1d5e0310219ed10ab5afc8d79a30f8 | Scalar shear/restoration, data-bank exchange, endpoint corrections, exact envelope projectors and product pivot geometry. Its earlier producer counts and W are not reused. |
| notes/copied-centers-bit.tex | ccc8191ddb51698251ed4461a4c26104501b9b2ee37ce3cbe82fa73e85ae40dd | 23/25 product frames, two-stage endpoints and data correction; its old producer count table is not reused. |
| notes/copied-centers-lemma.tex | d0ce6d3d504996aadb098227885224e48df46101daec8893523a0a8b7364d8fe | Copied-center path in both orientations and current generic mass identity. |
| upstream/build/sections/02-streams.tex | 606c80db61cad13aa0c3b6060dc4b88dbbe7ac60cdd831aa93f28d908fd09dab | Role/stream representation. |
| upstream/build/sections/03-motifs.tex | ed76761194988a01af77ead0ea6469cb5dcd29690ab985a0b5a4006b0f2b69bb | Common-frame identity, scalar role permutation, terminal matrices and rational interface. |
| upstream/build/sections/04-swap.tex | 412b170ccaab38dba96e95e3cbfae09f4876a9818f8d278776a746b0f8044906 | Literal rational edge-rank contract and paid interchange theorem. |

## Issue 16 result kept separate

Issue 16's FRAME_LIFT.md, OBLIGATIONS.md, RESULTS.md, SOURCES.md and
check_local.py are read from the immutable fork commit above. Its selected
FSa -> Y2 lift is a local witness only. This audit reran its compact checker
as a FAST local check; it did not use that selected triple line as a global
frame assignment.

## Lineage and attribution

PR #63 pins Avi Eisenberg's pair-assembly graph work with Claude assistance
and composes Chafik Boukhalfa's PR #60 rank-first compiler, derived from
eumemic's PR #57 compiler. The inherited graph/compiler work also retains
Rohan Arun's carrier matching, RaD/hipotures PR #41's independent role
timeline, PR #36's copied-center construction, and the cited contributors
listed in the pinned proofs. The underlying Section 3-4 manuscript is
attributed to OpenAI.

This checkpoint adds documentation only; it copies no source code. The
repository's Apache-2.0 terms and the upstream manuscript/source notices
remain applicable. Prepared with substantial OpenAI Codex assistance.
