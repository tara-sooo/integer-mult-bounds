# Bridge test

**Result: `REDUCTION_BRIDGE_NOT_SPECIFIED`.** The first honest attempt is the literal mask assignment. The pinned multiplication sources define no map from the zeta basis $U_h$ to their triple ports, and no output decoder from zeta roots to the source targets. The operators therefore cannot be composed into a well-typed equality. No real zeta-versus-multiplication basis-vector mismatch is claimed.

## Exact small source formulas

The original Section 3 formulas can be evaluated on their own true port space $\mathcal T_h=\binom{[h]}3$. This is a source-backed calculation, not a proposed zeta encoding:

| $h$ | zeta dimension $2^h-2$ | original local port dimension $\binom h3$ | exact complex source map |
|---:|---:|---:|---|
| 3 | 6 | 1 | center $[1]$, side $[0]$, sum $[1]$ |
| 4 | 14 | 4 | center $(I+J)/2$, side $-(J-I)/2$, sum $I_4$ |

In these two sizes the original bit map is also exactly $I$ over $\mathbb F_2$: its $(S,T)$ coefficient is $[|S\cap T|=1]+(|S\cap T|\bmod2)$. The complex matrices use $\mathbb Q$ coefficients, as prescribed by the source. These are small evaluations of Section 3's formula; they do not claim the large-size reduction hypotheses at $h=3,4$.

The dimensions differ, and neither the manuscript nor [PR #130](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/130) or [PR #144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144) specifies an embedding, projection, or decoder to bridge them. The separate paired-cube family is defined for $h=2p$, $p\ge4$; it has no $h=3$ instance, and at $h=4$ ($p=2$) its three-distinct-pair port set is empty. Thus those commits do not provide a 6-by-6 or 14-by-14 multiplication operator to compare with $D_h$.

## Source identity and a controlled support-only counterexample

At the smallest valid paired-cube size ($p=4,h=8$), the exact 32-port [PR #144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144) matrices in `check_small.py` satisfy $K+H+B=I$, $K^2=I$, and every nonzero $H,K$ entry is between binary-orthogonal addresses. This reproduces the source identity over $\mathbb Q$.

For an explicitly **synthetic** support-only control on those same source port labels, take target $T=\{1,3,5\}$ and source $S=\{1,3,7\}$. Then $|T\cap S|=2$, so the source coefficient is $B_{T,S}=+1/2$, while the disjointness indicator is 0. Hence a disjointness-only coefficient matrix on $P_4$ would send basis vector $e_S$ to coefficient 0 at $T$, while $B e_S$ has coefficient $1/2$. This is a counterexample to that synthetic substitution only; it is not a map from [PR #172](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/172)'s $U_h$ and is not a real bridge counterexample.

## Dirty restoration control

The source sequence for injection $V$, scalar circuit $M$, decoder $J$, and dirty register $z$ is

\[
y\gets y-JMz,\quad z\gets z+Vx,\quad z\gets Mz,\quad
y\gets y+Jz,\quad z\gets M^{-1}z,\quad z\gets z-Vx.
\]

With exact rational scalars $y=7,z=5,x=3,M=2,J=V=1$, the full word returns $(y,z)=(13,5)$, as required by $y+JMVx$ and restoration of $z$. Omitting the pre-read gives $(23,5)$; omitting the source inverse gives $(13,13)$. Both controls are exact and illustrate why the dirty-source chronology and inverse are part of the interface.

## Missing lemma

To change this result, a source-backed theorem must give a typed map from zeta inputs and outputs to actual multiplication ports, over the actual scalar ring, plus the signed port identity it realizes. For the paired-cube route this means a lawful $(B_z,H_z,K_z)$ (or a proved alternative), the exact data action and stage signs, a full inverse/cleanup for arbitrary dirty roles, and source/target frame maps satisfying [PR #130](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/130)'s endpoint condition. A trial $K_z$, coordinate identification, or support comparison alone is insufficient.

The exact matrices and controls are recorded in `small_exact_receipt.json`. The synthetic counterexample is deliberately kept separate from the primary result.
