# Adjacent product windows with a carried residual

**Status:** `KNOWN_EQUIVALENCE_ONLY`, with a scoped lower bound on residual
width. This is a falsification pilot, not a faster multiplication claim.

## Exact product and carry semantics

For binary inputs
\[
A=\sum_{i=0}^{n-1}a_i2^i,\qquad B=\sum_{i=0}^{n-1}b_i2^i,
\]
the raw integer coefficients are
\[
c_t=\sum_{i+j=t}a_ib_j,\quad 0\le t<2n-1.
\]
Exact binary recovery starts with \(q_0=0\) and uses
\[
d_t=(c_t+q_t)\bmod 2,\qquad
q_{t+1}=\left\lfloor(c_t+q_t)/2\right\rfloor.
\]
The invariant is
\[
\sum_{h<t}c_h2^h=\sum_{h<t}d_h2^h+q_t2^t.
\]
Thus \(q_t\) is precisely the information from the processed prefix that
the unprocessed suffix needs. The candidate below computes its child
products explicitly; it does not receive the \(c_t\) values as free input.

## Candidate A: two adjacent windows and a nonlinear state

Let \(n=2m\), and split each input into two \(m\)-bit words:
\[
A=A_0+2^mA_1,\qquad B=B_0+2^mB_1.
\]
The parent calls four strictly smaller, fully specified integer products:
\[
p_{ij}=\operatorname{Mul}_m(A_i,B_j)\in[0,2^{2m}),\qquad i,j\in\{0,1\}.
\]
Each child receives two \(m\)-bit words and returns its complete
\(2m\)-bit product. No coefficient convolution or child output is assumed
to exist before the call.

Define the adjacent output windows at the low-operand boundary \(m\):
\[
L=p_{00}\bmod 2^m,\qquad q=\left\lfloor p_{00}/2^m\right\rfloor,
\]
\[
H=q+p_{01}+p_{10}+2^mp_{11}.
\]
The typed parent returns \((L,H,q)\), with \(L\) exactly \(m\) bits,
\(H\) exactly \(2n-m=3m\) bits, and \(q\) an \(m\)-bit residual.
The full \(2n\)-bit product is recovered by
\[
AB=L+2^mH.
\]
Indeed,
\[
p_{00}+2^m(p_{01}+p_{10})+2^{2m}p_{11}
=L+2^m(q+p_{01}+p_{10}+2^mp_{11}).
\]
The lower child is shared across the boundary: its low bits form \(L\),
and its high bits are the state \(q\) used by the high window. The high
window is fully specified by \(H\); it is not a residual oracle for the
rest of the product.

The map \(p_{00}\mapsto(p_{00}\bmod 2^m,\lfloor p_{00}/2^m\rfloor)\) is
nonlinear over \(\mathbb Q\). This changes the Issue 32 premise that every
child is a full \(\operatorname{Conv}_m\) and that pre- and post-maps are
rational-linear. It does not show lower cost. The four children and the
boundary carry are exactly ordinary two-block schoolbook multiplication.

## Scoped residual-width theorem

Fix \(k\ge2\). Suppose a low-side computation handles the low \(k\) input
bits and sends a state \(S(A_0,B_0)\) to a high-side computation. The
high-side computation receives only \(A\mathbin{\gg}k\),
\(B\mathbin{\gg}k\), \(k\), and \(S\); it cannot reread low input bits or
recompute their product. The low output bits already written are not part
of \(S\).

When both high input parts are zero, the required high output is
\[
\left\lfloor A_0B_0/2^k\right\rfloor.
\]
Taking \(A_0=2^k-1\) and \(B_0=x\), for \(x=1,\ldots,2^k-1\), gives
every value \(0,\ldots,2^k-2\). Equal states must therefore imply equal
quotients, so the state has at least \(2^k-1\) values and needs at least
\(\lceil\log_2(2^k-1)\rceil=k\) bits. On a fixed finite alphabet this
also requires \(\Omega(k)\) cells and serial transport.

This rules out only a residual whose width is bounded independently of
\(k\), under the stated no-reread/no-recomputation interface. It does not
rule out growing states, access to low operands, or other child types.

## Candidate B: one transformed full convolution

As a comparison architecture, choose a power of two \(L\ge2n-1\) and a
prime \(p>n\) with \(L\mid p-1\). Pad the binary digit vectors to length
\(L\), evaluate both polynomials at the \(L\)-th roots of unity in
\(\mathbb F_p\), multiply pointwise, and apply the inverse transform. The
typed child state is \(\mathbb F_p^L\), and the decoder returns all
\(2n-1\) convolution coefficients. Since \(0\le c_t\le n<p\), the
canonical residues are the exact coefficients; the carry recurrence then
returns both output windows.

Its finite check is the exact transform identity plus \(p>n\) and root
order \(L\). It is a standard transform route, and the pinned manuscript
already uses a synthetic transform pipeline. It is a control, not the
selected carry-state mechanism or a new result.

## Relation to known multiplication methods

- **Schoolbook multiplication:** the selected recurrence computes all four
  block products once and adds their shifted values. It is precisely
  recursive two-block schoolbook multiplication with its output split at
  bit \(m\). A digit-by-digit carry pass has the same role; changing the
  carry representation does not reduce the child count.
- **Karatsuba:** replaces those four products with three products on
  \((A_0,B_0)\), \((A_1,B_1)\), and \((A_0+A_1,B_0+B_1)\), then subtracts
  the diagonal products to recover the cross term. That is the pinned
  Issue 31 identity. Candidate A uses four direct products and no
  interpolation.
- **Toom–Cook:** splits into more blocks, evaluates at points, recursively
  multiplies the evaluations, then interpolates. Candidate A instead uses
  the raw four block pairs and the exact carry quotient above; for two
  blocks, the three-product evaluation version is Karatsuba.
- **Truncated and middle products:** these compute a requested low, high,
  or middle portion and may use specialized convolution or transposition
  algorithms. Candidate A returns the *same two adjacent windows together*
  by computing the ordinary full product. No saving against the best
  separately computed truncated tasks is proved. Harvey's truncated
  integer algorithms have a 25% asymptotic saving under their stated
  real-cyclic-convolution assumption; that result is a comparison, not a
  consequence of this carry state.
- **Online multiplication:** candidate A receives both complete operands
  before recursion and is not an online input/output schedule.

In the source manuscript, the source/target motif has endpoint action
\((X,Y,\mathrm{scratch})\mapsto(-Y,X,\mathrm{same\ scratch})\); the next
section lifts it to a whole-array coordinate interchange. Its recursive
children are full array streams charged by volume and fixed-tape movement.
The integer-product child above has a different type and recurrence, so
that source recurrence and its exponent cannot be reused here.
