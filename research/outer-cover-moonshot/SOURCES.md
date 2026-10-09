# Sources, pins, hashes and credits

## Immutable source pins

| Material | Pinned source | Use |
|---|---|---|
| Issue scope | [Fork Issue 24](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/24), read 2026-10-09 UTC | Deliverables, bounded scope and backlink rules. |
| Prior result | [Fork Issue 23](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/23), `issue-23-section4-child-identity` at [commit](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/267c24dfa448fbf43fa68b7d2cfdd5f9580be458) | Its `NO_IDENTICAL_CHILD_INPUTS_IN_TESTED_SCOPE` is adopted only within its stated tested scope. The pinned `research/section4-child-identity/RESULTS.md` SHA256 is `259cfad0a56d3449fcd5ef667a6984d97df213de501fc11f6f1dcc77a3f37417`. |
| Geometry-first baseline | [Merged three-stage construction](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/130), tree at [commit](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/6a9970a530119174507904e23592fd59ede19a5d) | Three-stage Cayley cover, signed shears, data endpoints and separate bit/complex charges. |
| Paired-cube baseline | [Merged paired-cube construction](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144), tree at [commit](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/c8b22bc5c10dba497ac25804e27d9647d818e2ff) | Canonical local algebra, dirty completed cores, center, shared-bank routing and selected bit/complex suppliers. |
| Structural/accounting comparison | [Balanced construction](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/163), pinned head [commit](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/e1813796ef5c3ca38c5dd7b9e8d81b3908ff5997) | Checklist only; not a profile or theorem imported into either baseline. |
| Original manuscript | [Pinned manuscript tree](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a), `build/sections/04-swap.tex` | Section 4 pivot rank is over `Q`; each matrix-shear pivot pays a full-array `Swap` child. |
| Fork base | `origin/main` at [commit](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/0605a24a28836168ad29d6239b46064b892298fc) | Base of the isolated branch `issue-24-outer-cover-moonshot`. |

The three upstream objects were fetched read-only into the local Git object database and inspected by `git ls-tree` and `git show`. No source baseline was checked out over this worktree or changed. SHA256 values below were calculated from the bytes at the listed immutable commit/path, not from current `main` files.

## Relevant file hashes

All values in this table are SHA256.

### Three-stage baseline

| Immutable file | SHA256 |
|---|---|
| `notes/three-stage-cover-note.tex` | `db8078687825bcd43c6cc2fb69712ebb12840057b77cd5af8f67f53e4ffffa92` |
| `notes/three-stage-cover-assembly.tex` | `ccf34a6d37c4af14bebeab15be50ab204eb1caebe546385520050ec30089441d` |
| `notes/three-stage-cover-complex.tex` | `1c5b638aa9b75365b8addec9c8eeee6bc5e499722901079b94c65fce033fde8a` |
| `notes/three-stage-cover-bit.tex` | `47123a756f823c83a0d48cca2bf5add6472cd88410b13aed345e70c8834fb511` |
| `scripts/three_stage_cover_producer.py` | `ea6dd4f06173304bbcb74b8e5bcc02357b7bb162a6d26b4a6f7a9e886158123f` |
| `scripts/three_stage_cover/verify.py` | `4bd2347e87e4edb699968bc31dfb94f2ab89bf1227576e59f43c779ba74e4e06` |
| `certificates/three-stage-cover-complex-input.json` | `afecf8ce2d8eb259074e61cd0c386b464ca2f57c61b00979eac808fa26e0b770` |
| `certificates/three-stage-cover-bit-input.json` | `d0d496b64d45408d6e0773ebbcd4d5dcca918a596073a51e5fc186b82c3b8520` |
| `upstream/manifest.json` | `16ab13971694cabab09440c47ebf2fc0496a9d35fc3af33950fda3498f8e2392` |
| `upstream/build/sections/04-swap.tex` | `412b170ccaab38dba96e95e3cbfae09f4876a9818f8d278776a746b0f8044906` |
| `LICENSE` | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` |
| `NOTICE` | `e891051aa7858815850030c9531a88794ba0f39436fbd03cc0f2607a76da8b74` |
| `SOURCES.json` | `52aa2871fb4ef6244d9f4ec4c8587cc54d3ef3756a86f1eaff11232c822bda35` |

### Paired-cube baseline

| Immutable file | SHA256 |
|---|---|
| `notes/paired-cube-construction.tex` | `fb478cda034c1934c62230487008c0a753867e1b153b7d0088878d6fa06856b4` |
| `notes/paired-cube-sharing.tex` | `57fd2290d98528bce00f2ed51b1988e917748f43b2ec25acceacaf2beae1d7e2` |
| `notes/paired-cube-bit.tex` | `bed3841c349b1b897cab338b9800dc6030afcdcff0bc7cfdb437501e84fdcd19` |
| `notes/paired-cube-assembly.tex` | `45f28775ebf36338df9312957fd09af3c635690acc02ae3d60431ccd16fb46c3` |
| `scripts/paired_cube_producer.py` | `c84ea3e3ce3eb9563906b6ee4b7411d93dcddfed4bdbc2d4e39936642261cab2` |
| `scripts/paired_cube/graph.py` | `c757d47997f2fa42a95c16f6e6855cf8b125216ae3335b3891e305cf1da82855` |
| `scripts/paired_cube/frames.py` | `7d897418dbfee47de0723ea4983098a982610ccba45e1bac9000a79626d8421c` |
| `scripts/paired_cube/modules.py` | `18a1ad8af0a7832b7c5c4791f5b95f76386cfa7e82ad52bfd2758c081ada68c4` |
| `scripts/paired_cube/gauges.py` | `8a501c66e1330f054e0e11a35e9321d2deea7b51cd03ca56b6a41765e43fe061` |
| `scripts/paired_cube/verify.py` | `e13747916a58b631f10c36eaae230b91b63b427d0a80aa3a530dd9dd90159147` |
| `scripts/paired_cube_bit.py` | `306b3100b97885c0e8b8439a425deac77915d25a7f5bea5bc30d1ee837709efc` |
| `certificates/paired-cube-complex-input.json` | `11894aa8fd4d5e258ec534726eba5fc9c9fa7b826f993e229425c31ee2ad2440` |
| `certificates/paired-cube-bit-input.json` | `23461b66f3a87d4dc87ef209105df4de41d2ef076568ff29b9ea0a0747f01d96` |
| `LICENSE` | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` |
| `NOTICE` | `f8511476690f8554d2ee37304b34dc7f58e385e4bff77555d5bd895bcda6212e` |
| `SOURCES.json` | `6088da7ac41f658dc6b2405467d023fe2263be1a6e48803032144fd5a5a78bf9` |
| `references/three-stage-cover/pr117/NOTICE` | `a0030510cd3b5334fb113eae759aadd2c25951bd353dfb69ad9cb780ae5adf30` |
| `references/partial-gauge/pr97/NOTICE` | `1c53970fb4face631a1b331ec66d33111eccd280a129f9b64c2da6df96861c3f` |

