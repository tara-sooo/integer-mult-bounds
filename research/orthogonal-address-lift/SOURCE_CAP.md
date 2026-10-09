# Frozen source cap and fixed operator

This artifact answers [Issue 29](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/29). The source geometry is frozen at [PR 144 commit c8b22bc5c10dba497ac25804e27d9647d818e2ff](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/c8b22bc5c10dba497ac25804e27d9647d818e2ff), with the three-stage endpoint and bit contracts read at [PR 130 commit 6a9970a530119174507904e23592fd59ede19a5d](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/6a9970a530119174507904e23592fd59ede19a5d). The fixed signed operator and its prior verification are pinned at [Issue 28 commit c4c9c6461d86b84774b9a8cd0b5907549275c740](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/c4c9c6461d86b84774b9a8cd0b5907549275c740).

## Original p=4, h=8 ports

There are four coordinate pairs and eight binary address coordinates. In lexicographic order, choose a three-element set of pair indices $I=(i_0,i_1,i_2)$, then selector bits $e=(e_0,e_1,e_2)$. Its port is

$$
T=(2i_0+e_0,2i_1+e_1,2i_2+e_2),\qquad q_T=\chi_T\in\mathbb F_2^8.
$$

This gives four eight-port cubes and 32 distinct source ports and 32 distinct target ports. Each address has weight three and self-pairing one. The complex-side cap is the ordinary binary dot product

$$
q_T\cdot q_S=|T\cap S|\pmod 2.
$$

The scalar coefficients are exact elements of $\mathbb Z[i,1/2]$. The bit supplier is a separate construction; its coefficients and rational frames are not obtained by reducing these halves modulo two.

## Exact baseline matrices

With $B_{\rm block}$ zero between distinct cubes, the frozen source formulas are

$$
2B[T,S]=|T\cap S|-1,\qquad
K=I-B_{\rm block},\qquad H=B_{\rm block}-B.
$$

Inside each cube, $2K=P-A$, where $P$ is the antipode and $A$ is distance-one adjacency. The exact checker reconstructs all 1,024 coefficients of each full matrix, verifies $K^2=I$ and $K+H+B=I$, checks the direct source $F/A/G$ formula for every $H$ coefficient, and checks the coordinate-star scatter for every $B$ coefficient. Baseline nonzero counts are $B=544$, $H=384$, and $K=128$. Every nonzero $K$ and $H$ edge is orthogonal under the pinned address cap.

The original p=4 profile recorded by the prior verification is 32 source and 32 target data roles, source transitions $[2,4,1]$ per source, target transitions $[4,1,1,1]$ per target, 140 signed $H$ root uses, and eight coordinate-star centers of rank six each ($\ell=48$). These are finite source checks, not a completed p=4 all-size recurrence.

## Fixed Issue 28 shear and witness

The operator is not modified here. Port 0 is $T_0=(0,2,4)$, port 8 is $T_8=(0,2,6)$, and port 10 is $T_{10}=(0,3,6)$. Keep exactly

$$
C=I+E_{0,8},\quad C^{-1}=I-E_{0,8},\quad
K'=CKC^{-1},\quad B'=B,\quad H'=I-K'-B'.
$$

The committed Issue 28 check records the exact matrices and confirms the rational identities. The moved coefficient $K'[0,10]=-1/2$ has $q_0\cdot q_{10}=1$; $H'[0,10]=+1/2$ has the same violation. Each of $K'$ and $H'$ has four such nonzero violations. Their support counts are $136$ and $386$; $B'$ is unchanged at $544$.

The rank 2 address experiment adds coordinates only to test the stated cap. It does not replace the source port theorem. The complete matrices, support domains (including entries moved from zero), coefficient counts, hashes, and per-edge cap checks are in [receipt.json](receipt.json).
