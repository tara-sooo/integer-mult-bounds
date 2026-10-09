# Paid recurrence and comparison

## Type and recurrence

For powers of two \(n\), let \(J(n)\) be the fixed-tape cost of the
selected full-product routine. At \(n=1\), multiply the two bits directly.
For \(n=2m\), call four exact \(m\)-bit multiplications, form the cross
sum, extract \(q=\lfloor p_{00}/2^m\rfloor\), and return the low \(m\)
bits and the remaining \(3m\) bits. The paid recurrence is
\[
J(1)=O(1),\qquad J(n)=4J(n/2)+O(n).
\]
The parent term includes all encoding, addition, result movement,
initialization, clearing, descriptor, and head-return work below. Thus
\(J(n)=\Theta(n^2)\) for this recursion with one-bit leaves; there are
exactly \(n^2\) scalar multiplication leaves. Padding to the next power
of two and trimming the padded high zero bits costs \(O(n)\) and changes no
exponent.

## Complete parent ledger

At a parent with \(n=2m\):

- Splitting reads the \(2n\) input bits and writes \(2n\) half-buffer bits.
  The four child calls receive \(8m=4n\) argument bits; those source
  bits are reread and \(4n\) destination bits are copied into reusable
  child-input slots.
- Each child returns \(2m=n\) bits. The parent reads/copies all four
  outputs, \(4n\) bits total. \(p_{00}\) is retained because its low
  half is the low window and its high half is \(q\). The \(p_{01},p_{10}\)
  values are accumulated in a \(2m+1\)-bit cross-sum slot; \(p_{11}\) is
  retained for the high window.
- The parent performs \(O(n)\) bit additions and carry steps to form
  \(L,H\), and writes \(2n\) output bits. The state \(q\), of width \(m\),
  is a slice of the already returned \(p_{00}\); reading or transporting
  that slice is still included in the parent scan.
- A sequential schedule needs \(O(n)\) bits for retained products, the
  cross sum, one reusable child input/output frame, and output staging.
  It zeroes the accumulator and fresh buffers before use and clears them
  before reuse. Initialization and cleanup each cost \(O(n)\).
- Eight binary tapes suffice: input, output, parked parent frames, child-A
  input, child-B input, child result, arithmetic/accumulator, and call
  descriptors. A depth-first schedule parks the parent frame, copies a
  child frame, runs that child using the same tapes, returns its output,
  and clears the child region before the next call. Marked local endpoints
  bound head returns to the current frame; no random access or scan to an
  ancestor's maximum address is assumed. Parent-frame movement is
  \(O(n)\) per child, and the descriptor stack uses \(O(\log n)\) bits.
  The live geometric stack is \(O(n)\) bits.

The four recursive calls are counted once each. The quotient is not
credited as a free state, and no complete child is subtracted because some
of its output is shared. The boundary theorem in SEMANTICS.md also shows
that a carry-only message at a general cut can require linear-in-cut width.

## Same-output conventional control

The direct two-block decomposition of one complete product already makes
the same four calls and uses the same shifted-sum identity. It emits both
adjacent windows from the one resulting product. Its paid recurrence is
therefore exactly \(4J(n/2)+O(n)\), with the same copied child inputs,
returned child bits, parent additions, and carry state. Candidate A has no
work reduction against this same-output baseline; the state names a value
the ordinary decoder already has to form.

Calling separate full multiplication routines once for each window would
be a deliberately wasteful comparison. A fair window-only baseline may
use truncated or middle-product algorithms, which compute only the
requested range. We have not proved that the joint recurrence beats the
best such separate routines, and do not claim that it does. Harvey's
truncated integer result applies under a real-cyclic-convolution
assumption; the polynomial middle product has its own coefficient-window
contract. Neither supplies a new carry-state theorem for this candidate.

For comparison, the pinned Issue 31 Karatsuba recurrence has three
half-size products and exponent \(\log_2 3\), but is still asymptotically
larger than the fork's current conditional near-linear witness. Candidate
A has four children and is no better even than schoolbook. The fork's
current witness is conditional on the inherited fixed-tape framework and
has \(\kappa_0=971668963/25000000000000\) at the starting fork commit.
The pinned manuscript separately states \(\kappa=2^{-182}\); neither
exponent is transferred to this pilot.

The original manuscript charges its own source/target interchange as
recursive full-array streams with an explicit fixed-tape parking and
movement schedule. These \(m\)-bit integer products have a different
input/output type and recurrence. There is no typed bridge from \(J(n)\)
to that array-volume recurrence, so no \(\kappa\) improvement follows.
