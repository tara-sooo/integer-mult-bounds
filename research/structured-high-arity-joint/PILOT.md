# Exact pilot: `r=3`, `m=2`

## Typed operation

The parent inputs are `a,b ∈ Q^6`; each child encoder produces two
coefficients and each child returns three:
\[
 U_t,V_t:\mathbb Q^6\to\mathbb Q^2,\qquad
 z_t=\operatorname{Conv}_2(U_ta,V_tb)\in\mathbb Q^3,\qquad
 W_t:\mathbb Q^3\to\mathbb Q^{11}.
\]
An exact `q`-child candidate must satisfy
\[
 \sum_{t=1}^qW_tz_t=\operatorname{Conv}_6(a,b)
 \quad\text{for all }a,b\in\mathbb Q^6.
\]
This has direct integer semantics: for binary coefficient inputs it returns
the exact integer convolution, which becomes the ordinary integer product
after base-two carries.

## Scoped impossibility proof

The length-six convolution tensor has bilinear rank `2·6−1=11` over
`Q`. One length-two child has rank `2·2−1=3`; linear maps before or after
that child cannot raise its rank. A sum of three child tensors has rank at
most `3·3=9`. Therefore no choices of the matrices `U_t,V_t,W_t` can make
`q=3` satisfy the identity. More generally, the same argument gives
\[
q\ge\left\lceil\frac{11}{3}\right\rceil=4.
\]
Four children have rank capacity `12`, so this argument does **not** decide
whether `q=4` is possible. The general bound and its limits are proved in
MODEL.md; the rank theorem itself is prior work, not a new lower-bound
claim.

## Exact coefficient check and adverse control

`check_obstruction.py` checks all `6×6=36` basis pairs of the actual target
tensor: `(e_i,e_j)` must return the eleven-vector `e_(i+j)`. It then checks
the exact rank arithmetic: three children provide capacity `9<11`, while
four provide `12≥11`. This is a complete basis check of the declared
convolution semantics plus an exact check of the scoped rank gate; it is
not a search for or verification of a four-child decoder.

For the integer transfer, it also exhausts all `64×64` pairs of six-bit
inputs, computes the exact coefficient vector, performs binary carries,
and compares the recovered value with ordinary integer multiplication.

The adverse control is the tempting `q=r=3` proposal. It fails the rank
gate and is rejected. The checker deliberately leaves `q=4` as
`NOT_DECIDED`; treating a sufficient rank capacity as a construction would
be an invalid positive control.

## Integer transfer

For `N` binary digits, set
\[
A=\sum_{i=0}^{N-1}a_i2^i,\quad
B=\sum_{j=0}^{N-1}b_j2^j,\quad
c_k=\sum_{i+j=k}a_ib_j.
\]
Then `AB=Σ c_k2^k` exactly and `c_k≤N`. Starting from carry `q_0=0`,
emit `d_k=(c_k+q_k) mod 2` and set
`q_(k+1)=floor((c_k+q_k)/2)`, then append the final carry. This is the
standard exact binary recovery. It connects the typed convolution target
to integer multiplication; it does not make the hypothetical rational
encoders integral or free.
