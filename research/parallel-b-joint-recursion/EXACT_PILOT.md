# Exact pilot: shared-left pair of full products

## Small instance

For `n=2`, write `A=a_0+a_1x`, `B=b_0+b_1x`, and `C=c_0+c_1x`. Let

```text
sA = a0+a1, sB=b0+b1, sC=c0+c1.
P0 = a0*b0, P2 = a1*b1, P1 = sA*sB-P0-P2.
Q0 = a0*c0, Q2 = a1*c1, Q1 = sA*sC-Q0-Q2.
```

Then `(P0,P1,P2)=(AB)` and `(Q0,Q1,Q2)=(AC)` coefficientwise over any commutative ring. The shared `sA` is computed once. This is two ordinary Karatsuba/Toom-2 products with one repeated linear evaluation removed; all six recursive scalar products remain.

## Exact rank certificate

Flatten the bilinear tensor of `J_n` along its output. Its rows are the `4n-2` coefficient forms

```text
sum_(i+j=k) a_i b_j,   sum_(i+j=k) a_i c_j,     0 <= k < 2n-1.
```

The coefficient supports for distinct `k` are disjoint. The `B` and `C` supports are disjoint from each other. Hence these `4n-2` rows are linearly independent over `F`, so the output flattening has rank `4n-2`. A bilinear algorithm using `q` scalar multiplication terms is a sum of `q` rank-one tensors and has output-flattening rank at most `q`; therefore `q >= 4n-2`. Two independent Toom products use exactly `2(2n-1)=4n-2` scalar products over a field with enough interpolation points. Thus the bilinear rank of this typed joint child is exactly `4n-2`: no scalar multiplication leaf is saved.

At `n=2`, the exact certificate is rank `6`. The deterministic checker builds the rational flattening matrix, verifies rank `6` (also checks `n=3`, rank `10`), expands the Karatsuba forms exactly, and rejects a deliberately wrong `Q1` reconstruction that subtracts `P2` instead of `Q2`.

## Cost observed at `n=2`

The joint schedule uses six field multiplications, three input additions (`sA,sB,sC`), and four output subtractions: seven linear arithmetic gates. Two unshared Karatsuba calls use six field multiplications and eight additions/subtractions because they each recompute `sA`. A fair baseline can compute/cache `sA` once too; it then has the same six multiplications and seven linear gates. The one-gate difference is ordinary shared evaluation, not a deleted recursive multiplication child.

The exact experiment does not assign fictitious zero cost to output storage, copies, tapes, or integer carry. Their recurrence charges are stated in `RECURRENCE.md`; a finite-tape compiler for `J_n` into the original Section 4 interface is not claimed.
