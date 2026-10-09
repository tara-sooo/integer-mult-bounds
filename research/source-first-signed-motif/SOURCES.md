# Sources, pins, hashes, and attribution

This bounded report answers [fork Issue 30](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/30), read on 2026-10-09. The branch starts at fork main, [commit 0605a24a28836168ad29d6239b46064b892298fc](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/0605a24a28836168ad29d6239b46064b892298fc).

## Immutable source pins

- Issue 29's signed-address result and exact receipt were read at [commit 69e77d2d32b06b9f5b7e2d27d5946535d4d6f4f5](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/69e77d2d32b06b9f5b7e2d27d5946535d4d6f4f5).
- The original OpenAI manuscript and Sections 3–4 were read at [commit adc7f1241b42e322a6451854ab7e4b4c146bf78a](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a). The 39-character SHA written in the issue is a prefix; this is the full 40-character commit recorded in the frozen upstream manifest.
- PR 130's three-stage cover and bit source were read at [commit 6a9970a530119174507904e23592fd59ede19a5d](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/6a9970a530119174507904e23592fd59ede19a5d).
- PR 144's paired-cube notes and graph source were read at [commit c8b22bc5c10dba497ac25804e27d9647d818e2ff](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/c8b22bc5c10dba497ac25804e27d9647d818e2ff).

Every hash below is SHA-256 of the exact file bytes at the listed immutable pin. No mutable PR head or later p=5 certificate/cost was used.

## Original manuscript at the pinned commit

| File | SHA-256 |
|---|---|
| upstream/manifest.json | 16ab13971694cabab09440c47ebf2fc0496a9d35fc3af33950fda3498f8e2392 |
| build/sections/03-motifs.tex | ed76761194988a01af77ead0ea6469cb5dcd29690ab985a0b5a4006b0f2b69bb |
| build/sections/04-swap.tex | 412b170ccaab38dba96e95e3cbfae09f4876a9818f8d278776a746b0f8044906 |
| LICENSE | c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4 |

The section paths are inside the pinned manuscript subtree preprints/Integer-multiplication-below-n-log-n-September-23-2026/.

## PR 130 source files

| File at the PR 130 pin | SHA-256 |
|---|---|
| notes/three-stage-cover-note.tex | db8078687825bcd43c6cc2fb69712ebb12840057b77cd5af8f67f53e4ffffa92 |
| notes/three-stage-cover-complex.tex | 1c5b638aa9b75365b8addec9c8eeee6bc5e499722901079b94c65fce033fde8a |
| notes/three-stage-cover-bit.tex | 47123a756f823c83a0d48cca2bf5add6472cd88410b13aed345e70c8834fb511 |
| notes/three-stage-cover-assembly.tex | ccf34a6d37c4af14bebeab15be50ab204eb1caebe546385520050ec30089441d |
| notes/three-stage-cover-rows.tex | 6ad97a5cd7d6aecf978a81226e1c2763d37840caca130c61f3bf5c4ac111c5c8 |
| scripts/three_stage_cover/verify.py | 4bd2347e87e4edb699968bc31dfb94f2ab89bf1227576e59f43c779ba74e4e06 |
| docs/three-stage-cover.md | 7ce00f4a423214b96629e1b75f1716bdb66067c97a2f93e5c917e9c3111dd7b7 |
| LICENSE | c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4 |
| NOTICE | e891051aa7858815850030c9531a88794ba0f39436fbd03cc0f2607a76da8b74 |

## PR 144 source files

| File at the PR 144 pin | SHA-256 |
|---|---|
| docs/paired-cube.md | 4fc9c7c73569a5887bedec6e54471b9dde8442fb95e79f9e9f00eef673a9f815 |
| notes/paired-cube-construction.tex | fb478cda034c1934c62230487008c0a753867e1b153b7d0088878d6fa06856b4 |
| notes/paired-cube-sharing.tex | 57fd2290d98528bce00f2ed51b1988e917748f43b2ec25acceacaf2beae1d7e2 |
| notes/paired-cube-assembly.tex | 45f28775ebf36338df9312957fd09af3c635690acc02ae3d60431ccd16fb46c3 |
| notes/paired-cube-bit.tex | bed3841c349b1b897cab338b9800dc6030afcdcff0bc7cfdb437501e84fdcd19 |
| scripts/paired_cube/graph.py | c757d47997f2fa42a95c16f6e6855cf8b125216ae3335b3891e305cf1da82855 |
| LICENSE | c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4 |
| NOTICE | f8511476690f8554d2ee37304b34dc7f58e385e4bff77555d5bd895bcda6212e |

## Issue 29 result files

| File at the Issue 29 commit | SHA-256 |
|---|---|
| research/orthogonal-address-lift/RESULTS.md | 6035c7b209216ae68d4a0b36c66d08d4b3a04da8ac0f8e759e345d8b0d685351 |
| research/orthogonal-address-lift/SOURCE_CAP.md | 5e0d0ddfac0f47b82a645ac30b25ae782e0cef891340e23c40a7b634646d86d1 |
| research/orthogonal-address-lift/COST_DELTA.md | 3d1f6bfa0bff4b3beac530737fee14496b745940d249b6fe50607c211960ba2c |
| research/orthogonal-address-lift/check_small.py | 3f7e3d7aae4af6aec59587b148629ead397f3b55bbb4d43582a7a1ad4eb3a6b4 |
| research/orthogonal-address-lift/receipt.json | 0336cea880cca5eb62b85a173976bbf6c4cb8d5b8d865fee0ba15dbc6d47e594 |

## This package and source credit

| File | SHA-256 |
|---|---|
| check_small.py | 3431d2b71062c1d8601dd257c8ace73518cff9cf562156d0ce529a18ca7c6b36 |
| receipt.json | 513d1e3020cfc500afcc924f472df06b41f4f7cc3d4ee2fff566fc8a9ac18125 |
| Repository LICENSE | c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4 |
| Repository NOTICE | 4cd3cfb404ada8692803f15b33077fca3bb2d684e18bf4593bfd4e3159fa168e |

The original manuscript is credited to OpenAI and its Apache-2.0 license remains in the repository's frozen upstream snapshot. The paired-cube construction and three-stage cover are credited to icekylinx, with the substantial GPT-6 Astra assistance and Codex integration disclosed in their pinned notices. The paired-cube source retains the earlier DAG credit to eumemic and its Claude assistance disclosure; this report does not import that DAG. The separate bit supplier is credited to Zhihao Chen's [PR 97](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/97) and Swapnil Jain's [source commit](https://redirect.github.com/Swapnil-jain/integer-mult-kappa/commit/741e7aa078392553815df7926ee17ac5e25a8c38); this report does not import its code. The original source notices and repository license were left unchanged.

This report and its small checker were prepared with substantial OpenAI Codex assistance. The checker is an independent standard-library implementation of the displayed finite formulas; this does not claim independent mathematical review or OpenAI endorsement. No upstream code or NOTICE text was copied into this package.
