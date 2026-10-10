# Issue 42, lane C: milestone 3

**Result: `SCOPED_FRAME_NO_GO`.** In the fixed three-role CNOT cycle topology below, exhaustive exact search over the stated translated five-matrix frame alphabet found no `s < Wm`. The minimum is `s=Wm=8`. In the 1,448,520 normalized assignments containing both noncommuting nilpotents `E12` and `E21`, the minimum is `s=10`. This is a finite grammar result, not a general frame obstruction.

The work continues in the existing linked worktree on branch `issue-42-exact-operator-synthesis`, whose milestone-2 parent is [`42c88ee05ae49863fec05af507d484bf7646dde2`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/42c88ee05ae49863fec05af507d484bf7646dde2). The branch descends from the required fork starting commit [`0605a24a28836168ad29d6239b46064b892298fc`](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/0605a24a28836168ad29d6239b46064b892298fc). The first two milestone records, scripts and receipts are retained unchanged. Issue reference: [Issue 42](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/42).

## Section 04 contract and the two proved barriers

The pinned original source is Section 04, `build/sections/04-swap.tex`, at paper commit [`adc7f1241b42e322a6451854ab7e4b4c146bf78a`](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a); its SHA-256 is `412b170ccaab38dba96e95e3cbfae09f4876a9818f8d278776a746b0f8044906`. The finite contract assigns a rational `m×m` matrix to every source, sink and gate, with one shared matrix for every wire incident to a gate. A completed pointwise bit circuit must map each of the `W` independent source values, including scratch, to exactly one output according to a permutation `rho`. For every source role `w`,

```text
M_out(rho(w)) - M_in(w) = I_m,
s = sum_edges rank_Q(M_head - M_tail) < W*m.
```

Section 04 uses an edge of rational rank `a` for `a` smaller digit-chunk interchanges; its power-width recurrence has factor `s/W`. Thus the target is a reduction in actual recursive interchanges, not a reduction in Boolean gates or a rank statement detached from the full network.

