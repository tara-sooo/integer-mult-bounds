# Exact zeta operator

At fixed [PR #172](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/172) commit `427b23bc79489e7b2b7548bfd434dd9670fd5c47`, inputs and targets are $U_h=\{1,\ldots,2^h-2\}$. The Yates DAG accumulates each nonempty mask below a target mask. For $t\in U_h$, the root is at $(2^h-1)\mathbin\oplus t$, hence

\[
y_t=\sum_{u\in U_h}[u\mathbin\&t=0]x_u,
\qquad D_h[t,u]=[u\mathbin\&t=0].
\]

`check_small.py` propagates the unit-vector coefficients through that DAG recurrence and asserts equality with the direct matrix. These are exact integer computations, not random evaluations.

## Matrices

Rows and columns use ascending integer mask labels.

For $h=3$, $U_3=(1,2,3,4,5,6)$:

\[
D_3=\begin{pmatrix}
0&1&0&1&0&1\\
1&0&0&1&1&0\\
0&0&0&1&0&0\\
1&1&1&0&0&0\\
0&1&0&0&0&0\\
1&0&0&0&0&0
\end{pmatrix}.
\]

For $h=4$, each row below is its exact 14-entry binary vector, in columns 1 through 14:

```text
1  01010101010101
2  10011001100110
3  00010001000100
4  11100001111000
5  01000001010000
6  10000001100000
7  00000001000000
8  11111110000000
9  01010100000000
10 10011000000000
11 00010000000000
12 11100000000000
13 01000000000000
14 10000000000000
```

Both matrices are symmetric, have zero diagonal, and have full rational rank (6 and 14). Their coefficients are all 0 or +1; neither is an involution. In particular, $(D_h^2)_{1,1}=2^{h-1}-1$, equal to 3 at $h=3$ and 7 at $h=4$, not 1. These are diagnostics of the zeta map, not a failure of some unspecified encoded multiplication map.

For a fixed target $t$, the root's input support is exactly the nonempty subsets of $[h]\setminus t$, of size $2^{h-|t|}-1$. Their binary span is the coordinate subspace supported outside $t$, so $u\cdot t=0$ in the standard $\mathbb F_2^h$ address form. This proves the complex compiler's side-root support condition. It does not establish the signed scalar identity or the bit-side physical frame condition.

[PR #172](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/172) also supplies a reversible dirty-register word: adjoint pre-read on raw dirt, data injection, forward additions, post-read, inverse additions and inverse data injection. Its clean map is $D_h$ and scratch is restored. That proves transparency for this zeta operator only; see the exact source-word control in [BRIDGE_TEST.md](BRIDGE_TEST.md).

The full exact $D_3,D_4$ matrices, ranks, row sums, and squared-matrix diagnostics are in `small_exact_receipt.json`.
