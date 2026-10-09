# Frozen sources

All external GitHub references in this checkpoint use the redirect form
required by [Issue 35](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/35).

| Source | Frozen reference and files used |
|---|---|
| Original manuscript | [`openai/math` commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a), Sections 3 and 4: `preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/03-motifs.tex` (blob `cdb0ba527aa8df5d57c151183fd3893c1a7e21ab`) and `04-swap.tex` (blob `951e792b1768e6509561380b8bbfb1d1ccb64c08`). |
| Prior fork result, [Issue 23](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/23) | Result at [commit `267c24dfa448fbf43fa68b7d2cfdd5f9580be458`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/267c24dfa448fbf43fa68b7d2cfdd5f9580be458); `research/section4-child-identity/{RESULTS,SOURCE_BRIDGE,EQUALITY_TEST,COSTS}.md`. |
| Prior fork result, [Issue 25](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/25) | Result at [commit `520203231ff0de8d9c3121c924ed4fce398c8f69`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/520203231ff0de8d9c3121c924ed4fce398c8f69); `research/full-cube-stage-twist/{RESULTS,CHECKS,TWIST}.md`. |
| Prior fork result, [Issue 30](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/30) | Result at [commit `78f4a20fa1be5fb7366ae93c808a93d191491472`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/78f4a20fa1be5fb7366ae93c808a93d191491472); `research/source-first-signed-motif/{RESULTS,DECODER,SOURCE_INTERFACE}.md`. |
| Paired-cube baseline | [Upstream PR 144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144), commit [`c8b22bc5c10dba497ac25804e27d9647d818e2ff`](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/c8b22bc5c10dba497ac25804e27d9647d818e2ff), `notes/paired-cube-construction.tex` (blob `9dd1f10cb757d87a769266cb3b9a996a6f7a1048`), `notes/paired-cube-sharing.tex` (blob `56e729572d859216b88a275ec53592b65f4ee56b`), and `notes/paired-cube-bit.tex` (blob `dd84535b21923bab388305231f6f4c756aefacd8`). |
| Source-assisted control | [Upstream PR 193](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/193), pinned head [`187e1010ac8b259af8e9b5166f68b64bc27b4b47`](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/187e1010ac8b259af8e9b5166f68b64bc27b4b47), `research/source-assisted-v4/PROOF.md` (blob `f225002bd0d7acf222800dfb01fe84d63893552b`) and `README.md` (blob `014572a29619f82b1c6da06de171cce78286b768`). The proof covers source-controlled parity erasure and donor/recipient flow for its own complex supplier. |
| Paid-data stop control | [Upstream PR 203](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/203), pinned head [`d2873e20750d0949d2ad75cbc4cd82b5b1a74e84`](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/d2873e20750d0949d2ad75cbc4cd82b5b1a74e84), `research/percent-exponent-architecture/PROOF.md` (blob `043bc4af5e103300c6c457791d48cb5a9e7bec3f`), `inputs/complex-pr193.json` (blob `550d0ca928e4f5c3fe207c1ee3a61c26b1e9aef1`), and `inputs/bit-pr187.json` (blob `1a00656788de786852dd46fcc89fa069af114e4e`). |
| Coordinated bank/frame control | [Upstream PR 207](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/207), pinned head [`cd14825023b75af4f5919a30e5e6d548b6ade5bc`](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/cd14825023b75af4f5919a30e5e6d548b6ade5bc), `research/coordinated-crossover-pr200/CROSSOVERS.md` (blob `abb23e7dab9328ec82e1045ddfc80141dc6cdc78`) and `PROOF.md` (blob `7b2fb0db689ba54d28659a3da9a9fd82c53e8d01`). |

## Scope and credit

The local fork results above were read from their immutable commits; they were
not assumed to be present on `origin/main`. The manuscript and upstream PR
files were fetched at the commit pins in this table. No upstream repository
was written to.

The paired-cube source note identifies icekylinx, Apache-2.0, and substantial
GPT-6 Astra and Codex assistance. [PR 193](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/193)
credits the [PR 184](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/184)
method to icekylinx, the [PR 168](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/168)
v4 modules to eumemic, and its package to Avi Eisenberg with Claude
assistance. [PR 207](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/207)
retains the [PR 200](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/200)
bit and [PR 202](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/202)
complex source notices. Those constructions are cited as prior work; no source
code from them is copied here. The new checker and analysis were prepared with
substantial OpenAI Codex assistance under this repository's Apache-2.0
license.
