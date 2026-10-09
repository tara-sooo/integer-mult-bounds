# Source contract

This audit pins the [zeta proposal, PR #172](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/172) at `427b23bc79489e7b2b7548bfd434dd9670fd5c47`, the three-stage construction in [PR #130](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/130) at `6a9970a530119174507904e23592fd59ede19a5d`, and the paired-cube construction in [PR #144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144) at `c8b22bc5c10dba497ac25804e27d9647d818e2ff`. The original manuscript is pinned separately at [openai/math commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a), Sections 3 and 4.

## Typed maps in the pinned sources

| Object | Domain and coefficients | Exact source obligation |
|---|---|---|
| [PR #172](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/172) zeta operator | Rows and columns are $U_h=\{1,\ldots,2^h-2\}$, the nonempty, nonfull masks. Integer matrix $D_h[t,u]=[u\mathbin\&t=0]$. | $x\mapsto D_hx$, with each target indexed by the same mask set as its inputs. This says nothing by itself about multiplication ports. |
| Original Section 3 local motif | $\mathcal T_h=\binom{[h]}3$, with local source $x_T$ and target $y_S$. The outer banks $X_a,Y_a$ are indexed by $a\in\mathcal T_h^3$. Scalar domains are $\mathbb F_2$ for the bit word and $\mathbb Z[i,1/2]$ for the complex word. | $JV+RG=I_{\mathcal T_h}$. In the bit word, the $(S,T)$ coefficient is $[|S\cap T|=1]+(|S\cap T|\bmod2)$. In the complex word, the center scatter is $B_{S,T}=(|S\cap T|-1)/2$; the side term is $-B_{S,T}$ for distinct triples of even intersection and zero otherwise. Their sum is the identity. |
| Original Section 3 three-stage word | Same role set including arbitrary scratch; local scalar maps are composed across three stages. | $(X,Y)\mapsto(X,Y+X)\mapsto(-Y,X+Y)\mapsto(-Y,X)$, restoring scratch. Over $\mathbb F_2$, the signs disappear and the banks exchange. |
| [PR #144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144) paired-cube identity | $h=2p$, $p\ge4$. Ports $P_p$ choose one coordinate from each of three distinct coordinate pairs; $v=8\binom p3$. The matrix coefficients are rational, with dyadic halves. | $B_{T,S}=(|T\cap S|-1)/2$, $K=I-B_{\rm block}$, $H=B_{\rm block}-B$, so $K+H+B=I$ and $K^2=I$. Nonzero $H,K$ entries use binary-orthogonal source and target addresses. |
| [PR #130](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/130) address-frame interface | All $W$ roles, including scratch, have rational $m\times m$ endpoint and gate matrices; $\rho$ is the scalar network's route permutation. | For every role $w$, $M_{\rm out(\rho(w))}-M_{\rm in(w)}=I_m$, and the paid edge-rank sum is $s<Wm$. The three-stage field interchange depends on this endpoint identity. |

The zeta operator's row/column labels and coefficient semantics do not identify with any row or column labels above. In particular, there is no source-defined Boolean-mask-to-$\mathcal T_h$ or Boolean-mask-to-$P_p$ encoder, output decoder, sign rule, or rational frame map in these pins. An equality of orthogonality supports is not a linear-map identity.

## Center condition

The complex-side $B$ term in [PR #144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144) is realized by coordinate-star sources $S_i=\sum_{S\ni i}x_S$. For $h=2p\ge8$, its source span has dimension $h-2$ for each of the $h$ coordinates, and the copied-center charge is $\ell=h(h-2)$ (528 at the selected $h=24$). The exact scatter is

\[
(Bx)_T=\frac12\sum_{i\in T}S_i-\frac16\sum_i S_i.
\]

The retained bit ledger from [PR #97](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/97), carried into [PR #144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144), also uses $h$ copied centers, with charge $\ell=h(h-1)$ at its selected $h=23$. [PR #172](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/172) has no center roots, so its compiler sets $\ell=0$ and derives `deficit = 2v`; it does not construct either source-defined scatter or prove a substitute for $B$. A different centerless proof is possible in principle, but the pinned sources do not state one.

The source equations and file hashes are listed in [SOURCES.md](SOURCES.md). Exact small evaluations are in [BRIDGE_TEST.md](BRIDGE_TEST.md) and `small_exact_receipt.json`.