### Balanced structural/accounting comparison

| Immutable file | SHA256 |
|---|---|
| `research/paired-cube-balanced-161/README.md` | `d9f3ebd24898b94169ffb9d04de4df5d09c158d104b3d1550c43c05628c19f58` |
| `research/paired-cube-balanced-161/PROOF.md` | `985cefad2e4f532bf1e13424c50f3356d100a114d5e93d601a8adaf23e14bd17` |
| `research/paired-cube-balanced-161/SOURCE.json` | `836e087c0d747ac06256949593eb35c72e6b3db7502683644d77ffac51f53985` |
| `research/paired-cube-balanced-161/certificate.json` | `5c9aa0ab8c026b39f5bff25a10f8cad69275b91156685fc37eea9f1b4bd13f24` |
| `research/paired-cube-balanced-161/verify.py` | `8d74a52ac7ec7dc4959a98c595a09c936fa147002a4e79bd909fecbd6f048cf0` |
| `research/paired-cube-balanced-161/NOTICE` | `61c13d602f9f9a6477d84ebd2dd83d6c129c1e63b821a0497cbf88dcd584a5bc` |
| `LICENSE` | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` |

The original manuscript manifest already pins `build/sections/04-swap.tex` at SHA256 `412b170ccaab38dba96e95e3cbfae09f4876a9818f8d278776a746b0f8044906`. Its retained upstream license is Apache-2.0.

## Licenses, notices and assistance

The repository source trees use Apache-2.0 at the top level; their original root `LICENSE` and `NOTICE` are retained in the source pins above. The imported [PR 117 module source](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/117) retains its Apache-2.0 notice and Claude-assistance disclosure. The unchanged bit-word lineage is [PR 97](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/97), credited in the pinned notice to Zhihao Chen (jacklightChen) and Swapnil Jain's underlying witness. The paired-cube construction and repository integration credits remain those in the pinned notice: icekylinx with substantial OpenAI GPT-6 Astra assistance and Codex integration; an664 supplied the broader completed-core sharing principle, with its own Codex disclosure, and no source code or serialized witness from that contribution is imported here. The three-stage construction retains its own notice. The balanced comparison is credited in its pinned notice to Chafik Boukhalfa with substantial OpenAI Codex assistance and to its listed retained contributors.

This pilot was prepared with substantial OpenAI Codex assistance: source/proof mapping, candidate selection, exact-checker implementation, mathematical review and all six research documents. The checker and prose here are new work; no upstream source code, certificate or witness was copied into the branch. This disclosure does not claim authorship, review or endorsement by contributors to the pinned baselines. The root license and the original source notices govern their respective material.
