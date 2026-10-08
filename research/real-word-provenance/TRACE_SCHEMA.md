# Trace schema

The sidecar uses IDs only where the source or generated arrays provide them.

| Entity | Identity in this experiment | Cardinality / unknown handling |
|---|---|---|
| Logical producer node | PR 63 graph node `2039` (`FSa`) | A value node, not an operand occurrence. |
| Logical use | `(axis=23, producer=2039, consumer=2044, operand=0)` | Stable graph-occurrence key; other occurrences of producer `2039` inside the same block are listed as coalesced occurrences. |
| Envelope block | `compile_` group index plus `(core_mask, cover_mask)` | Several scalar nodes may share one group. |
| Compiler use | Integer index in `uses[]` | Present only for an external block input. It is compiler-local, not a stable graph edge ID. No index is emitted for an intra-block operand. |
| Matched carrier | Actual `right[compiler_use]` edge, if selected | `UNRESOLVED`/absent when the use is unmatched; no carrier is inferred from node count. |
| Physical slot | Slot integer from the compiler's actual `assign`, `value_slots`, and input arrays | Meaning is scoped by this exact word hash and its event history. |
| Physical XOR | `(word_sha256, axis=23, collection="ops", index=k)` and exact tuple | One logical use may depend on zero or many compiler ops. Causes describe the source call site. |
| Frame event | `(word_sha256, axis=23, collection="events", index=j)` and exact tuple | Includes allocations, same-frame raises, and actual frame changes; these are distinct from XORs. |
| Orientation | The saved arrays have no orientation field | `NOT_ENCODED_BY_ARRAY_ENTRY`; full forward/reverse execution is `NOT_RUN`. |
| Rational frame edge | Old/new frame group keys, exact h=23 factor rank, and the product-context rank per h=25 triple line | The inherited product family is `P_T(25) tensor P_hat_g(23)`, with `rank(P_T)=1` for every one of the 2,300 triples. A known old/new edge therefore has the same exact rank in Q^575 as in its 23 factor. Same-frame raises cost rank 0; allocation has no old frame and rank is `UNRESOLVED`. A Section 4 pivot/child identity remains `UNRESOLVED`. |

On a successful run, the trace stores all `ops[]` and `events[]` entries emitted in the producer and consumer groups, the exact group-wide index sets, and the backward operation cone for the producer's assigned use slot and the consumer's `Y2` output slot. A distinct-block join is confirmed only if the selected compiler use's assigned slot equals the consumer's input slot and exact block-row dataflow shows that slot in the `Y2` output cone. In this run the captured `Y2` output slot was `None`; the post-processor failed before writing a production sidecar. `TRACE.json` records that failure without inventing operation or event IDs.

The record does not assign a one-to-one cardinality. It lists the exact producer-value-to-carrier and input-to-`Y2` operation cones separately; operations can be shared by several outputs in a block. No physical operation or event ID is created by the trace code. `NO_EVENT` is reserved for a completed scoped search proving absence; otherwise fields stay `UNRESOLVED`.
