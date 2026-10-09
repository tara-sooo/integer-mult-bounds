# Sources, pins, hashes and attribution

All source snapshots below are pinned by exact commit. Issue, PR, and commit
links use the redirect form. No current upstream HEAD was substituted.

## Read-only research inputs

- Full request and exit taxonomy: [fork Issue 28](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/28).
- Prior result: [fork Issue 27 artifacts at commit `91661785056376ecafebf8e00b0ebd7226cd23a0`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/91661785056376ecafebf8e00b0ebd7226cd23a0), read-only.
- Paired-cube source: [upstream PR 144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144), frozen merge [commit `c8b22bc5c10dba497ac25804e27d9647d818e2ff`](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/c8b22bc5c10dba497ac25804e27d9647d818e2ff).
- Three-stage and paid frame source: [upstream PR 130](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/130), frozen merge [commit `6a9970a530119174507904e23592fd59ede19a5d`](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/6a9970a530119174507904e23592fd59ede19a5d).
- Original manuscript, Sections 3–4: [OpenAI math commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a). The exact PDF and section source files were read at this commit.
- Issue 24 comparison verifier: [fork commit `6cb527acd8f96019638bf33f520db333d9b26031`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/6cb527acd8f96019638bf33f520db333d9b26031), read-only; its verifier was inspected but not run.

## SHA-256 file pins

Hashes are over exact file bytes at the stated commit.

| Source snapshot | File | SHA-256 |
|---|---|---|
| PR 144 | `scripts/paired_cube/graph.py` | `c757d47997f2fa42a95c16f6e6855cf8b125216ae3335b3891e305cf1da82855` |
| PR 144 | `scripts/paired_cube/frames.py` | `7d897418dbfee47de0723ea4983098a982610ccba45e1bac9000a79626d8421c` |
| PR 144 | `notes/paired-cube-construction.tex` | `fb478cda034c1934c62230487008c0a753867e1b153b7d0088878d6fa06856b4` |
| PR 144 | `notes/paired-cube-bit.tex` | `bed3841c349b1b897cab338b9800dc6030afcdcff0bc7cfdb437501e84fdcd19` |
| PR 144 | `LICENSE` | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` |
| PR 144 | `NOTICE` | `f8511476690f8554d2ee37304b34dc7f58e385e4bff77555d5bd895bcda6212e` |
| PR 130 | `notes/three-stage-cover-assembly.tex` | `ccf34a6d37c4af14bebeab15be50ab204eb1caebe546385520050ec30089441d` |
| PR 130 | `notes/general-clifford-frames.tex` | `c9bb9655b594583c6b4bab8cb485233f1d1e588f83858cf1e4c3530cee8fed54` |
| PR 130 | `notes/three-stage-cover-bit.tex` | `47123a756f823c83a0d48cca2bf5add6472cd88410b13aed345e70c8834fb511` |
| PR 130 | `LICENSE` | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` |
| PR 130 | `NOTICE` | `e891051aa7858815850030c9531a88794ba0f39436fbd03cc0f2607a76da8b74` |
| Manuscript | `preprints/Integer-multiplication-below-n-log-n-September-23-2026/paper.pdf` | `834f644c3ce67932b9f7357d3615fb8fea4a7ff198d90e4f6883a15ba9df7129` |
| Manuscript | `preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/03-motifs.tex` | `ed76761194988a01af77ead0ea6469cb5dcd29690ab985a0b5a4006b0f2b69bb` |
| Manuscript | `preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/04-swap.tex` | `412b170ccaab38dba96e95e3cbfae09f4876a9818f8d278776a746b0f8044906` |
| Manuscript | `LICENSE` | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` |
| Issue 24 comparison | `research/outer-cover-moonshot/check_small.py` | `025e210e154559d90f492ea50d92e6a9bffa0a7922e2d79a46d435fddb3cf9a9` |

The Issue 27 artifact files inspected at its pinned commit are recorded by
these SHA-256 hashes:

| File | SHA-256 |
|---|---|
| `research/zeta-signed-center-bridge/COST_COMPARISON.md` | `d3f613dcb80ae93a1eb2c29ba47ad213d24cf314bd65aa2ee3e40db886ee7264` |
| `research/zeta-signed-center-bridge/EXACT_CHECK.md` | `af3a0a9f0c4353399b32f3b7c801acecd3d6c51e0b01ede10608ae6244c6d6d1` |
| `research/zeta-signed-center-bridge/FORMULA.md` | `0f9b97b9017a8323dd934f762db12492cfc276b3026b6763ef7459a4b7c47966` |
| `research/zeta-signed-center-bridge/PHYSICAL_INTERFACE.md` | `62f0feab92b0e5b5febccef5b2cfe881a1d925969055d9170ce935ed670277df` |
| `research/zeta-signed-center-bridge/RESULTS.md` | `b5bf03aa53f519225a08b5fe3c206ef26976bd82a54ccb08a77f7b2ef9c6430d` |
| `research/zeta-signed-center-bridge/SOURCES.md` | `659738ac96c62665637e59c3eb606c0367529af36357c12483046ff070aff2e2` |
| `research/zeta-signed-center-bridge/check_small.py` | `710f14d76617f02156997dc506de96e214e42921ba426554a4606541e9f6d3bd` |
| `research/zeta-signed-center-bridge/small_exact_receipt.json` | `3ed9525f88cd4a9ebbc5ffc44bfec545665ccad9894e64bd227ad231274fb9c9` |

The exact matrix digests for this pilot are in `BASELINE.md` and
`small_exact_receipt.json`. They hash canonical compact JSON encodings of
the full doubled-integer matrices.

## Notices and assistance

The pinned PR 144 graph and construction retain icekylinx's paired-cube
work, its disclosed OpenAI GPT-6 Astra assistance, and Codex integration.
The pinned PR 130 notice credits icekylinx's three-stage extension and
OpenAI GPT-6 Astra assistance, Codex integration, the adopted local complex
DAG, and the inherited bit-word authors and notices. The original manuscript
identifies OpenAI as author. The source trees carry Apache-2.0 licenses; their
existing `LICENSE` and `NOTICE` files were not changed or copied here.

The Issue 27 audit is credited to OpenAI Codex assistance. This independent
pilot report and its standard-library verifier were prepared with OpenAI
Codex assistance. This records research assistance, not independent review,
an OpenAI endorsement, or a claim of a multiplication improvement. The
checker reimplements the short exact formulas and does not copy source code.
