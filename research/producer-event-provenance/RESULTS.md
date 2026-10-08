# FAST results

**Outcome: `PARTIAL_TRACE_WITH_BLOCKER`.** The selected h=23 logical use and its local rational ranks are source-backed. No selected production slot, physical event, raise/copy/clear cause, reverse attribution, physical rational rank, or pivot/child descriptor is identified.

## Evidence and limits

- Issue 18 was read with `gh issue view`; Issue 16 at `cf0f30e932416a35147ec2e69f28b87a48e18b31` and all five Issue 17 audit files at `8d4fb37796f9eb2badeca1ef0dd1c810ae23245c` were read from their exact commits.
- The PR 63 graph, compiler, frame driver, screen, certificates, word hashes, and inherited Section 3-4 sources were read or hash-checked at `aa7701b68540b7863d3b66a414e4319915d6282d`. The frozen compiler and certificates were not changed.
- `build(h)` coalesces block inputs by producer value before matching, while `ops` and slot `events` serialize slots/groups without permanent node/use IDs. The whole-axis matching and reclaim decisions are required for an exact operation index; this pilot stops before that compile/replay.
- `trace_one.py` uses only inline standard-library fixture rows (18 rows across two explicitly separate synthetic orientations). It checks exact `Fraction` dimension differences `(4,4,0)` from the local source witness and rejects wrong uses, slots, frames/groups, carriers, missing raises/copies/clears/scatters, missing reverse attribution, and the one-logical-XOR-to-one-physical-XOR assumption. These fixture identifiers are not pinned events.

## Checks

- `python3 research/producer-event-provenance/trace_one.py`: PASS.
- FAST: PASS for the bounded source inspection and deterministic fixture check.
- FOCUSED: NOT RUN.
- FULL: NOT RUN.

The check has no graph, matrix, word, or compiler input; its memory is limited to the inline fixture and its execution time was not benchmarked. No `make verify`, full compiler build, full physical-word replay, large CRT/profile regeneration, or broad CI ran. The complete paid child histogram remains inherited and unchanged; no new `kappa` is implied.

Prepared with OpenAI Codex assistance.
