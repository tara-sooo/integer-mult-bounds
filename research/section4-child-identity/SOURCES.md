# Sources, hashes, and attribution

Issue scope: [fork Issue #23](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/23). Immediate predecessor: [fork Issue #22](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/22), result commit [`a59478900d41aaac56f2a1f9418440cf5a49a47d`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/a59478900d41aaac56f2a1f9418440cf5a49a47d).

The [Issue #22](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/22) result and boundary were read from that immutable commit:
`RESULTS.md` SHA-256 `6b9593d3c6f062fa90495720f14d76737a0c526d3db12f808c490e3ea617b494`,
`CORE_CONTRACT.md` `074c67255dae16db3f74a64e35f9ca18d1b31e442cdae94602a8ec95a6493d75`,
`WHAT_IS_SHARED.md` `29f7ef0f9794417a173d9ce67af62dd1677736875f4033f158d9c94bdd18c09d`,
`COST_BOUNDARY.md` `bd729018827c1d176e329dc2afd8496d309aa3e0f981a903a94d723e66c9b4a1`,
and `RESEARCH_DIRECTIONS.md` `3db4fe5e4d51d0a586ad4a553fcc35dce3b17dbef227543a1577afe66e922c95`.
Its bounded exact checker `check_small.py` (`c2232231855ed976c44538c27e4c5bf25ee005cc74fd7c305f7dc88d0a663f32`)
was rerun read-only and passed.

## Frozen mathematical sources

| Source | Immutable pin | Files used |
|---|---|---|
| Original manuscript, Sections 3 and 4 | [`openai/math` commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a), also pinned in this fork's `upstream/manifest.json` | `upstream/build/sections/03-motifs.tex` SHA-256 `ed76761194988a01af77ead0ea6469cb5dcd29690ab985a0b5a4006b0f2b69bb`; `upstream/build/sections/04-swap.tex` SHA-256 `412b170ccaab38dba96e95e3cbfae09f4876a9818f8d278776a746b0f8044906`. Section 3 defines the selected role/gate matrices; Section 4 defines the exact factorization and pivot-call rule. |
| Upstream PR 128, completed-core sharing | [PR #128](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/128), commit `530588a019b4a74f09180680c9e3961bf649ec89` | `research/completed-core-sharing/PROOF.md` SHA-256 `24eb6d03e32b5322e4e86bde521dc8d32a11bf33f72e806eba985ba47ce05fb0`; reviewed as a distinct completed-core workspace proof, not a Section 4 call ledger. |
| Upstream PR 130, three-stage data cover | [PR #130](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/130), commit `6a9970a530119174507904e23592fd59ede19a5d` | `notes/three-stage-cover-bit.tex` SHA-256 `47123a756f823c83a0d48cca2bf5add6472cd88410b13aed345e70c8834fb511`; `notes/three-stage-cover-rows.tex` SHA-256 `6ad97a5cd7d6aecf978a81226e1c2763d37840caca130c61f3bf5c4ac111c5c8`. Reviewed as an outer data-incidence change. |
| Upstream PR 144, paired cubes and shared bank | [PR #144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144), commit `c8b22bc5c10dba497ac25804e27d9647d818e2ff` | `notes/paired-cube-bit.tex` SHA-256 `bed3841c349b1b897cab338b9800dc6030afcdcff0bc7cfdb437501e84fdcd19`; `certificates/paired-cube-bit-input.json` SHA-256 `23461b66f3a87d4dc87ef209105df4de41d2ef076568ff29b9ea0a0747f01d96`; `references/partial-gauge/pr97/SOURCE.json` SHA-256 `68fb539abcd6df21d142e4e204b6e9482eb7f9cd3907650f54bd058070266596`; `references/partial-gauge/pr97/round7_literal_frame_ledger.py` SHA-256 `02617ba608f971e3bdd2b45d4cbfc3d0d629873a0b9f7c22b12f347d099fdb59`. Reviewed first; no map from its selected bit records to the original Section 4 `M_v` edge/pivot records was found. |

The [PR #128](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/128),
[PR #130](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/130), and
[PR #144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144) immutable commits and their role distinctions match the
[Issue #22](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/22) source map. All GitHub Issue, PR, and commit links in this report
use `redirect.github.com`.

The hashes above are the exact blobs read with `git show COMMIT:path | sha256sum`.
The source pins and original `SOURCES.json`/`NOTICE` files are unmodified.

## Attribution and limits

The original Section 3/4 construction is credited to the authors of the
pinned `openai/math` manuscript; its source license and notices remain in the
fork's `upstream/` snapshot. The [PR #128](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/128) completed-core sharing contribution
is credited to Andrey Mas (`an664`) and its recorded Codex assistance. The
[PR #130](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/130) and
[PR #144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144) contributions are credited to icekylinx, with the substantial GPT-6
Astra assistance and Codex integration/review disclosures retained in those
pinned files. The [PR #144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144) bit supplier derives from Zhihao Chen's [PR #97](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/97) word
and Swapnil Jain's underlying witness; its source notices remain unmodified.
This Issue's notes and checker were prepared with OpenAI Codex assistance. No
pinned upstream source, license, or notice was changed.

The exact edge factorization here is newly written from the manuscript's
rational projector formulas. It is not copied from a PR source and does not
claim authorship or priority for the original construction.

This Issue's exact compact verifier,
`research/section4-child-identity/check_small.py`, has SHA-256
`344a15dd1e3396a460a0465fdef1422c299562acac1faf8889c3fe8f29fe656d`.
