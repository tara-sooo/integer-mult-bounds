# Known and unknown cost delta

This ledger uses the fixed operator and source pins in [Issue 29](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/29), [PR 144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144), [PR 130](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/130), and [Issue 28 commit c4c9c6461d86b84774b9a8cd0b5907549275c740](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/c4c9c6461d86b84774b9a8cd0b5907549275c740).

| Cost item | Pinned p=4 baseline | Fixed shear and rank 2 Gram experiment |
|---|---|---|
| Address dimensions | Complex address cap is $\mathbb F_2^8$; 32 typed ports | The Gram labels append two coordinates, so their ambient cap is $\mathbb F_2^{10}$. No source theorem realizes it. |
| Port and role counts | 32 source roles and 32 target roles | Still 32 labels on each side; physical storage, adapters, or copied roles required by an encoder are UNKNOWN. |
| Paired geometry | $p=4$, $h=8$, four eight-port cubes; each port has weight three | Six labels have weight four and norm zero. Treating $h=10$ as $p=5$ gives 80 source-family ports, not this 32-port operator. No legal child profile follows. |
| Scalar matrices | $B=544$, $H=384$, $K=128$ nonzeros; all K/H edges pass the original cap | $B'=544$, $H'=386$, $K'=136$; four K' and four H' edges fail the old cap. The rank 2 labels repair only those support equations. |
| Original support preservation | Original K and H domains have 128 and 384 edges | The rank 2 labels pass all 128 original K and 384 original H edges with zero violations. B remains a separate center channel. |
| Center work | Eight coordinate-star roots of rank six, $\ell=48$ | The scalar matrix B is unchanged. Its star-root spans, incidences, physical readouts, and rank charge for lifted labels are UNKNOWN; the old weight-three proof does not apply. |
| Signed H roots | 140 root uses in the p=4 source schedule | No source-typed H' root schedule. New support coefficients and frames have no charged implementation. |
| K action | The original local K is implemented on original source values; source/target transition histograms are recorded in SOURCE_CAP.md | $C$ and $C^{-1}$ are formal additions on roles 0 and 8. Their frame changes, movement, signed phase, routing, and dirty restoration charges are UNKNOWN. |
| Operations and copies | Existing construction includes its source injections, readouts, inverse cleanup, and role endpoints | No extra semantic port is introduced by the labels. Number of physical bit wires, copies, adapters, or invocations is UNKNOWN. |
| Child problem | The p=4 check fixes exact matrices and source transition samples; it is not a complete p=4 all-size child multiset | No valid frame edge graph, rank sum, parent width, child count, child widths, or recurrence exists. These are NOT RUN, not zero. |
| Routing and endpoints | PR 130 provides an explicit three-stage endpoint and routing theorem for its pinned source geometry | The two appended directions and changed source lines require new routing and endpoint adapters. Their charges are UNKNOWN. |
| Complex branch | Scalar coefficients use $\mathbb Z[i,1/2]$ and the original $\mathbb F_2^8$ cap | The Gram check is exact; no complex physical word or paid realization of the changed address frame is supplied. |
| Bit branch | Separate bit supplier with rational $H_0=(I-J/9)/2$ frames | No mapping or bit-side supplier for the lifted labels. H0 pairing, bit roles, and costs are NOT RUN. |
| Recurrence and $\kappa$ | No p=4 recurrence is established by this finite source check | No paid recurrence exists for the candidate, so no $\kappa$ claim is made. |

At the matrix level, $C$ and $C^{-1}$ are one addition and one subtraction of role 8 into role 0. This is a formal operation count only. Their source-defined physical schedule is absent. For comparison, a hypothetical source construction at $h=10$ would use $m=3h=30$ under the pinned three-block formula; that does not define a valid 32-port child profile or authorize reuse of p=4 ranks.

No old p=12 histogram, finite group multiplicity, row reserve, fixed-tape router, or bit moment was transplanted into this candidate.
