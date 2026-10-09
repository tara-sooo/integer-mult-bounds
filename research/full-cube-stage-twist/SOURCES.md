# Source pins, hashes, and attribution

## Scope and immutable commits

| Material | Exact reference | Use |
|---|---|---|
| Issue scope | [Fork Issue 25](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/25), read locally with `gh issue view` on 2026-10-09 UTC | Defines the one-candidate scope, checks, and backlink rules. |
| Worktree base | Fork `origin/main` at [commit 0605a24](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/0605a24a28836168ad29d6239b46064b892298fc) | Required base of this isolated branch. |
| Preceding result | [Issue 24 result at commit 6cb527a](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/6cb527acd8f96019638bf33f520db333d9b26031) | Read the complete result directory. Its parity-half-cube failure is external only. |
| Three-stage data-cover baseline | [PR 130](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/130), pinned at [commit 6a9970a](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/6a9970a530119174507904e23592fd59ede19a5d) | Signed shears and exact data-frame endpoints. |
| Paired-cube/shared-core baseline | [PR 144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144), pinned at [commit c8b22bc](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/c8b22bc5c10dba497ac25804e27d9647d818e2ff) | Full eight-port cubes, local `B/H/K`, dirty completed cores, and orthogonal stage routing. |
| Completed-core sharing contribution | [PR 128](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/128), commit [530588a](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/530588a019b4a74f09180680c9e3961bf649ec89), as credited by the PR 144 notice | an664's broader completed-core workspace/scratch-sharing principle; acknowledged separately, with no source code, partition, or serialized witness imported. |
| Structural comparison only | [PR 163](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/163), historically pinned at [commit e181379](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/e1813796ef5c3ca38c5dd7b9e8d81b3908ff5997) | Read as a separate modern fused/balanced structure; no values or profile pieces are combined with PR 144. |
| Original Section 4 interchange | [`openai/math` at commit adc7f12](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a), mirrored and hash-pinned by PR 144 | Its full-array `Swap` call ranks over `Q` stay distinct from local scalar operations; this checkpoint does not evaluate a Section 4 profile. |

The pinned PR 130, PR 144, and PR 163 trees were read with `git show` from their immutable commit objects. Hashes below are SHA256 over the complete bytes at those commit/path pairs, even where the content inspection focused on the relevant sections. Issue 24 is likewise read from the pinned commit, not from the current worktree.

## Hashes of inspected Issue 24 result files

All values are SHA256 at commit `6cb527acd8f96019638bf33f520db333d9b26031`.

| File | SHA256 |
|---|---|
| `research/outer-cover-moonshot/BASELINE_MAP.md` | `ddcb9e50d70d79f5a36c172e3de1190838aecd3a17cff02373506f53ed3cc830` |
| `research/outer-cover-moonshot/VARIANT.md` | `78ee908c11b8ac1342afe122df9a5a68b0da3df12e01223470418d98e6a117af` |
| `research/outer-cover-moonshot/IDENTITIES.md` | `fe6b3b1273773fd3d5fbd86e30d07cb5a0fea6907e999c5f1e156f80fe16ebff` |
| `research/outer-cover-moonshot/PAID_LEDGER.md` | `a318c66bb4a373e4adbaeb4076c65db2a1ae12a347261c0cace2baebf2931bde` |
| `research/outer-cover-moonshot/RESULTS.md` | `b553adf46910a16447ace40c32ecfe091e5187761cf579119ddb183d8399979a` |
| `research/outer-cover-moonshot/SOURCES.md` | `4c97340e6e02e740e6f9f99fdc2e2782a9ef0c1385a9544dcd27fd3211d75319` |
| `research/outer-cover-moonshot/check_small.py` | `025e210e154559d90f492ea50d92e6a9bffa0a7922e2d79a46d435fddb3cf9a9` |

The result explicitly records that its even-parity four-port cube had frozen `B_block=I4`, `K=0`, and `K^2 != I`; that failed candidate is not reused here.

## Hashes of inspected PR 130 files

All values are SHA256 at commit `6a9970a530119174507904e23592fd59ede19a5d`.

