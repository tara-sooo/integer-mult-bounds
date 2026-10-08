# Selected `FSa -> Y2` trace attempt

**Outcome: partial trace with a source-to-word join blocker.** This file separates pinned logical evidence from a synthetic schema fixture. It reports no selected PR 63 physical event ID.

## Pinned logical path

At h=23, the pinned graph has:

```text
FSa node 2039 ── operand 0 ──┐
                              ├─> Y2 node 2044 ── operand 1 ──> consumer 2048
Sb2 node 2020 ── operand 1 ──┘
```

The selected source use is the occurrence `(2039, 2044, operand 0)`. The `(2020, 2044, operand 1)` occurrence is the other input to that logical XOR. The later `Y2 -> 2048` occurrence is a different use. Issue 16 derives source-local envelope dimensions 10, 10, and 14, and the exact rational logical-edge ranks `(4,4,0)` in its chosen `Q^23 tensor Q^25` lift. Those facts locate the logical neighborhood; they do not name a word slot or event.

## Where the join is lost

```text
pair_graph node/operand occurrences
        │
        ▼
rank_pair_compiler.build(h): nodes grouped by envelope; external inputs deduplicated by value
        │   compile-local block/use indices; selected uses and carrier matching
        ▼
slot allocation / raise / acquire / block XOR synthesis
        │
        ├── ops[k]       = (target slot, control slot, frame group)
        ├── events[j]     = (slot, old group, new group)
        └── sources / outputs / scatter records
             no permanent source node or operand-use ID
```

The compiler's `uses` list uses sequential indices and records a value, target block, and optional terminal. Before that, each block's external producer values are collected in a set, so consumer node and operand position have already been coalesced. Matching then chooses among those compiler-local uses. `frame_compile.py` hash-pins the graph and unchanged compiler and compiles each full axis; the global match and reclaim order determine the selected slot and operation indices. The independent Issue 16 role timeline preserves logical uses in a different slot assignment and is not a map into the rank-first word.

The saved word does retain physical slot and frame-group data. Its `events` array is a slot/frame transition list, not a list of source-attributed event IDs. The XOR list has exact tuple order but no source-use field. A word hash plus operation index could name a located XOR, but there is no evidence here to choose that index for use `(2039,2044,0)`.

## Reverse execution and stop point

The pinned compiler/receipt checks both forward and reverse-complement behavior. The saved operation tuples do not distinguish those executions. Any future sidecar must key event references by orientation and retain raises, copies, clears, and scatter dependencies separately. No full compiler build or word replay was run for this pilot: block matching and reclamation are global, and running that path would violate the bounded FAST scope.

The least missing source artifact is a sidecar from the unchanged pinned compiler at the emission seam. Before block-input coalescing it must retain `(graph hash, producer node, consumer node, operand position)`; through matching it must retain block/frame key, matched-use/carrier assignment, physical slot lifetime, and orientation; at emission it must retain exact `ops`/`events` indices, operation tuple/cause, raises, copy/clear dependencies, and output/scatter record. The matching sidecar must be produced with the pinned whole-axis build, since a hand-isolated block would not preserve the global matching or reclaim decisions.

## Fixture boundary

`trace_one.py` contains a tiny **toy fixture**, not a source-faithful compiler run and not a pinned word event. Its `fixture:` row keys demonstrate the schema's one-to-many handling and negative controls only. Production fields for event IDs, physical slots, frames, carrier matching, operation causes, and orientation attribution remain `UNRESOLVED`.
