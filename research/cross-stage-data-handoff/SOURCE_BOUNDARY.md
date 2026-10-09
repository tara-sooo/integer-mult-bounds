# Source boundary and real stage 1 → 2 data flow

## Frozen interface

The source is the manuscript snapshot `openai/math` at commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`, Sections 3 and 4. Its production
parameters are `h=100`, `T=binom([h],3)`, `|T|=161700`, and `m=h^3=1,000,000`.
This checkpoint specializes its formulas to `h=10` for an exact finite
fixture. No `h=10` saving is projected to the production parameter.

The data roles are `X_a,Y_a` for `a=(a1,a2,a3) in T^3`. Stage `j` fixes the
other coordinates and varies coordinate `j`; there are `|T|^2` invocations
per stage. Every invocation has private side and center scratch, initially
arbitrary. The completed forward invocation has the typed identity
`J V + R G = I`, so it adds its source bank to its target bank and restores
that invocation's scratch.

The complex path uses coefficients in `Z[i,1/2]`. Its center coefficient is
`(|S∩T|-1)/2`; the side path cancels that value for distinct triples with
intersection 0 or 2. The bit path is separately defined over `F2`; its center
coefficient is `|S∩T| mod 2`, and its side path cancels the intersection-one
case. The checker builds each path independently. It never reduces the
complex dyadic coefficients modulo two.

Section 4's bit supplier charges each actual edge by
`rank_Q(M_head-M_tail)`. It requires the common gate frames, the signed role
permutation on **all** roles, the endpoint equation
`M_out(rho(w))-M_in(w)=I_m`, and `s=sum_e rank_Q(M_head-M_tail)<Wm`.
Its recurrence is `F_k <= (s/W) F_(k-1) + O(1)`. A local involution alone
does not establish this frame theorem. Each rank-one pivot child receives
the entire active stream with every other address field as a spectator. The
parent also pays to park inactive roles, copy/erase the active stream, return
the child output, restore parked streams, and process fixed-tape descriptors.
The theorem's full-array endpoint follows only after those all-role frames,
signs, role routing, and row restoration are verified.

## The typed handoff in the full `T^3` semantics

Write the bank values immediately before stage 1 as `X0,Y0`. The completed
stage operations are

```text
stage 1: Y1 = Y0 + X0;       X1 = X0
stage 2: X2 = X1 - Y1;       Y2 = Y1
stage 3: Y3 = Y2 + X2;       X3 = X2
```

Thus `X2=-Y0` and the endpoint is `(X3,Y3)=(-Y0,X0)`. In the bit network,
minus equals plus and the endpoint is `(Y0,X0)`.

The stage-1 output `Y1_a` has one owner: the existing data role `Y_a`. Stage 2
reads it as its logical source while updating `X_a`; stage 2 leaves `Y_a`
unchanged. Stage 3 then reads that same value as the old target before writing
`Y3_a`. The consumers are sequential. There is no added copy or intermediate
role. Every stage completes its own inverse cleanup before the next stage,
and scratch roles are disjoint between invocations.

The paper's frame calculation gives matching outgoing and incoming data
labels at each stage boundary. For `j<3`, setting `A'=A⊗F` and
`P'=P⊗<t>` makes `B'=(P')^perp`; the outgoing `X,Y` labels are exactly the
next stage's incoming labels. The prescribed source and sink labels remain
`X: U_a → F` and `Y: 0 → U_a^perp`; `rho` exchanges `X_a,Y_a` and fixes every
scratch role. This checkpoint changes none of those frames or endpoints.

For a concrete full-array consumer, take `S={0,2,4}` and `a=(S,S,S)`, an
address in the original `T^3`. Put `X0_a=1,Y0_a=0` and all other data values
zero. Stage 1 writes `Y1_a=1`; stage 2 reads that value and writes `X2_a=0`;
stage 3 reads `Y1_a` as its target value and leaves `Y3_a=1`. The exact check
also covers all 120 possible coordinate triples at `h=10`, not only this
witness.

## The p=5, h=10 local paired-cube block

With pairs `{0,1},{2,3},{4,5},{6,7},{8,9}`, a local port chooses one element
from each of three distinct pairs. There are
`8*binom(5,3)=80` ports, arranged as ten complete eight-selector cubes. The
full source type has `binom(10,3)=120` triples; the 40 triples containing a
whole pair are outside this local block.

On the 80 local ports, the frozen paired-cube coefficients are
`B[T,S]=(|T∩S|-1)/2`, `B_block` is its within-cube restriction,
`K=I-B_block`, and `H=B_block-B`. Exact checks give `K+H+B=I`, `K^2=I` on
each cube, and binary-orthogonal support for every nonzero off-diagonal
`K,H` entry. Coordinate-star gather/scatter reproduces `B` exactly. These
are local algebra checks. They do not assign the 40 omitted triples to
cubes or define a new full-array frame supplier.

The original Section 3 formula itself is also checked separately on all 120
triples at `h=10`. This verifies its full local invocation identity and the
three-shear data action for the h=10 `T^3` array. A bridge from a changed
80-port paired-cube construction to all of `T^3` would still need a typed
cover for the 40 omitted triples, complete ordered source-target incidence
accounting, arbitrary-dirty restoration, stage-boundary frames, and a full
paid child ledger. No such new cover is asserted here.

## Prior stop controls

- [Issue 25](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/25),
  result at
  [commit 520203231ff0de8d9c3121c924ed4fce398c8f69](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/520203231ff0de8d9c3121c924ed4fce398c8f69),
  found the tested cross-stage route twist nonorthogonal (`e8` lies in both
  active blocks with norm one). Under unchanged source/target/gauge child
  multisets, a pure stage permutation preserves the child histogram and
  moment. This checkpoint keeps the original order and makes no route twist.
- [Issue 23](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/23),
  result at
  [commit 267c24dfa448fbf43fa68b7d2cfdd5f9580be458](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/267c24dfa448fbf43fa68b7d2cfdd5f9580be458),
  separated two real equal-rank Section 4 child calls by a one-hot full-input
  witness. Their complete payloads and active field pairs differ, so neither
  child can be reused in that tested pair.
- [Issue 30](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/30),
  result at
  [commit 78f4a20fa1be5fb7366ae93c808a93d191491472](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/78f4a20fa1be5fb7366ae93c808a93d191491472),
  found no source-typed decoder for a five-pair port. The present fixture
  retains three-element ports and treats the 80-port cube calculation only
  as a local block.

These controls are scoped to their frozen candidates. They do not rule out a
changed full-array data itinerary with a newly proved decoder and a different
paid child multiset.
