# One producer-to-Swap bridge audit

## Selected operation

The candidate is the `h=23` pair-assembly use generated in the two-by-two
group case of `pair_graph.py`:

```text
FSa = F ⊕ Sa
Y2  = FSa ⊕ Sb2
```

At the cut immediately before the `Y2` gate, put `x=FSa` and `z=Sb2`. The
local scalar map, retaining the carrier, is

```text
(x,z) ↦ (x, x⊕z),       S = [[1,0],[1,1]] over F₂.
```

It is invertible and self-inverse; an arbitrary dirty spectator is unchanged.
This verifies the scalar dependency. It does not identify a recursive call.
The `Y2` gate combines bit values at one address. Section 4's child instead
permutes addresses of a complete array on one role stream.

In this two-value scalar space, `S−I=[[0,0],[1,0]]` has rank one over
`F₂`, with its sole pivot at row 2, column 1. Section 4's pivot is selected
from `Π` after factoring the rational address-frame difference `A_e` in
`Q^{m×m}`. No map between these two matrix spaces is pinned.

## Section 4 object required for a call

Section 4 assigns a rational matrix `M_v ∈ Q^{m×m}` to each source, gate,
and sink, with the same matrix at every incidence of a gate. For a particular
wire segment `e`, it needs the actual difference

```text
A_e = M_head(e) - M_tail(e),     a = rank_Q(A_e).
```

The fixed lower-triangular factorization `A_e=E₁ΠE₂` has `a` pivots. Each
pivot, not each XOR node, invokes one `Swap_(k−1)` on a pair of `b=e/m`
digit fields in one row class. That child receives the complete row stream
with arbitrary payload, swaps the two address fields, preserves all
spectators, and returns the same shape. Its charge is `(V/W)F_(k−1)`; the
parent's splitting, frame work, copies, stack handling, and cleanup are also
charged `O(V)`.

For the manuscript's pinned bit network, `m=1,000,000`,
`W_b=177,176,569,091,445,000,000`, and the sum of these rational edge ranks
is `s_b=177,176,569,088,785,861,287,000,000`. These are the paper network's
constants. The PR 63 certificate's `m=575`, `W=137,151,806`, and `n_529`
belong to a different profile and do not name its `Swap` calls.

## Where the attempted bridge stops

The pinned PR 63 compiler groups producer nodes by the bitset pair
`(core, cover)` and records a local frame rank as
`popcount(cover) - popcount(core)` (with rank one for a source block). Its
frame-containment and paid-XOR checks are meaningful for that compiler. The
source does not assign a common rational address-frame matrix to each
producer gate, or identify these bitset labels with the manuscript's `M_v`.
Thus no source-derived `A_e` exists for the selected `FSa → Y2` incidence in
the frozen artifacts, and its required `rank_Q(A_e)` and pivot matrix are
undefined there. The rank-one difference `S−I` belongs to the two-scalar
`F₂` value map; it is not an address-frame matrix in `Q^{m×m}`.

There is a separate locator gap. The compiler's internal blocks have source
node lists, but its serialized word stores slot operations, source/scatter
records, output records, frame labels, and frame events without the block's
producer node IDs or the original operand-use ID. The `h=23` transition and
profile JSON files retain aggregate counts only. The local generator also
does not persist the group-pair occurrence ID for `FSa` and `Y2`. Therefore
the frozen physical word cannot select one physical event for this source
use or attach its exact paid copy, frame-change, and cleanup costs.

The current evidence supports this bounded conclusion:

```text
producer scalar use ──[verified]──> local F₂ shear
local F₂ shear      ──[missing]───> rational address-frame difference A_e
A_e pivot           ──[missing]───> a selected Swap_(k−1) child
```

This is `NO_BRIDGE_AT_SELECTED_EDGE` for the pinned data, not a proof that
another compiler record or a future frame assignment could never provide a
bridge. The exact missing proof/data requirement is a source-pinned mapping
from one producer use and physical word event to source/target rational
frames, a rank factorization and pivot, and the resulting child row class,
array payload, state ownership, and paid return/cleanup path. That mapping
must also prove the common-frame gate invariant and the Section 4 endpoint
identity for the substituted finite network.
