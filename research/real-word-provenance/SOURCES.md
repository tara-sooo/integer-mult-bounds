# Sources and pinned inputs

## Issue scope and tracking schema

- [Issue 19](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/19) defines the h=23 word identity and logical-to-physical provenance experiment, with no broader compile/replay.
- [Issue 18](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/18), read at fork commit `54e49f0301e09c08d2670a63af6fb15e72b9a146`, defines separate graph-use, compiler-use, block, carrier, slot, operation, frame-event, orientation, and rational-edge identities.
- Issue 18's `TRACE_SCHEMA.md` SHA-256 is `99cd22bb6d50b36251cb4d4629765e68599bd89c45caa7b5212d3c575d6392f6`; its `COSTS.md` SHA-256 is `cc1a5054b25a272fc82c12e6bc34a264813cd03ecbac3583ef27821ce7e87cd2`.

## Fixed PR 63 producer

- [PR 63](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/63), construction commit `aa7701b68540b7863d3b66a414e4319915d6282d`.
- The byte-copied source closure and file hashes are in `pinned/SOURCE_MANIFEST.json`; all were rechecked before the successful compile.
- Graph `research/pair-assembly/pair_graph.py`: SHA-256 `3d47e89d2649c90800a276bdd0480131def50e0bdf92c122a19494b55bf17420`.
- Frozen compiler `scripts/experiments/rank_pair_compiler.py`: SHA-256 `9984aaccf880e4840402322d76678bfddb33ce7e494af78430a43429f51b85fd`.
- Instrumented compiler copy used for the word: SHA-256 `e2eb7063e5ca6788dd86b3c2affdc49b470efc3ba57ca89ef820e76e6843bb89`. Its only edits are optional provenance capture; `INSTRUMENTATION.patch` is the exact diff.
- The original compiler source, certificates, and frozen word were not edited.

## Word identity and frame context

- Frozen h=23 canonical JSON SHA-256: `640696dd7cd893add9d6e12d0d587956fecf113b2eff8c29547b82e5a6f3c0ad`.
- Frozen gzip SHA-256: `1a57c143380a063211653f1f35e7cc9710539523b0b34c90f354a0425c34bd59`.
- The generated canonical bytes matched exactly. The gzip hash also matched when compressed with the frozen output filename, `mtime=0`, and level 9. `WORD_HASH_RECEIPT.json` preserves the initial no-filename `BytesIO` digest and its header-only explanation.
- Pair-assembly rational projector audit hash: `dd369a7a6e0be4354c05560d0e1d9750c14839928459f43beeb55970f86e0631`.
- Issue 17 frame-contract commit `8d4fb37796f9eb2badeca1ef0dd1c810ae23245c` supplies the inherited `P_T(25) tensor P_hat_g(23)` context with 2,300 rank-one h=25 triple lines. It scopes the lifted rank of a known physical edge; it does not provide event identity, pivots, child assignment, or a selected-use price.
