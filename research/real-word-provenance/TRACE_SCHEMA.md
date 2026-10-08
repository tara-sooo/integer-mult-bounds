# Real-word trace schema

The record follows Issue 18's identity layers and keeps compiler-local IDs scoped to this exact pinned word.

| Entity | Identity | Interpretation |
|---|---|---|
| Logical producer | Graph node `2039` (`FSa`) | One scalar value, separate from an operand occurrence. |
| Logical use | `(axis=23, producer=2039, consumer=2044, operand=0)` | Stable graph occurrence under the pinned graph hash. |
| Block | `compile_` group plus `(core_mask, cover_mask)` | Multiple scalar nodes share a block. Its external `inputs` are value-deduplicated. |
| Compiler use | Index in `uses[]` | Present only for a cross-block input/output role. It is not a stable graph use ID. |
| Match/carrier | Actual `right[compiler_use]` and assigned slot | `matched=false` for the selected FSa use. The producer slot is passed to the consumer input directly. |
| Physical slot | Slot integer in the exact word and event history | A slot can change linear form, retire, be cleared, or be reused. |
| Physical XOR | `(word_sha256, axis=23, collection="ops", index)` plus exact tuple | May support several logical values, or one logical value may require several XORs. |
| Frame event | `(word_sha256, axis=23, collection="events", index)` plus exact tuple | Allocation has `old_group=-1`; a same-group raise has rank 0; an old/new group transition is ranked directly. |
| Linear form | GF(2) mask over listed block inputs and exact global source-variable mask | Replayed around each captured operation. `VIRTUAL_LINEAR_FORM` has no dedicated output slot and is not free to reuse. |
| Orientation | Not encoded on each array entry | `NOT_ENCODED_BY_ARRAY_ENTRY`; complete forward/reverse replay is `NOT_RUN`. |
| Rational edge | Actual old/new frame groups and exact rank | Product-context rank is equal per h=25 triple line because its factor rank is one. Pivot and Section 4 child remain unresolved. |

## State labels

- `MATERIALIZED`: some real physical slot equals the target's exact global GF(2) form during the recorded interval. It does not imply `value_slots` exports that logical name.
- `VIRTUAL_LINEAR_FORM`: in the scoped state (here, block exit) no single slot is assigned the target form, but the saved slot forms exactly reconstruct it. A value may have been materialized earlier.
- `UNRESOLVED`: neither physical equality nor an exact linear solution is established.

The top-level target state is `MATERIALIZED`: slot 17581 contains `Y2` after `ops[75970]` and changes away from it at `ops[75972]`. The independent block-exit representation state is `VIRTUAL_LINEAR_FORM`: `Y2 = slot 21455 XOR slot 17581`, where slot 21455 carries external output `2048` and slot 17581 is a retired slot carrying input `1952`.

## Validation and cardinality

`TRACE.json` stores the producer and consumer block input/coefficient/output rows; the Gaussian elimination and exact physical XOR plan; every `ops[]` and `events[]` entry in both groups; exact raising-event references and rational ranks; producer and target linear cones; and the temporary target-valued slot interval. The separate `FOCUSED_RAW_TRACE.json` was written before analysis.

Linear replay initializes the actual block input slot forms, seeds any reclaimed slot at first use, checks every target/control form before each physical XOR, and checks the exit slot forms. The consumer block verifies `Y2`'s coefficient row as `2020 XOR 2039`, while its sole output row is `Y2048 = 1952 XOR 2020 XOR 2039`. The graph child `Y2 -> 2048` and output row explain why Y2 has no standalone output slot.

All slot, operation, and event references are verified against arrays in the hash-matching word. Negative controls reject changed operand identity, wrong coefficients/slots, operation reordering, omitted operation/copy/clear entries, missing frame raises, stale matching, and a missing hash checkpoint when `target_value_slot` is `None`. No one-to-one logical-XOR mapping is assumed. The source-paper cost and Section 4 child remain unallocated where shared work prevents an evidence-backed attribution.
