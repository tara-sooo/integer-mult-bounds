# Typed frame boundary audit

**Snapshot:** fork `main` at `0605a24a28836168ad29d6239b46064b892298fc`;
real-construction source pinned to CrocSwap commit
`aa7701b68540b7863d3b66a414e4319915d6282d`. This note follows the source
ledger in `SOURCES.md` and does not copy or modify the earlier issue worktrees.

## Selected child family and recurrence

The bounded target is the width-529 row of the pinned rank-pair bit moment.
The profile constructor in `research/pair-assembly/frame/frame_verify.py`
sets `m = 23·25 = 575` and forms the `h=23` exterior width as `m−2h = 529`.
Its multiplicity is

```text
N / C(23,3) · R23 = 4,073,300 / 1,771 · 27,918 = 64,211,400.
```

The exact profile records `W = 137,151,806`, total rank
`78,860,441,550`, and maximum child width 529. This row contributes to the
single-type sufficient moment

```text
M_b(a) = (1 / (m W)) Σ_t n_t t (m/t)^a.
```

The row has a width and multiplicity, but no child-function identifier. The
certificate therefore names the scalar recurrence cost, not a typed
parent-to-child call.

The finite producer itself is an XOR DAG for the paired-exclusion output
functions. It does not identify a recursive multiplication parent or child
at the width-529 boundary.

## One shared-state candidate

The pinned producer `research/pair-assembly/pair_graph.py` defines this local
sub-DAG in its pair assembly:

```text
FSa = F ⊕ Sa
Y2  = FSa ⊕ Sb2
```

All four values are one-bit GF(2) linear forms. The proposed carrier is the
already-produced scalar `FSa`; its consumer computes `Y2`. The local boundary
function is exactly `(x,z) ↦ (x, x⊕z)`, with `x=FSa` and `z=Sb2`. Its inverse
is the same map, so this local scalar transformation is valid for arbitrary
input values. It is an internal producer-DAG dependency, not a recursive
child call. The source does not identify it with the width-529 row.

## What the physical compiler guarantees

The rank-pair compiler groups scalar DAG nodes by `(core, cover)` frame. It
selects a carrier only when the source frame is contained in the consumer
frame and the output basis permits the retained value. It assigns each
selected use once. When a value is needed more than once, it acquires a role
and emits an XOR to make the copy; the copy is included in the physical word
and rank profile. The compiled word and independent replay check all input
and dirty basis vectors in both orientations, restore dirty roles, and check
frame inclusions.

The pinned rank-pair records are:

| Axis `h` | Roles `R` | Elementary XORs | Rank mass | Checked basis vectors |
|---:|---:|---:|---:|---:|
| 23 | 27,918 | 149,172 | 642,620 | 31,460 |
| 25 | 36,586 | 205,915 | 915,250 | 41,186 |

The basis-vector totals include logical input and scratch-role basis vectors;
they are not counts of scratch bits alone.

These are whole-graph costs. The compiler record does not map a selected
carrier to a recursive child function, nor does the profile map the local
`FSa` edge to any individual child row. Its aggregate frame-inclusion result
does not prove that this exact edge is retained across a width-529 call. In
particular, the width-529 row is formed by the exterior-profile formula
above; the serialized frame artifacts do not label 64,211,400 semantic call
sites or say which input, output, or state each such child owns.

## Boundary fields that are missing

For the selected width-529 family, the pinned files do not specify:

| Required field | Available record |
|---|---|
| Parent logical function | Only the aggregate `m=575` bit recurrence and a finite scalar XOR producer. |
| Child logical function and payload | Only `(t=529, multiplicity=64,211,400)`; no function, input/output tuple, or type tag. |
| Child frame and basis | Aggregate rank histograms and serialized whole-graph frame events; no call-boundary frame attached to a typed child. |
| State creation, transfer, and erasure | The producer DAG has internal scalar carriers, but no operation that exports one across a recursive call. |
| Child ownership and dirty-state contract | Whole-network source/role ownership and arbitrary-dirty replay are checked; no per-child ownership or pre/post contract exists. |
| Per-child physical charge | Paid transitions and copies enter the global role/rank profile; there is no typed child attribution. |

Thus the only source-derived operator is the existing scalar moment. Its sole
type is its sole strongly connected component. No multi-type operator or
dominant typed cycle can be reconstructed from these artifacts, and the
`FSa` carrier cannot be shown to change that scalar row. Treating a width
histogram entry as a semantic state would invent an interface the compiler
does not emit.

This is a falsifiable interface obstruction, not a no-gain theorem: an
immutable producer/compiler record that connects a child width to its
logical function, payload, frame, ownership, dirty contract, and paid
transitions would reopen this comparison.
