# Sources and pins

## Request and tracking rules

- [Issue 19](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/19) defines the one-axis h=23 experiment, the pinned-word hash check, the resource gate, and the prohibition on broader runs.
- [Issue 18](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/18), read at fork commit `54e49f0301e09c08d2670a63af6fb15e72b9a146`, defines separate identities for graph nodes, operand uses, blocks, carriers, slots, operations, frame events, orientation, and rational frame edges. Its result explicitly labels prior tracing as fixture-only.
- Issue 18's `research/producer-event-provenance/TRACE_SCHEMA.md` SHA-256: `99cd22bb6d50b36251cb4d4629765e68599bd89c45caa7b5212d3c575d6392f6`.
- Issue 18's `research/producer-event-provenance/COSTS.md` SHA-256: `cc1a5054b25a272fc82c12e6bc34a264813cd03ecbac3583ef27821ce7e87cd2`.

## Frozen PR 63 source

- [PR 63](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/63), construction commit `aa7701b68540b7863d3b66a414e4319915d6282d`.
- The byte-copied source closure is enumerated in `pinned/SOURCE_MANIFEST.json`; every listed file was checked against its SHA-256 before the single compile.
- Graph `research/pair-assembly/pair_graph.py`: `3d47e89d2649c90800a276bdd0480131def50e0bdf92c122a19494b55bf17420`.
- Original `scripts/experiments/rank_pair_compiler.py`: `9984aaccf880e4840402322d76678bfddb33ce7e494af78430a43429f51b85fd`. The separately instrumented copy is `6581da72be6f53246d1989c75ec36ca90960ebd6cbb3b4b1427a6343486fea53`; the exact isolated diff is `INSTRUMENTATION.patch`.
- Pair assembly rational projector audit: `dd369a7a6e0be4354c05560d0e1d9750c14839928459f43beeb55970f86e0631`.
- Frozen h=23 word gzip: `1a57c143380a063211653f1f35e7cc9710539523b0b34c90f354a0425c34bd59`. Decompressed canonical JSON: `640696dd7cd893add9d6e12d0d587956fecf113b2eff8c29547b82e5a6f3c0ad`. The baseline artifact passed local integrity checks; the generated word was not verified against it.

## Global frame context

- Issue 17 frame-contract commit `8d4fb37796f9eb2badeca1ef0dd1c810ae23245c` supplies the inherited `P_T(25) tensor P_hat_g(23)` product context with 2,300 rank-one h=25 triple lines. Its endpoint contract is SHA-256 `28219018338e7161b00ce3a7838db40d8e0863ea2033034262d1bc178bc80e53`.
- Issue 17 is used only to scope how a known nested frame edge would lift. It does not supply the missing selected compiler slot or event ID.
