# Typed joint-recursion reduction

**Checkpoint:** the joint split identity below is exact, but its cost is too
large to improve the current integer-multiplication bound. It is the
classical Karatsuba identity written as a typed convolution operator; no
priority or new-algorithm claim is made.

## Semantic target and source boundary

For the pilot, \(R=\mathbb Z\) and
\[
\operatorname{Conv}_n(a,b)[k]=\sum_{i+j=k}a_i b_j
\quad (0\le k<2n-1).
\]
For n=2m, the typed maps are
E^A_n,E^B_n: Z^n -> (Z^m)^3,
P_n: (Z^m)^3 x (Z^m)^3 -> (Z^(2m-1))^3, and
D_n: (Z^(2m-1))^3 -> Z^(2n-1), with
\[
D_n(P_n(E^A_n(a),E^B_n(b)))=\operatorname{Conv}_n(a,b).
\]
At n=1 the child operator is integer multiplication. The family is defined
for powers of two; for other lengths, zero-pad to the next power of two,
then truncate the decoded output to 2n-1 coefficients. Both operations are
linear in the padded length and paid.

The pinned manuscript claims deterministic
O(N(log N)^(1-2^-182)) time on a fixed finite-alphabet multitape machine.
At the fork's starting commit, the accepted conditional witness is
O(N(log N)^(1-kappa)), where
kappa=971668963/25000000000000. These are distinct evidence levels.

The original manuscript's Section 3 instead takes two data banks X,Y,
each indexed by triples of three-element subsets, together with scratch
wires whose initial values are arbitrary. Its exact scalar output is
(X,Y,scratch) -> (-Y,X,same scratch). Section 4 lifts that network to a
full-array coordinate interchange: it swaps the two designated address
chunks and preserves every spectator field. Its recursive children are
full array streams of volume V/W, counted by matrix ranks, and its
normalized recurrence is F_k <= (s/W)F_(k-1)+O(1). A polynomial
coefficient convolution child has neither that array type nor that rank
ledger. This pilot does not replace or modify the Section 4 recurrence.

The fork's current kappa witness is conditional on the inherited manuscript
framework and its own bit/complex profiles, physical frames, precision,
prime, exact-recovery, uniform-machine, and all-size obligations. This
pilot imports none of those claims. Its only integer-transfer step is the
explicit binary carry proof in PILOT.md; it requires no modular or complex
arithmetic.

## Architecture A: share the cross term at decomposition

Let n=2m, split
\[
a(x)=a_0(x)+x^m a_1(x),\qquad
b(x)=b_0(x)+x^m b_1(x),
\]
where each block has length m. Define
\[
E^A_n(a)=(a_0,a_1,a_0+a_1),\quad
E^B_n(b)=(b_0,b_1,b_0+b_1).
\]
The joint operator makes three genuine smaller calls:
\[
P_n(E^A_n(a),E^B_n(b))=(p_0,p_2,p_1),
\]
where
\[
p_0=\operatorname{Conv}_m(a_0,b_0),\quad
p_2=\operatorname{Conv}_m(a_1,b_1),\quad
p_1=\operatorname{Conv}_m(a_0+a_1,b_0+b_1).
\]
The decoder returns
\[
D_n(p_0,p_2,p_1)
=p_0+x^m(p_1-p_0-p_2)+x^{2m}p_2.
\]
At n=1, the encoder and decoder are identities and P_1 is one
integer multiplication. This is a joint operation from the split itself:
the summed-input child supplies both cross products. It does not reuse
completed children or relabel their types.

**Proposed saving:** four independent block products become three half-width
convolutions at every split.

**Cheapest fatal checks:** compare the full n=4 bilinear coefficient
tensor against the target and check that the claimed child really has
smaller coefficient-array width. Both checks pass. The paid recurrence then
shows the limit: its exponent is log_2(3), which is worse than the
current near-linear-in-N integer bound.

## Architecture B: exact modular transform batch

For binary input vectors, the types are
E^A_n,E^B_n: {0,1}^n -> F_p^L,
P_n: F_p^L x F_p^L -> F_p^L, and
D_n: F_p^L -> Z^(2n-1). Choose a power-of-two transform length
L >= 2n-1, a prime p with L | (p-1), and a root omega in F_p of
exact order L. Pad each input with zeroes and let E^A,E^B evaluate at
1,omega,...,omega^(L-1). Let P multiply the L values coordinatewise,
and let D apply the inverse transform and take canonical integer residues
of the first 2n-1 coefficients. This gives linear convolution modulo p.
For binary coefficient inputs, 0 <= c_k <= n; choosing p>n makes those
canonical residues equal the exact integer coefficients, after which
ordinary binary carries recover the integer product.

**Proposed saving:** transform diagonalization replaces n^2 scalar
products by L=O(n) pointwise products; the transforms cost
O(n log n) field operations.

**Cheapest fatal checks:** first prove a uniform fixed-alphabet method for
choosing p,L,omega, then charge transform, residue recovery, carries,
and all tape movement. A finite F_17 example is easy but does not settle
that gate. The pinned manuscript already uses a synthetic transform
pipeline and exact recovery, so this is a comparison architecture,
not a new theory selected for the pilot.

## Selection

Architecture A is selected because it is the smallest exact operation that
tests the Issue's leading hypothesis: related child products are combined
before recursion begins. Its typed map is over Z, with no
modular, Gaussian, or dyadic identification. Unlike the fixed-profile
switching toy in [Issue 11](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/11)
and cooperative Boolean toy in
[Issue 12](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/12),
it changes the child-work multiset at decomposition. Unlike [Issue 30](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/30),
it starts with a typed multiplication input/output. It is not a
basis-changed coordinate-star or a free source/target relabel. The selection
is for a bounded falsification pilot, not a forecast of a better kappa. The result
confirms the identity and rejects this fixed binary split as a route to a
better integer-multiplication exponent.
