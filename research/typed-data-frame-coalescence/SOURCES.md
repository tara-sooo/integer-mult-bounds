# Sources and provenance

## Frozen inputs

| Source | Immutable reference | File evidence used |
| --- | --- | --- |
| PR193 complex supplier | [Pinned commit](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/187e1010ac8b259af8e9b5166f68b64bc27b4b47) | `research/source-assisted-v4/certificate.json`, SHA-256 `d84406d2fcc6990deba2b135509e6d86600e57123d88f9b21f7b7240e1aeb513` |
| PR203 cost analysis | [Pinned commit](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/d2873e20750d0949d2ad75cbc4cd82b5b1a74e84) | `research/percent-exponent-architecture/inputs/complex-pr193.json`, SHA-256 `b608bc0af5ad837ea2604fed3cba82cadf5ab3f001fc74d9cea01fe3dc9fb201` |
| Original manuscript source | [Pinned source commit](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a) | `03-motifs.tex`, SHA-256 `ed76761194988a01af77ead0ea6469cb5dcd29690ab985a0b5a4006b0f2b69bb`; `04-swap.tex`, SHA-256 `412b170ccaab38dba96e95e3cbfae09f4876a9818f8d278776a746b0f8044906` (as pinned in PR193's `upstream/manifest.json`) |
| Previous checkpoint reviewed for scope | [Fork Issue 35 result commit](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/f6618ae74e6e2ad4c2583c915f967809887d4794) | Its `LEGAL_HANDOFF_BUT_NO_DATA_GAIN` result was not reused as a candidate. |

The PR193 `research/source-assisted-v4/SOURCE.json` pins `scripts/paired_cube_producer.py` at `97efa5842c040537f05072e26b7ba1851a1965eca6ec2472e75aa452cf7a7256`, `scripts/paired_cube/graph.py` at `d10478ba509c7d8abcefcaaf7c5e0b580b9cd9cbe7777b3e49b2fe24620985c8`, and `research/source-assisted-v4/contract_v4.py` at `67da183217adbe28915391c8cd0c8c4ec9c9dedead54a641a2de23834df2342c`.

## Replay

The pinned PR193 paths needed by `scripts/paired_cube_producer.py` were extracted to a scratch directory and replayed with Python assertions enabled. The command completed with exit status 0 after regenerating the signed graph, matching frozen arcs, selecting the physical word, and checking the local scalar identity and target chains. The scratch output was removed after inspection. No generated role/frame trace was committed because the producer does not export the required source-data-to-role mapping.

PR193's `research/source-assisted-v4/NOTICE` credits the package to Avi Eisenberg with Claude assistance; the method is derived from PR184 work by icekylinx with OpenAI assistance; its query modules and physical layer retain eumemic/Claude and PR117 attributions. The original manuscript source is under the Apache License 2.0 pinned in `upstream/manifest.json`. This checkpoint adds analysis documents only and copies no upstream code or manuscript text.

These documents were prepared by OpenAI Codex with AI assistance. No code artifact is included. This work was requested for [Fork Issue 36](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/36); no upstream post, push, comment, mention, or notification was sent.
