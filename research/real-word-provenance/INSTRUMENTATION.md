# Isolated instrumentation

The exact PR 63 compiler is kept beside the instrumented copy as `pinned/scripts/experiments/rank_pair_compiler.py.original`. Its SHA-256 remains `9984aaccf880e4840402322d76678bfddb33ce7e494af78430a43429f51b85fd`. The paired graph, PR 48 producer dependency closure, receipt and frozen h=23 word are byte-copied from PR 63 under `pinned/`; no original source, certificate, or word was edited.

The only compiler edits add an optional `trace_spec` used for this one selected h=23 operand. The existing `build`, candidate ordering, `match`, reclamation, slot choices, elimination rows, XOR order, scatter and output generation remain intact. Instrumentation observes, around the producer and consumer groups:

- the selected graph occurrence before the block-input set deduplicates values;
- the consumer block's compiler-use index, match result, input row and assigned physical slot;
- exact `ops[k]` tuples, cause (`block_synthesis`, `dependent_output`, `duplicate_use_copy`, or `retired_slot_clear`), and the two actual `events[j]` appended by each XOR;
- direct block-input raises, slot allocation events, selected producer/consumer output slots and output-use carrier slots;
- the local order in which these records were appended.

Cause labels are call-site metadata from the frozen compiler control flow; they are not fields in the serialized word. Each recorded operation and event is independently round-tripped against the actual generated arrays, and group-wide index lists must equal all corresponding records in those arrays.

For each identified old/new group event, the runner computes the exact rational rank of the 23-dimensional envelope-projector difference using the pinned `audit.py` formula. The inherited Issue 17 product frame gives `P_T(25) tensor P_hat_g(23)` in each h=23 context, and every h=25 triple line has rank one. Thus the 575-dimensional edge rank for each replicated context equals the computed h=23 factor rank, uniformly over the 2,300 triple lines. Allocation has no old projector and stays unresolved; no pivot coordinates or Section 4 child are inferred.

The runner imports the PR 48 compiler dependencies first, then clears only Python's module cache entries for the `partial_swap` package and loads the separately pinned PR 63 graph dependencies from their own copy. The compiler's imported PR 48 producer objects remain referenced by its module. It calls `compile_(23, matching=True, reclaim=True, dirty=False, trace_spec=...)` exactly once. The trace parameter only adds observation records; it does not choose a slot, gate, frame or output.

After emission, canonical JSON is serialized using the frozen driver expression. Its bytes and SHA-256 are compared with the decompressed frozen word; deterministic gzip is also compared when the local zlib output permits an exact match. No full dirty replay is run. A matching word proves emitted-word identity, while the separately checked logical-use-to-slot-to-op references establish the trace join.

In the sole h=23 run, the compiler returned and the word was canonicalized, but trace construction failed before either digest was compared or saved: the trace read no materialized `value_slots` entry for `Y2=2044` and passed `None` to the backward-cone walker. The isolated runner was then corrected to preserve a missing target slot as unresolved and to save the word-hash comparison before trace construction. That correction has only fixture self-check coverage; the one-compile limit prevents another h=23 run here. See `RESULTS.md` and `TRACE.json` for the exact boundary of what this run establishes.
