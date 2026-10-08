# h=23 focused trace

The logical occurrence is `FSa(2039) -> Y2(2044)`, operand 0, keyed by the pinned graph hash and axis. Issue 18's identity rules remain in force: graph node, operand occurrence, compiler use, frame group, carrier slot, `ops[]`, `events[]`, orientation, and rational frame edge are separate entities.

One real h=23 compiler call returned and emitted the word in memory. Matching took 36.665491 seconds; the compiler progress log reached step 50,000 at 92.374 seconds. The whole-axis role, rank-mass, XOR, statistics, and histogram checks against the frozen receipt passed.

Trace extraction stopped because the instrumented compiler had no standalone `value_slots` entry for `Y2(2044)`: the captured target slot was `None`. The post-processor tried to start a backward cone from that missing slot and raised `TypeError`. This does not establish that `Y2` has no equivalent linear representation; it establishes that this run did not capture a standalone output slot for it.

The runner had already serialized the generated word to canonical JSON and computed raw and gzip SHA-256 values in memory. The exception happened before those values were compared with the frozen word or saved. They cannot be recovered from the run record, so this artifact makes no word-match claim. No compiler operation ID, event ID, slot number, physical rank, pivot, or per-use cost is assigned.

The isolated runner now preserves a missing target slot as `UNRESOLVED` and saves digest comparisons before trace construction. Its fixture and exact-rank self-check passes. The h=23 compiler is not run again under this task's one-run limit.
