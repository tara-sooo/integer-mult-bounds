# Producer-to-event trace schema

**Status: schema proposal plus test fixture; no production event join is present.**

## Identity layers

| Identity | Meaning and cardinality | PR 63 creation and boundary |
|---|---|---|
| `producer_node` | One scalar value in the pair DAG. A node may have several outgoing operand uses. | `pair_graph.py` assigns node indices. The selected values are `FSa=2039`, `Sb2=2020`, and `Y2=2044`. These indices are meaningful only with the pinned graph hash. |
| `operand_use` | One occurrence of a producer at a consumer node and operand position. A node is not a use. | For this slice the two inputs of `Y2` are `(producer=2039, consumer=2044, operand=0)` and `(producer=2020, consumer=2044, operand=1)`. PR 63 has no exported stable use ID. A proposed ID is the tuple `(graph_sha256, axis, producer_node, consumer_node, operand_position)`. |
| `block` / `frame_group` | Nodes sharing the same `(core, union/cover)` envelope, assigned a compile-local group index. One block can contain many nodes and uses. | `build(h)` groups by envelope key, stores `nodes[]`, and forms external `inputs` as a set. Group number `g` depends on compile ordering; the frame key is the stable mathematical descriptor. The set coalesces repeated external values and omits the consumer node/operand position. |
| `carrier` | A value continuation chosen by block synthesis or use matching. A source value can be retained, copied, carried, or retired. | `match()` selects candidate compiler-use indices; `assign` maps those indices to slots. The mapping is internal and compile-local. Repeated output values can be copied into extra carriers. |
| `slot` | A physical role in one saved word. It can be created, raised, retired, cleared, and reused. | `new()` assigns slot numbers; `acquire()` may reclaim a cleared slot. Slot numbers have meaning only within the exact saved word. Reverse-complement execution is a separate orientation. |
| `primitive_event` | An emitted operation or frame transition. One logical node/use may yield zero, one, or many events. | `ops[k]` stores `(target_slot, control_slot, frame_group)` for an XOR. `events[j]` stores `(slot, old_group, new_group)` for allocation/raise transitions (`old_group=-1` means allocation). Neither stores a producer node or operand-use ID. Copy/clear purpose is not a distinct tag in `ops`; their XORs need compiler-side cause metadata. |
| `scatter/source` | Input placement or an output read/target record. It need not be a graph operand use. | The word separately stores `sources`, `outputs`, and `scatter` tuples. They do not identify the originating producer node/use. |
| `orientation` | One execution of a word, such as forward or reverse-complement. | The compiler receipt checks both orientations, but the saved `ops` tuples have no orientation label or independent event IDs. The orientation belongs in the trace key. |
| `rational_edge/pivot` | An adjacent address-frame transition `M_head-M_tail`, its exact rational rank, and—if factored—pivot coordinates/child descriptor. | The projector family is derived from the envelope group plus the 23/25 context. The selected Issue 16 `(4,4,0)` ranks are local logical-edge ranks, not physical-op charges or production pivots. |

## Proposed production record

```text
trace_kind: PINNED_WORD_TRACE
source: { graph_sha256, compiler_sha256, word_sha256, axis }
logical_use: { producer_node, consumer_node, operand_position, stable_use_id }
block: { frame_key, compile_group_index, node_ids }
carrier: { match_use_index, carrier_id, retired_or_retained }
slot: { word_sha256, slot_index, before_frame, after_frame }
physical: { word_sha256, ops_index | events_index, op_tuple, cause }
orientation: FORWARD | REVERSE_COMPLEMENT
frame_edge: { context, tail_frame, head_frame, rank_Q, pivots, child }
trace_confidence: PINNED_JOIN | FIXTURE_ONLY | UNRESOLVED
```

For this task, `stable_use_id`, `carrier_id`, the selected word indices, operation causes, and selected physical frame edges are `UNRESOLVED`. A canonical physical XOR reference can be formed from `(word_sha256, ops_index)` only after the actual operation is located; it does not establish a logical-use join by itself. The numeric compiler-use index is not a stable source-use ID.

## Cardinalities in the pinned h=23 record

- The selected graph slice has two operand occurrences at `Y2=2044`; `FSa=2039` is operand 0 and `Sb2=2020` is operand 1. `Y2` has a later use at consumer `2048`, operand 1. The reversible shear also preserves `FSa`; that role has no separate use ID in the selected logical DAG.
- The h=23 rank-first receipt has 52,473 blocks, of which 10,350 contain multiple nodes; 37,025 matched uses; 27,918 slots; 149,172 XOR tuples; 1,612 clearing XORs; and 621,482 replay word operations. These are whole-axis counts, not counts for the selected use.
- The h=23 serialized word has arrays for `ops`, `sources`, `scatter`, `outputs`, `frames`, and slot `events`. It contains no stable producer-node/use field on an XOR or raise. Thus selected-use-to-event cardinality is unknown, not one.

## Unknown and many-to-many rules

- Use `UNRESOLVED` when a value is absent from the source artifact or the join has not been established. Use `NO_EVENT` only after a complete, scoped search proves the trace has no event.
- Keep fixture IDs prefixed `fixture:` and set `trace_confidence=FIXTURE_ONLY`. They are test-row keys, never pinned physical event IDs.
- Store zero-to-many and many-to-one relations as lists. Do not infer a bijection from node count, XOR count, word order, or equal ranks.
- A `clear`, `copy`, or `raise` is paid work where the compiler emits a transition; do not drop it because its cause is administrative. Keep its exact operation tuple, slot/frame transition, dependency, and orientation when those are available.
- Attach `rank_Q`, pivot coordinates, and child descriptors only after both adjacent rational frames and their physical event/role are joined. A logical edge rank alone does not identify a Section 4 call.