| File | SHA256 |
|---|---|
| `notes/three-stage-cover-note.tex` | `db8078687825bcd43c6cc2fb69712ebb12840057b77cd5af8f67f53e4ffffa92` |
| `notes/three-stage-cover-assembly.tex` | `ccf34a6d37c4af14bebeab15be50ab204eb1caebe546385520050ec30089441d` |
| `notes/three-stage-cover-complex.tex` | `1c5b638aa9b75365b8addec9c8eeee6bc5e499722901079b94c65fce033fde8a` |
| `notes/three-stage-cover-bit.tex` | `47123a756f823c83a0d48cca2bf5add6472cd88410b13aed345e70c8834fb511` |
| `LICENSE` | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` |
| `NOTICE` | `e891051aa7858815850030c9531a88794ba0f39436fbd03cc0f2607a76da8b74` |

## Hashes of inspected PR 144 files

All values are SHA256 at commit `c8b22bc5c10dba497ac25804e27d9647d818e2ff`.

| File | SHA256 |
|---|---|
| `notes/paired-cube-construction.tex` | `fb478cda034c1934c62230487008c0a753867e1b153b7d0088878d6fa06856b4` |
| `notes/paired-cube-sharing.tex` | `57fd2290d98528bce00f2ed51b1988e917748f43b2ec25acceacaf2beae1d7e2` |
| `notes/paired-cube-assembly.tex` | `45f28775ebf36338df9312957fd09af3c635690acc02ae3d60431ccd16fb46c3` |
| `notes/paired-cube-bit.tex` | `bed3841c349b1b897cab338b9800dc6030afcdcff0bc7cfdb437501e84fdcd19` |
| `LICENSE` | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` |
| `NOTICE` | `f8511476690f8554d2ee37304b34dc7f58e385e4bff77555d5bd895bcda6212e` |
| `upstream/build/sections/04-swap.tex` | `412b170ccaab38dba96e95e3cbfae09f4876a9818f8d278776a746b0f8044906` |
| `upstream/LICENSE` | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` |

## Hashes of inspected PR 163 comparison files

All values are SHA256 at commit `e1813796ef5c3ca38c5dd7b9e8d81b3908ff5997`.

| File | SHA256 |
|---|---|
| `research/paired-cube-balanced-161/README.md` | `d9f3ebd24898b94169ffb9d04de4df5d09c158d104b3d1550c43c05628c19f58` |
| `research/paired-cube-balanced-161/PROOF.md` | `985cefad2e4f532bf1e13424c50f3356d100a114d5e93d601a8adaf23e14bd17` |
| `research/paired-cube-balanced-161/SOURCE.json` | `836e087c0d747ac06256949593eb35c72e6b3db7502683644d77ffac51f53985` |
| `research/paired-cube-balanced-161/NOTICE` | `61c13d602f9f9a6477d84ebd2dd83d6c129c1e63b821a0497cbf88dcd584a5bc` |
| `LICENSE` | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` |

## Attribution, notices, and assistance

The pinned repository roots and the retained original manuscript tree use Apache-2.0; their original `LICENSE` and `NOTICE` files remain the attribution authorities for their own material. The PR 130 three-stage work is credited to icekylinx with substantial OpenAI GPT-6 Astra assistance and Codex integration; its retained inputs include eumemic's PR 117 complex module with its Claude-assistance notice and Zhihao Chen (jacklightChen)'s PR 97 bit word based on Swapnil Jain's witness. The PR 144 paired-cube/shared-core extension is credited to icekylinx with substantial OpenAI GPT-6 Astra assistance and Codex integration. It separately credits an664's PR 128 completed-core workspace/scratch-sharing principle and its reported Codex assistance; this checkpoint imports no PR 128 source code, partition, or serialized witness.

PR 163 is only a structural comparison. Its notice credits Chafik Boukhalfa with substantial OpenAI Codex assistance and retains prior lineage including icekylinx, eumemic, GamingPuzzled (Joel Pulikkan), jamesyc, gupt1156, Abhinav Ramachandran/geckods, jacklightChen (Zhihao Chen), Rohan Arun, and earlier bit-word contributors. No PR 163 source or profile value is transplanted here.

This checkpoint was prepared with substantial OpenAI Codex assistance: source mapping, the candidate's exact definition, checker implementation, mathematical review, and all six markdown files. The checker adapts the prior Issue 24 p=4 verifier and adds the new stage-routing checks; no code from the pinned upstream PR trees, certificate, or serialized witness was imported. This is not an authorship, review, or endorsement claim for the contributors above; their source notices and Apache-2.0 terms remain in force.
