# Minimal typed contract for one interchange child

## Type and operation

Let `m`, `W`, and `q` be the fixed constants of the selected Section 4 bit
network and its matrix-shear construction. Let `e=m^k`, with `k>0`, and
`b=e/m=m^(k-1)`. A logical input is a bit array

```text
A : [P] x [R] x S0 x [q^e] x S1 x [q^e] x S2 -> {0,1},
```

where `P,R>=1`, each `S_i` is a finite product of positive spectator ranges
(possibly a singleton), the row field `[R]` precedes both target chunks, and
`W^k` divides `R`. The two `[q^e]` fields are the target chunks; the `S_i`
fields collapse all other address fields while preserving their order.

The parent function `Swap_k` is the address permutation that interchanges
the target chunks and fixes all spectators:

```text
A_out(p,r,s0,d,s1,h,s2) = A_in(p,r,s0,h,s1,d,s2).
```

This equation defines the full payload behavior, including arbitrary values
on rows used as scratch roles. The implementation at `k=0` is the elementary
single-digit interchange. At `k>0`, a selected child is `Swap_(k-1)` on one
pair of `b`-digit subfields and one row class of the parent array.

## One-call precondition and postcondition

**Precondition.** The caller is processing an edge matrix `A_e` of the fixed
network after applying the factorization's scheduled triangular changes.
One pivot `(i,j)` of the fixed partial permutation `Pi` calls `Swap_(k-1)` on
the corresponding `H_i,D_j` fields. The active role stream contains every
row in exactly one class
`r = W g + (w-1)`, with its complete common suffix and its complete
`H,D` address ranges. Its child row range has length `R/W`, divisible by
`W^(k-1)`. Before descent, the parent constructs the child descriptor from
the two target fields and collapsed spectator intervals, pushes its own
descriptor and program counter, parks inactive role streams, and copies the
active stream to the child I/O area. At child entry the reusable work tapes
are empty except for the active I/O and descriptor; stack heads are at their
saved tops. All other fields are spectators.

**Postcondition.** The returned stream has the same finite shape and tape
representation. Every entry is moved by the exact `H_i,D_j` address swap;
all spectator coordinates and payload bits are preserved. The caller can
continue the remaining pivots and triangular changes to realize the edge
shear `Phi_(A_e)`. The parent copies the child output to the active role,
restores and erases the parked streams, and pops the descriptors; it returns
with its work tapes clean and stack heads at their prior tops. Applying the
same child interchange again restores the input stream.

## Field-by-field status

The labels mean `SOURCE-PROVED`, a direct consequence of a pinned source;
`DERIVED`, a bookkeeping or algebraic consequence of that source;
`PROPOSED`, an extension being suggested; and `UNAVAILABLE`, absent from
the pinned source records.

| Field | Minimal contract | Status |
|---|---|---|
| Parent logical function | Exact address transposition `Swap_k` on two `q^e` chunks, fixing all other fields. | `SOURCE-PROVED` |
| Child logical function | Exact address transposition `Swap_(k-1)` on a pivot pair of `q^b` fields in one role stream. | `SOURCE-PROVED` |
| Payload and shape | Complete bit array, row/prefix/suffix shape, arbitrary values, and binary length descriptors. | `SOURCE-PROVED` |
| Recursion parameter | `e=m^k`, child `b=e/m`, and row divisibility `W^k | R` implying `W^(k-1) | R/W`. | `SOURCE-PROVED` |
| Edge and pivot selector | A fixed edge difference `A_e`; a fixed `A_e=E_1 Pi E_2`; one child per `1` in `Pi`, hence `rank_Q(A_e)` children on that edge. A proof-level selector can be derived from the edge and pivot position; it is not a compiler-generated call ID. | `SOURCE-PROVED` for the factorization/count; `DERIVED` for a selector notation |
| Frame and basis | The role frame is `Phi_M`; an edge changes it by `Phi_(M_head-M_tail)`. The local child is expressed in the transformed `H,D` coordinates selected by the factorization. | `SOURCE-PROVED` |
| State/invariant | The current state is the complete active role stream plus its local shape descriptor and stack tops. No extra mutable shared value is an argument to `Swap`. | `SOURCE-PROVED` for the stream/stack invariants; `DERIVED` for the concise state record |
| Ownership/exclusivity | Row classes are disjoint. Children execute sequentially depth first on one active role stream; inactive streams are parked and restored before the parent continues. | `SOURCE-PROVED` |
| Dirty scratch | All logical rows and payload bits may be arbitrary. The exact permutation handles auxiliary-role values without assuming zero scratch. Reusable work tapes are empty, apart from the active I/O/descriptor and stack tops, at the stated boundaries. | `SOURCE-PROVED` |
| Copies and conversions | Row split/merge, triangular updates, child stream copy, parking, pop, reset, and cleanup are charged within `O(V)` at the parent. The source proves this asymptotic bound, not a concrete transition count per copy. | `SOURCE-PROVED` for the bound; exact constants `UNAVAILABLE` |
| Tape representation and cleanup | One fixed finite-alphabet, fixed finite-tape machine; canonical binary descriptors; child descriptor construction; fixed-tape depth-first schedule; parent descriptors and parked streams are popped and erased; reusable work tapes are clean at return. | `SOURCE-PROVED` |
| Paid recurrence | One child contributes `(V/W) F_(k-1)`. The `s` children contribute `(s/W) V F_(k-1)`; all parent work, including stack movement, is `O(V)`. Thus `F_0=O(1)` and `F_k <= (s/W)F_(k-1)+O(1)`. | `SOURCE-PROVED` |
| Extra carried producer token, such as Issue 13 `FSa` | No token is named in the Section 4 child type, and no frozen compiler record identifies it with this child's payload or frame. | `UNAVAILABLE` |
| Mapping `FSa` to an edge/pivot/child | A commuting map from the Issue 13 producer and paid compiler transition to one specific `Swap_(k-1)` call, preserving all frames and charges. | `PROPOSED`; proof/data `UNAVAILABLE` |

## Forgetful projection and cost preservation

Forget the proof-level edge/pivot/role labels and retain the complete array
shape, `Swap_k` function, and its implementation. This is exactly the scalar
interchange contract in Proposition `prop:power-interchange`; the arbitrary
width wrapper is Lemma `lem:chunk-swap`. The projection removes no physical
step: it retains all child contributions `(V/W)F_(k-1)` and all `O(V)`
splitting, frame, stack, copy, and cleanup costs. The contract gives no
free fan-out, conversion, or persistent alias across sibling calls.

For the exact local check, take `m=2`, the rank-one integer matrix
`A=diag(1,0)`, `q=3`, and a one-digit child (`b=1`). Its factorization has one
pivot. On coordinates `(h,d) in (Z/3Z)^2`, the caller uses

```text
d <- d+h;  (h,d) <- (d,h);  d <- h-d
```

and obtains `(h+d,d)`, with the middle operation being the one recursive
field interchange. This local matrix-shear example illustrates the source
rule; it does not assert that `q=3` is the prime selected for the full
million-dimensional network or that the entire network has these toy
parameters.
