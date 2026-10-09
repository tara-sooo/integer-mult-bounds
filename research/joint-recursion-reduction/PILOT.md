# Exact pilot: length-four integer convolution

## Construction

For n=4, split at m=2. The top call computes three length-two
convolutions:
\[
p_0=\operatorname{Conv}_2(a_0,b_0),\quad
p_2=\operatorname{Conv}_2(a_1,b_1),\quad
p_1=\operatorname{Conv}_2(a_0+a_1,b_0+b_1).
\]
Each length-two call splits once more and uses three length-one integer
products. Thus the root has three actual width-two child tasks and the full
tree has nine scalar multiplication leaves. The output has seven integer
coefficients:
\[
c=p_0+x^2(p_1-p_0-p_2)+x^4p_2.
\]

For every m, expansion in the commutative ring Z[x] gives
\[
(a_0+x^ma_1)(b_0+x^mb_1)
=a_0b_0+x^m(a_0b_1+a_1b_0)+x^{2m}a_1b_1.
\]
Since p_1-p_0-p_2=a_0b_1+a_1b_0, the decoded polynomial is exactly
a(x)b(x). Induction from n=1 proves the typed identity for every
power-of-two n, not only n=4.

## Full bilinear tensor check

The recursive map is bilinear: each encoder is linear in one input, every
leaf multiplies one A-linear form by one B-linear form, and the decoder is
linear. Therefore checking all basis pairs checks every coefficient of its
bilinear tensor. For n=4, the checker visits all 16 pairs (e_i,e_j) and
requires the exact seven-vector e_(i+j):

| i\j | 0 | 1 | 2 | 3 |
|---:|---:|---:|---:|---:|
| 0 | e0 | e1 | e2 | e3 |
| 1 | e1 | e2 | e3 | e4 |
| 2 | e2 | e3 | e4 | e5 |
| 3 | e3 | e4 | e5 | e6 |

The exact deterministic checker is check_pilot.py; it uses Python integers
and checks the entire table.

## Child ownership and workspace

| Child | A input | B input | Output | Dependencies |
|---|---|---|---|---|
| p0 | a0 in Z^2 | b0 in Z^2 | Z^3 | used directly and in the middle difference |
| p2 | a1 in Z^2 | b1 in Z^2 | Z^3 | used directly and in the middle difference |
| p1 | a0+a1 in Z^2 | b0+b1 in Z^2 | Z^3 | supplies both cross terms |

The parent reads its input arrays without mutation. It owns fresh sum arrays,
three returned child arrays, and a fresh seven-coefficient output. The
p0,p2 outputs must be retained until the decoder uses them a second
time; their storage and reads are paid. Calls run sequentially. After
decoding, the parent clears and releases all sum and child buffers.

This is an ordinary deterministic computation, not a reversible or
dirty-transparent circuit. It makes no claim for arbitrary initial scratch.
Every work buffer is newly initialized, and clearing/releasing it costs a
linear scan of its stored bits; that scan is included in COST.md. Inputs
and final output are not cleared.

## Adverse control

A plausible decoder error is to omit -p2 from the middle term. On
a=b=x^2, that incorrect formula returns x^2+x^4, while the correct
product is x^4. check_pilot.py asserts that this negative control is
rejected. The recorded witness is in receipt.json.

## Integer-product transfer

Write nonnegative N-bit integers as
A=sum_(i=0)^(N-1) a_i 2^i and
B=sum_(j=0)^(N-1) b_j 2^j, with a_i,b_j in {0,1}.
The exact convolution gives
\[
AB=\sum_{k=0}^{2N-2}c_k2^k,\qquad 0\le c_k\le N.
\]
Set q_0=0, d_k=(c_k+q_k) mod 2, and
q_(k+1)=floor((c_k+q_k)/2). Emit d_k for k=0,...,2N-2
and append the final carry q_(2N-1). This is ordinary exact binary carry
propagation and returns AB. The convolution proof is over Z;
no modular, complex, or dyadic construction is identified with it.
