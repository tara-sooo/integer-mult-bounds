# h=23 real-word trace

The generated word matches the frozen PR 63 canonical JSON byte-for-byte at SHA-256 `640696dd7cd893add9d6e12d0d587956fecf113b2eff8c29547b82e5a6f3c0ad`. The correctly named gzip output also matches SHA-256 `1a57c143380a063211653f1f35e7cc9710539523b0b34c90f354a0425c34bd59`.

`FSa(2039)` is emitted from group 1908 into slot 17581. Compiler use 455 places that same slot at input 2039 of group 1929; `events[226456]=(17581,1908,1929)` is its rank-4 frame raise. `Y2(2044)` belongs to group 1929, whose external inputs are `[1952,2020,2039]`. Its coefficient mask is `0b110`, or `2020 XOR 2039`.

There is no dedicated `value_slots[2044]`: the only exported value from group 1929 is `2048`. The graph's direct child is `(2044 -> 2048, operand 1)`, also inside group 1929. In the physical basis transform, slot 17581 becomes `Y2` after `ops[75970]`, remains so while `ops[75971]` produces `Y2048` in slot 21455, then changes back to `1952` at `ops[75972]`. At block exit, `Y2 = slot 21455 XOR slot 17581`; slot 17581 is retired. Thus the value is `MATERIALIZED` temporarily and `VIRTUAL_LINEAR_FORM` at block exit.

The logical use relates to several physical operations and frame events. The exact producer cone is `ops[55648]`, `ops[55650]`, `ops[55655]`; the target linear-form cone is `ops[75970]`, `ops[75972]`. The matched continuation is false for FSa's use. The other input `2020` has a separate matched carry (use 427) in the same block. Three later copy operations duplicate `Y2048` for other outgoing uses; they remain in the sidecar but are not charged to this logical occurrence.

The actual carrier edge from group 1908 to 1929 has exact rational rank 4. The second `Y2` input edge also has rank 4. The producer inputs contribute ranks 2, 4, 6, and 4; the operations within the two groups' synthesis frames are rank 0. These are event-level ranks, not an apportioned logical-use cost. Pivots, a Section 4 child, full orientation replay, h=25, and a new `κ` are not established.

`TRACE.json` contains the verified block coefficients and basis, physical slot linear forms, exact operation/event tuples, per-event ranks, the saved-word hash receipt, resource measurements, and negative-control results. `FOCUSED_RAW_TRACE.json` preserves the pre-analysis compiler records. See `COSTS.md` for the event ledger and unresolved costs.
