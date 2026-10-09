# Paid cost gate

## Type-indexed recurrence

Let T(n,b) be worst-case bit/tape time for length-n convolution when
each input coefficient is a signed integer of at most b bits. A child
formed by adding two coefficients has at most b+1 bits. Let M(t) be
the cost of multiplying two t-bit integers at the base case. The
construction gives
\[
T(1,b)=M(b),\qquad
T(n,b)\le 3T(n/2,b+1)+C n(b+\log n)
\quad(n>1,\ n\text{ a power of two}).
\]
The parent term includes the two input sums, child-input copies, all three
child outputs, coefficient additions/subtractions, output initialization,
and clearing the temporary buffers. Child outputs have O(b+log n)
bits per coefficient. No copy, decode, or cleanup is free.

Use signed fixed-width binary slots for coefficients. A call on n
coefficients of at most b bits needs slot width
w=O(b+log n): along any descendant path input sums add at most log n bits,
and each output coefficient sums at most n products. Fixed slot widths let
the routine stream aligned coefficients without searching for delimiters.

A fixed-tape depth-first schedule stores each parent frame contiguously on
work tapes. It appends one child frame, copies the selected input blocks to
that frame, runs the child, copies its returned coefficients back, and pops
and clears the child frame before the next child. The parent retains p0
and p2 in its own frame while p1 runs. A descriptor stack records
the node size and child phase. Its O(log^2 n) total bits and scans are
absorbed by the parent scan bound. The number of tapes is fixed; none is
allocated per recursion depth. Each parent scans O(nw) bits across its
input sums, copies, outputs, initialization, decoding, and cleanup.

At recursion depth j, there are 3^j nodes of width n/2^j. The
total parent work at that depth is
O(n(3/2)^j(b+log n)). With alpha=log_2(3), summing levels and leaves gives
\[
T(n,b)=O\left(n^\alpha
  (M(b+\log n)+b+\log n)\right).
\]
The depth-first live frames occupy O(n(b+log n)) bits. For binary digits
and grade-school base multiplication M(t)=O(t^2), this is a fixed-finite-tape
O(n^(log_2(3)) log^2 n) algorithm for the coefficient convolution,
followed by O(n log n) tape time for carries.

This is an upper bound in the stated clean-workspace model. Zero-padding
and truncating non-power-of-two lengths cost O(n(b+log n)); padding grows
the input length by less than a factor of two. It does not implement
arbitrary-dirty scratch restoration, and it does not claim a new tape
compiler for the source manuscript's address arrays.

The assumptions are kept separate: the polynomial identity and binary carry
recovery are proved here; clean-buffer initialization and fixed-tape stack
movement are paid by the schedule above. No inherited bit circuit, complex
frame, physical endpoint, approximation precision, prime selection,
uniformity theorem, or arbitrary-dirty restoration claim is used. The fork's
current kappa witness retains those separate conditional obligations.

## Same-model independent-child baseline

The direct split computes all four block products independently:
\[
U(1,b)=M(b),\qquad
U(n,b)\le4U(n/2,b)+C n(b+\log n).
\]
For binary digits with constant-size leaf products this is O(n^2).
The joint formula changes the paid child count from four to three at every
binary split, reducing the exponent from 2 to
log_2(3) approximately 1.584963. This is a genuine nonvanishing saving over
that baseline, but it is the established Karatsuba saving.

It is not a saving against the fork's current conditional witness
O(N(log N)^(1-kappa)), with
kappa=971668963/25000000000000, pinned at fork commit
0605a24a28836168ad29d6239b46064b892298fc. The pilot's
O(N^1.584963 log^2 N) cost is asymptotically larger. Substituting the
current best integer multiplier at the leaves still leaves the
N^1.584963 factor.

## Source-recursion comparison

At the original manuscript pin, Section 3 has h=100, m=h^3=10^6,
and a fixed wire network whose scalar source/target banks are indexed by
triples. Section 4 implements full-array coordinate interchange on shapes
[P] x [2^u] x [G] x [2^u] x [B], swapping the two 2^u fields and
preserving every other field. One call has volume V; the edge-rank sum s
gives s child calls, each on a full stream of volume V/W, and the proved
normalized recurrence is
\[
F_0=O(1),\qquad F_k\le(s/W)F_{k-1}+O(1).
\]
The source's bit network has
W=177176569091445000000 and
s=177176569088785861287000000. Its O(V) parent charge explicitly
includes role parking, child input/output copies, shape processing, fixed
tape movement, and restoring parked streams. The Section 4 child is an
array interchange, not a polynomial convolution.

The three Conv_(n/2) calls here cannot be inserted as s=3, or credited with
the source's V/W volume ratio. Their input and output spaces, recursion
parameter, and per-parent costs differ. The pilot proves no change to that
rank moment or to any current kappa certificate.

## Variable-arity conjecture and cost obstruction

A distinct next family would split into r blocks and use 2r-1 evaluation
products instead of r^2 independent block products. Algebraically its
fixed-arity child exponent would be
\[
\alpha_r=\log_r(2r-1)
=1+\log_r(2-1/r)\longrightarrow1.
\]
**Falsifiable conjecture:** there is an r=r(n) tending to infinity
evaluation family whose exact integer encoding, interpolation, child
coefficient growth, workspace clearing, and fixed-tape movement all fit a
paid recurrence below O(n(log n)^(1-eta)) after carry recovery, with
eta >= 10*kappa_0 and kappa_0=971668963/25000000000000. This is a
tenfold exponent target against the pinned witness. The required property
is a structured decoder whose cost does not grow like dense O(rn)
interpolation while retaining the 2r-1 child count.

The direct dense-matrix implementation already fails this target. To make
the leaf factor n^(alpha_r-1) polylogarithmic requires
r >= exp(Omega(log n/log log n)); direct dense evaluation and interpolation
then take Theta(rn) coefficient operations per level, exceeding n log n.
This is not a lower bound against structured transforms. It identifies the next lemma: either give a
uniform structured decoder and tape schedule with proved coefficient-height
bounds, or prove a lower bound for that explicit family. The original
manuscript's synthetic transform route is a known comparison, not evidence
that this new joint family exists.
