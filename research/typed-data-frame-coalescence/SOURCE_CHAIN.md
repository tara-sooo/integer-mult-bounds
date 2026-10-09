# Source-chain provenance

## Checkpoint status

**`PROFILE_ONLY_NO_TYPED_CHAIN`.** The pinned complex supplier confirms the aggregate source widths `1:1320, 2:1320, 18:1320`. The audited producer does not associate those entries with one chronological physical role, its intermediate frames, gate IDs, or a consumer. No chain is inferred from the matching counts.

## Frozen inputs

- The complex supplier is pinned at [the PR193 source commit](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/187e1010ac8b259af8e9b5166f68b64bc27b4b47). Its `research/source-assisted-v4/certificate.json` hash is `d84406d2fcc6990deba2b135509e6d86600e57123d88f9b21f7b7240e1aeb513`.
- The cost input is [the PR203 research commit](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/d2873e20750d0949d2ad75cbc4cd82b5b1a74e84), file `research/percent-exponent-architecture/inputs/complex-pr193.json`, SHA-256 `b608bc0af5ad837ea2604fed3cba82cadf5ab3f001fc74d9cea01fe3dc9fb201`. It points back to the PR193 certificate hash above.
- The source files named by the issue are pinned by PR193's `upstream/manifest.json` to [the original source commit](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a). The manifest hashes `03-motifs.tex` as `ed76761194988a01af77ead0ea6469cb5dcd29690ab985a0b5a4006b0f2b69bb` and `04-swap.tex` as `412b170ccaab38dba96e95e3cbfae09f4876a9818f8d278776a746b0f8044906`.

## What the pinned producer records

The deterministic replay of `scripts/paired_cube_producer.py` from the PR193 commit completed successfully and matched its pinned complex input. Its `graph.json` has `h=22`, `v=1320`, source histogram `{1:1320, 2:1320, 18:1320}`, and target histogram `{1:3960, 18:1320}`. It also emits a local `frames.json` and `selection.json`; the latter has 1,320 local source slots and 32,971 local operations.

In `scripts/paired_cube/graph.py`, `Graph.finish` assigns `source_data_histogram` as `{2: len(labels), h-4: len(labels), 1: len(labels)}`. In `research/source-assisted-v4/contract_v4.py`, the contract checker reads that histogram from `certificates/paired-cube-sinks-input.json` and adds three copies to the paid child ledger. Neither record has a per-port mapping from those widths to a role and its ordered gate incidences. The producer's `selection.sources` and `selection.ops` identify roles and gates of its local helper word; no field links those IDs to the separate source histogram.

The replay therefore confirms the supplier and the arithmetic inputs, but cannot answer whether all three widths lie on the same role. The PR193 local certificate also says that a globally renumbered scalar transcript and a full Clifford/router replay are not exported.

## Why the original source does not fill this gap

The pinned original `03-motifs.tex` specifies scalar roles (`X_a`, `Y_a`, side wires, and center wires), gate schedules, and common frames for its `h=100`, `m=h^3=1,000,000` example. That is not the PR193 `h=22`, `m=66` supplier, and there is no recorded map between those role IDs and the PR193 source histogram. The pinned `04-swap.tex` explains that a rank-`r` rational shear uses `r` recursive interchanges, each realized by a three-shear sequence. This makes a frame-rank ledger insufficient to identify a particular charged runtime call.

PR203 describes a candidate source-chain rank pattern `[2,18,1]` for one general interface, but explicitly leaves it as an endpoint ingredient rather than a complete global word. It does not supply the PR193 role, event order, frame matrices, or gate record needed here.

## Exact evidence needed to resume

Export one representative PR193 source port with:

1. its physical role ID, source value, all role aliases, and the actual consumer;
2. ordered `M0` through `M3` frame vectors or matrices and the exact role-edge endpoints;
3. each intervening gate ID and time, every incidence wire, and the single common frame used by that gate;
4. source-assisted control ports, parity frame, signs, and source/target ownership at those events;
5. the complete all-role input/output map, including spectators and arbitrary dirty scratch restoration; and
6. the mapping from each frame edge to its charged child, including the rank-one `Swap` pivot occurrences on the full address arrays.

Without this record there is no actual intermediate gate at which to test a frame collision, and no basis for naming a representative chronological chain.
