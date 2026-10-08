# Isolated compiler instrumentation

The original PR 63 compiler, graph, certificates, and word remain byte-pinned under `pinned/`. The experiment edits only `pinned/scripts/experiments/rank_pair_compiler.py`; its original sibling hash remains `9984aaccf880e4840402322d76678bfddb33ce7e494af78430a43429f51b85fd`. The instrumented compiler hash used for the successful word is recorded in `SOURCES.md` and `TRACE.json`. `INSTRUMENTATION.patch` is the complete copy-only diff.

The optional `trace_spec` records the selected occurrence before block-input values coalesce, the producer/consumer group metadata, compiler-use and matching decisions, assigned slots, elimination rows, physical XOR plan, operations, frame events, and append order. It tracks each touched physical slot as an exact GF(2) mask over the graph's original inputs, including reclaimed slots. The postprocessor independently replays the captured group operations, checks each before/after slot form, reconstructs block outputs, solves `Y2` over real block-exit slots, and round-trips every operation and event ID against the generated arrays.

The initial `target_value_slot=None` was a compiler output-selection result, not an omitted capture. `value_slots` maps values needed outside a block. `Y2` has only an intra-block graph child, `2048`, and its block exports `2048`, so no standalone `value_slots[2044]` exists. Its `coeff` row is nevertheless exactly `0b110` over `[1952,2020,2039]`.

The slot-state trace additionally found an actual transient materialization: slot 17581 becomes `Y2` at `ops[75970]` and stops representing it at `ops[75972]`. At block exit it contains input `1952` and is marked retired; the output slot for `Y2048` is 21455. The verified relation is `Y2 = slot 21455 XOR slot 17581`. `VIRTUAL_LINEAR_FORM` describes this exact algebraic relation, not a free stored value.

The compiler-use array in the raw instrumented ledger is global and a physical slot number can be reused; that raw list can retain historical use-to-slot entries. The final sidecar only associates exit slots with this block's output compiler uses and its selected carry edges. It labels slot 17581 as retired and does not treat stale global assignments as live output carriers.

## Hash-first execution

The FOCUSED runner completes one `compile_(23, matching=True, reclaim=True, dirty=False, trace_spec=...)`. Before it invokes trace analysis, it writes `WORD_HASH_RECEIPT.json` and `FOCUSED_RAW_TRACE.json`. The receipt captures canonical bytes and SHA-256, compiler receipt checks, word counts, memory/time, and gzip metadata. If canonical word bytes drift, the generated gzip word is retained for diagnosis. A missing target slot or postprocessor exception cannot erase that checkpoint.

Canonical JSON is the primary identity check. Gzip comparison uses the frozen artifact's output filename, mtime 0, and level 9. The initial no-filename `BytesIO` variant had a different header and hash, but identical DEFLATE bytes and trailer; adding the pinned `frame-word-23.json` FNAME field reproduces the exact frozen gzip hash. This separates wrapper metadata from compressed-word content.

The successful compiler run took 89.21 s, peak RSS 286,532 KiB. A postprocessing validator initially assumed both raise events around an XOR belonged to the same slot; it correctly found the target and control slots differed. That validator was fixed, and analysis resumed from the saved raw trace and frozen word without another compiler call. The highest recorded process RSS across compile and recovery analysis was 473,856 KiB. FAST and recovery details are in `FAST_CHECK_RECEIPT.json` and `runs/attempt-02/POSTPROCESS_RECOVERY.json`.

For each old/new frame event, the postprocessor computes the exact rational rank of the pinned PR 63 envelope-projector difference. A known event in the inherited product context has the same per-h25-triple-context rank in `Q^575`, since the h=25 factor has rank one. Allocation events have no old projector and remain rank-unknown. No pivot coordinates, Section 4 child, operation orientation, full replay, h=25 compilation, or new `κ` are inferred.
