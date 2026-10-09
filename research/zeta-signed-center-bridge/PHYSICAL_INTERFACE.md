# Physical interface status: unresolved

The matrix factorization is exact. No certified physical schedule for the full B_z map or PR130 endpoint-frame proof is supplied.

| Map | Logical role | Physical status |
|---|---|---|
| E:P_4→U_8 | Place 32 source values at their triple masks | The pinned graph has 254 input roles, with 222 zero data contributions. No P_4-to-zeta source frame, role placement, or wrapper cleanup charge is supplied. |
| D_8E, singleton rows | Z_i=∑_{i∉S}x_S | Each singleton root is available after the eight zeta passes. It has 127 possible input slots, 20 carrying P_4 data. Its PR172 side-root frame is attached to address e_i; using it as a center input to triple targets needs a new adapter. |
| X | ∑_{S∈P_4}x_S | X is not a PR172 output because its empty target is excluded. The original Section 3 has a total-sum wire, but no P_4 read point, frame, copy tree, terminal charge, or dirty cleanup is transferred. |
| C_B | 32 signed output rows | X is used 32 times and each Z_i 12 times. A shared arithmetic schedule uses eight half-scalings and 96 additions. Copies, broadcasts, phases, output-frame moves, and cleanup remain unpriced. |

PR172’s scalar word has adjoint pre-reads, post-reads, inverse additions, and source subtraction for its own zeta graph. Those steps restore that graph’s roles. They do not wrap the new X source, B decoder, or its copies. The focused checker records the singleton raw-dirty pre-read footprint; it does not claim an end-to-end dirty-state word for the wrapper.

PR130 requires M_out(ρ(w))−M_in(w)=I for every data and scratch role, with its paid edge ranks. No endpoint matrices are specified for E, X, the singleton roots, or C_B. Therefore the original K/H schedule and three-stage signed interchange are not physically closed for this candidate.

## Complex and bit scopes

The complex dyadic ring permits 1/2. The shortcut X=(∑_i Z_i)/5 is not available there; a direct X avoids that quotient algebraically but has no paid P_4 carrier/frame.

The bit supplier cannot reuse this decoder: 1/2 is undefined in F_2. Its source physical form is H_0=(I−J/9)/2. Under the literal triple-indicator labeling, disjoint triples have H_0 pairing −1/2≠0, so that tested support assignment fails the required cap. This refutes only the literal labeling; it does not rule out a different bit encoding. A separate F_2 operator, decoder, and H_0-compatible frame adapter would be required.

No sign/gauge transfer, full arbitrary-dirty wrapper, or bit-side frame proof is claimed.