At the pinned [PR #203 proof commit](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/d2873e20750d0949d2ad75cbc4cd82b5b1a74e84), the triangular-flag theorem assumes *all* source, gate and sink frames are simultaneously upper triangular over a characteristic-zero splitting field; under that hypothesis it proves `s >= Wm`. The proof groups equal diagonal labels and charges an incoming edge per demanded independent source value. The same result excludes pairwise commuting frame families, but says nothing about every noncommuting family.

The separate Fano exclusion concerns the balanced 10-role, 14-vertex topology and its 87 specified local splice choices. It proves the relevant scalar completions routable for those topologies, which then rules out a deficit there. It is not a theorem for arbitrary reversible networks. This experiment uses neither that topology nor any of its 87 splice variants. The `E12,E21` frame subfamily below is not simultaneously triangularizable even over an algebraic closure: each nilpotent has a unique invariant line, and those lines are distinct.

## Selected finite grammar

I fixed one small mixed-role topology that has genuine intermediate data mixing but ends as a role permutation:

```text
data roles: 0, 1, 2       scratch role: 3
CNOT word (control -> target):
  0->1, 0->2, 2->0, 0->2, 1->2, 2->1
rho (input role -> output role): (1, 2, 0, 3)
```

Each gate is an invertible `F2` CNOT on its two incident roles; role 3 is untouched. The full circuit is a 3-cycle on data roles and identity on the arbitrary scratch bit. The gate word is a small reversible linear circuit, not a new multiplication formula. It was chosen because the frame assignment problem is small enough to exhaust, while its interleaved role incidences are unlike a balanced Fano splice and permit a non-triangular frame family.

For `m=2`, each source and gate frame is selected from the translated alphabet `T+P`, where `T` is any common rational `2×2` matrix and

```text
P = { 0, I, E12, E21, E12+E21 },
E12 = [[0,1],[0,0]], E21 = [[0,0],[1,0]].
```

The common translation cancels on every edge and in every endpoint difference, so the search fixes `T=0`. For output role `k`, set its sink frame to `M_in(rho^-1(k))+I`; this enforces all four endpoint equations, including scratch, by construction. The scratch source frame is also quotiented out: its sole edge always has difference `I_2` and contributes rank 2, independent of that frame. This folds the factor of five from its palette choice; the unquotiented finite palette has `5^10 = 9,765,625` tuples. At each of the six gates there is exactly one frame variable shared by both incident role wires.

This is an explicit alphabet grammar, not a search over all rational matrices. It contains a non-triangular family (`E12` and `E21`) outside the PR #203 triangular theorem. Its `W=4,m=2` scale is far below the aspirational `W=30,m=3` target; it tests whether a minimal mixed-role topology can realize the finite contract before expanding either dimension.

The gate word and role cycle are fixed to one labeled representative. Relabelings of its three data roles give equivalent copies and are not searched again. Different CNOT decompositions of the same cycle, other Boolean gates, other topologies, larger frame alphabets, and larger `m,W` are outside this bounded run.

## Exact verification and coverage

Run the standard-library-only checker with:

```sh
python3 research/parallel-c-exact-synthesis/milestone3_search.py
```

It deterministically enumerates all `5^(3+6) = 1,953,125` normalized data-source/gate-frame assignments. There is no random seed. The receipt is [`milestone3_receipt.json`](milestone3_receipt.json); it records the full rank-sum histograms, exact tested counts, controls and runtime. Sink endpoints are derived rather than searched. Because endpoint identities depend on source frames but not gate frames, the checker checks all four identities for each of the 125 distinct data-source tuples; this covers every gate-frame assignment. Each gate has one shared frame variable used on both incident role edges. For `2×2` integer differences, it computes exact rank over `Q` from zero/nonzero entries and the determinant; rank controls cover zero, nonzero singular and full-rank examples. All frame differences here are integer matrices, so this computes their rational ranks exactly.

The `F2` check separately enumerates all 16 assignments of the four independent source bits. Every row maps by the declared `rho`; the scratch bit can be either value and is preserved. Adverse controls are rejected: reversing the first CNOT causes 12 truth-table row mismatches, restricting role 1 to alias role 0 omits half the independent input domain, and adding `E12` to one required sink frame violates its endpoint equation.

Search result:

| Frame assignments | Count | Minimum `s` | Strict deficit |
| --- | ---: | ---: | ---: |
| All normalized assignments | 1,953,125 | 8 | 0 |
| Assignments containing both `E12` and `E21` | 1,448,520 | 10 | 0 |

Across the full grammar, 18 assignments have `s=8` and 81 have `s=9`; the rest and their counts are in the receipt. The non-triangular subset count is `5^9 - 2*4^9 + 3^9`, checked independently against enumeration. Since any frame family containing both `E12` and `E21` has no common invariant line, this gives a specific exact obstruction outside the triangularizable class: in this topology and alphabet, making those two noncommuting nilpotents available together does not produce a deficit and costs at least two more rank units than `Wm`.

## Cost and scope

For this network `Wm=8`. The best edge-rank total gives `s/W=8/4=2=m`, so Section 04's recurrence has no sublinear exponent from this construction; the certified non-triangular subfamily has `s/W >= 10/4`. No recursive interchange is eliminated. This result therefore supplies neither a cheaper multiplication child nor a plausible integer-multiplication `κ` improvement.

The bit contract includes one arbitrary dirty scratch role and proves it is restored exactly for all bit values. That does not establish a supplier family for a multiplication algorithm. No all-size circuit family, complex supplier, prime/precision compilation, global dirty-row restoration, fixed-tape implementation or integrated recurrence was constructed or tested. Since there is no rank deficit, those later obligations were not pursued.

The bounded no-go is limited to the stated CNOT cycle, one pass-through scratch role, `m=2`, and the translated palette `T+P`. A discriminating next search should change the interaction topology or admit a larger noncommuting frame algebra, retain the all-role/scratch truth-table contract, and still use exact endpoint and rational-rank checks. It must not infer impossibility at `m=3,W=30` from this finite result.

## Reproducibility status

- Exact `F2` truth table and adverse controls: **PASS**.
- Exact rational endpoint and rank search: **PASS**, exhaustive in the declared grammar; runtime in the receipt.
- Full repository `make verify`: **NOT RUN**; this isolated mathematical search does not change runtime code.
- First-wave and milestone-2 records: retained unchanged.
