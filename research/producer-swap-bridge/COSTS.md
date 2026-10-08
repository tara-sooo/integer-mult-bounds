# Costs and ownership for the selected `FSa → Y2` use

## Scalar producer

The generated local DAG has two named additions in this subgraph:

| Operation | Scalar work | Result |
|---|---:|---|
| `FSa = F ⊕ Sa` | 1 XOR | Creates the retained value `x`. |
| `Y2 = FSa ⊕ Sb2` | 1 XOR | Consumes `x` and `z=Sb2`; returns `x⊕z`. |

These are logical source operations, not recursive-call counts. If the
compiler needs an extra role to preserve or duplicate a value, that XOR and
its frame transitions must be charged. The frozen aggregate does not say
whether this particular use caused such a copy or reclamation.

## Physical PR 63 record

The selected axis is `h=23`. Its pinned whole-graph record is:

| Quantity | Recorded value | Scope |
|---|---:|---|
| Input dimension `v` | 1,771 | Whole axis. |
| Physical roles | 27,918 | Whole axis. |
| Compiled regions | 52,473 | Whole axis. |
| Matched carrier links | 37,025 | Whole axis. |
| Reclaimed roles | 801 | Whole axis. |
| Paid clearing XORs | 1,612 | Whole axis; included in compiled work. |
| Elementary XORs | 149,172 | Whole physical word. |
| Frame-transition rank mass | 642,620 | Whole physical word/profile. |
| Independent replay word length | 621,482 | Whole physical word. |
| Dirty/input basis vectors | 31,460 | Checked in both orientations. |

The replay checks every input and dirty basis vector in both orientations,
checks all recorded physical frame inclusions, and returns all dirty role
values. These finite whole-graph checks do not attribute a role, transition,
or clearing XOR to the `FSa → Y2` use. In particular, `642,620` is the
compiler's aggregate rank mass; it is not `rank_Q(A_e)` for a manuscript
wire segment and is not a pivot count for this selected use.

## Section 4 charge if a bridge were established

For an identified rational edge difference `A_e`, Section 4 pays exactly
`rank_Q(A_e)` recursive calls, one per pivot of `A_e=E₁ΠE₂`. Each call
processes one disjoint role-row class of volume `V/W` and contributes
`(V/W)F_(k−1)`. The parent pays `O(V)` for row splitting/merging, triangular
updates, gate work, descriptor and stack movement, copies, and cleanup. The
fixed-tape child owns a complete array stream; other role streams are parked
and restored, and arbitrary scratch payload is preserved.

No `A_e` or selected physical event is available for `FSa → Y2`, so this
checkpoint cannot assign it a pivot count, child volume, or per-use physical
charge. The existing scalar moment and its child multiplicities are
unchanged.
