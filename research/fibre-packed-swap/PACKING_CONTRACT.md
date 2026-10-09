# Storage type and packing contract

## Original one-fibre type

Fix \(h=6\), \(A,B\), and let \(\mathcal T\) have its 20
third-coordinate triples. At one address, the fibre has 20 independent
\(X_{ABT}\) values and 20 independent \(Y_{ABT}\) values. For
array-valued data, write
\[
\mathcal V=(R^\Omega)^{20}_X\times(R^\Omega)^{20}_Y\times\mathcal Z,
\]
where \(R=\mathbb F_2\) for the bit circuit or
\(R=\mathbb Z[i,1/2]\) for the complex circuit, and \(\Omega\) is the
corresponding address set. \(\Omega\) includes any address spectators,
but not the role index \(T\). No values are assumed equal. The state
\(\zeta\) contains every side, center, scratch, and external spectator
value, with no cleanliness assumption.

The source manuscript assigns \(X_a\) source/sink labels
\((U_a,\mathcal F)\), \(Y_a\) labels \((0,U_a^\perp)\), and each
scratch role labels \((0,\mathcal F)\). These are role-specific endpoints.

## Reversible lane reindexing that was screened

Keep \(T\) as an outer lane tag. Define
\[
E(X,Y,\zeta)=(\widetilde X,\widetilde Y,\zeta),\qquad
\widetilde X(T,\omega)=X_T(\omega),\quad
\widetilde Y(T,\omega)=Y_T(\omega),
\]
where \(\widetilde X,\widetilde Y\in R^{\mathcal T\times\Omega}\). Define
\[
D(\widetilde X,\widetilde Y,\zeta)
=((\widetilde X(T,\cdot))_{T\in\mathcal T},
  (\widetilde Y(T,\cdot))_{T\in\mathcal T},\zeta).
\]
Then \(D\circ E=\mathrm{id}\) for all 40 independent arrays and
all arbitrary dirty \(\zeta\). No lane is identified, summed, or
initialized. The checker uses distinct values in every lane and a
distinct dirty-scratch sample; the identity \(D\circ E=\mathrm{id}\)
holds for an arbitrary scratch tuple by definition.

This is a lossless storage encoding, but it is only a reindexing of the
direct sum. It supplies no operation between the endpoints. The signed
logical contract remains, separately for every \(T\),
\[
(X_T,Y_T,\zeta)\longmapsto(-Y_T,X_T,\zeta),
\]
and the bit full-array Swap must still exchange the two address chunks
on every original role, restore row order, and return every arbitrary
scratch value. \(E\) and \(D\) perform neither operation.

## Width and role count

With scalar roles, \(T\) remains a role tag: \(m'=m=216\), and all 40
data roles and all scratch roles remain in the scalar network. The
existing one-invocation \(h=6\) counts are 226 bit roles and 247 complex
roles; the counts are detailed in COST_GATE.md.

If the 20 \(X\) lanes and 20 \(Y\) lanes are treated as two aggregate
vector-valued roles, the storage view has 2 data containers, each 20
lanes wide, and the side/center scratch roles stay separate. Its total
number of stored values is unchanged. The paper's scalar-wire gate and
recurrence do not accept a vector-valued role as one wire, so this does
not define a legal \(W'\). The nominal local role count would be 188 bit
containers or 209 complex containers after replacing the 40 data roles
with 2; these are not legal scalar-wire counts. One can keep the lane as
an external finite address field and retain \(m'=216\); putting 20 lanes
inside each address chunk as five binary address bits instead gives
\(m'=221\), but leaves 12 padding lanes. Those lanes cannot be zeroed if
they carry arbitrary dirty state.

For a faithful scalar implementation \(W'=W\). For a flattened layout,
the nominal container count is smaller but the scalar gate type and
recurrence schema change. No \(W',m',s'\) recurrence has been proved for
that schema.

## Why this is not the requested typed operation

The lane map's action on an independent adapter is
\(E(P_{AB}^{\oplus 10})E^{-1}\). That is an invertible relabeling of the
same operation, with the same rank. A useful packed-fibre construction
would need a different operation on the lanes, its source and sink
frames, its role routing, and an inverse decoder that restores all dirty
scratch. No such operation is supplied here. In particular, a label
map on the \(m\)-dimensional \(\mathcal F\)-space is not itself a
transform on the array values in \(R^\Omega\).
