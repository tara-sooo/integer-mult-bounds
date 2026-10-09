# Two actual Section 4 pivot calls

## Selected scope and parent shape

The source-backed edge is the stage-3 central wire `C_1` in the invocation
whose two fixed triples are both `T0={1,2,3}`. Its consecutive endpoints are
the time-1 subtract-scatter gate and time-3 gather gate. The exact matrices
and factorization are in `SOURCE_BRIDGE.md`.

Use the original Section 4 construction with `m=100^3=1,000,000`, and choose
the legal parent level `k=2`. Write `e=m^2=10^12` radix-`q_*` digits and
`b=e/m=m=1,000,000` digits per child field. Here `q_*` is the fixed odd prime
chosen by the paper's finite denominator table; its numerical value is not
printed. The minimal parent shape that meets the row condition is

```text
row field [W^2] ; H chunk [q_*^e] ; D chunk [q_*^e] ;
W = 177176569091445000000,
V = W^2 q_*^(2e).
```

There are no extra prefix or suffix fields in this representative shape.
After the root splits rows into `W` role streams, the selected `C_1` row class
has `W` rows and all `2m` digit fields remain present. Its volume is
`V/W = W q_*^(2e)`. `H_1,...,H_m` and `D_1,...,D_m` each range over
`[q_*^b]`. All fields other than the current pair are full spectators.

The source does not assign a global integer wire number to `C_1`. The exact
row split is `r=Wg+(w-1)`, where `w` is the numeric index of this role in a
wire enumeration and `g=0,...,W-1`; the paper leaves that enumeration open.
The exact row class is therefore identified by its stage, fixed triples, and
center-wire name, without inventing a numeric `w` or synthetic call number.
The tensor coordinates below use the explicit lexicographic order fixed in
`SOURCE_BRIDGE.md`.

## Shared parent edge and call records

| Source occurrence key | Edge / pivot | Recursion | Target fields | Child input shape |
|---|---|---|---|---|
| stage 3, fixed `(T0,T0)`, wire `C_1`, time `1 -> 3`, first `Pi` one | matrix row 1, column 999901; tensor pair `((1,1),(10000,1))` | parent `Swap_2`, child `Swap_1` | `H_1`, `D_999901` | `[W] x [q_*^b]^(2m)`, with these two fields active |
| stage 3, fixed `(T0,T0)`, wire `C_1`, time `1 -> 3`, second `Pi` one | matrix row 2, column 999902; tensor pair `((1,2),(10000,2))` | parent `Swap_2`, child `Swap_1` | `H_2`, `D_999902` | `[W] x [q_*^b]^(2m)`, with these two fields active |

These are not IDs copied from a run log: they are the first two calls generated
by the explicit valid factorization and row-major pivot order above. All `Pi`
ones use disjoint rows and columns, so this ordering is a valid execution
order. In particular, both calls have the same rank-one pivot count, child
width, row class, full array shape, and parent edge.

## Complete live state and chronology

Let `Z` be the arbitrary dirty bit array initially on this scratch role. It
has one bit at every address; no scratch bit is assumed zero. The first edge
of this wire takes it from source frame zero to the time-1 frame. The time-1
gate leaves `C_1` unchanged, and the time-2 gate does not touch it. Thus the
complete stream entering the selected edge is

```text
Z_tail = Phi_((I-P) tensor I_100)(Z),
```

including every bit at every address. The edge implementation first applies
the two lower-triangular address transforms
`H <- E_1^-1 H` and `D <- E_2 D`; call the resulting complete state `Z_0`.
They are invertible, and all role rows, all `H` and `D` fields, and every
arbitrary payload bit remain part of this state.

For a pivot `(i,j)`, Section 4 performs, in order,

```text
D_j <- D_j + H_i;
Swap_(k-1)(H_i,D_j);
D_j <- H_i - D_j.
```

The complete first child input is the state `Z_1` obtained by applying the
first update `D_999901 <- D_999901 + H_1` to `Z_0`. The first child's output
is copied back to the active `C_1` stream, then the last update completes the
first pivot. The complete second child input `Z_2` is obtained from that
updated stream by `D_999902 <- D_999902 + H_2`. There are no intervening
writes to `C_1` other than the first pivot's stated address operations.

For clarity, let `S_(i,j)` be the address map `D_j <- D_j+H_i`, let
`T_(i,j)` be `H_i <- H_i+D_j` (the complete three-operation pivot), and let
`move_T` move every array bit according to address map `T`. The exact child
entrance states are

```text
Z_1 = move_S_(1,999901)(Z_0),
Z_2 = move_S_(2,999902)(move_T_(1,999901)(Z_0)).
```

Thus the second entrance frame includes the completed first pivot. Both
states have the same full shape and spectator ranges, while their address
maps are different functions of the arbitrary payload; the exact separator
is in `EQUALITY_TEST.md`. A child exits with its target pair swapped and all
other fields preserved. The edge's completed output is `Phi_I(Z)` at the
time-3 gate frame. The two child outputs are sequential intermediate states
in that one stream, not two independently owned logical values.

## Owners and consumers

The parent recursion owns the active `C_1` row stream. At each child boundary,
the Section 4 fixed-tape schedule parks the other `W-1` role streams, copies
the active stream into child I/O, erases the parent copy, and pushes a
descriptor. On return it copies the child's full bit-array output back into
the active role and restores the parked streams. The first child output is
consumed by the final affine update of pivot 1 and then the next pivot's
pre-update. The second child's output is consumed by pivot 2's final affine
update and the remaining edge program. The completed edge output is consumed
by the time-3 gather gate. No second consumer requests the first child's
unmodified output.

The role's dirty state and all address spectators are preserved by the
source's arbitrary-array contract. Their storage and movement are included
in the parent schedule; the child return is not a free alias or a scalar
cache entry.
