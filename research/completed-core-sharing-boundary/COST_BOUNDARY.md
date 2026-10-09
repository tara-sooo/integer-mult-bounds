# Paid-cost boundary

The three pinned constructions change different objects. Their `m`, role counts and child histograms describe different geometries, so the rows below are source-separated and are not a cross-version efficiency ranking. The audit does not compare their conditional exponent values. Here `s_profile=Σ_r r n_r` denotes weighted rational child-rank mass; it is separate from a finite XOR count, role count and the exponential recurrence moment. This symbol is distinct from `s_swap=Σ_e rank_Q(A_e)` in the Section 4 bit-array recurrence.

## PR #128: old independent roles versus the grouped profile

For the pinned `h=24` producer, `v=2024`, `R=28,705`, `N=v^2=4,096,576`, and `m=576`.

| Quantity | Separate per-core allocation | Pinned grouped allocation |
|---|---:|---:|
| Auxiliary roles | `2vR = 116,197,840` | `2*87*R = 4,994,670` |
| Data roles | `2N = 8,193,152` | `2N = 8,193,152` |
| Total roles | `124,390,992` | `W = 13,187,822` |
| Outer auxiliary correction | Derived independent schedule: `2vR` children of width `m-h=552` | `2*4*R = 229,640` children of width 384; full 24-groups need none |
| Correction rank mass | Derived: `64,141,207,680` | `88,181,760` |

The separate-allocation column is the counterfactual obtained by retaining the source's old role key `(stage,b,u)` and closing every core separately. It is not a separately certified prior profile. The grouped column is the actual pinned profile. Grouping saves role streams and replaces one 552-dimensional exterior per old role with one 384-dimensional complement for each of four partial groups per stage and role. The width-384 complement remains a recursive child, and its signs/adapters remain scalar/router work.

The full pinned profile is `m=576`, `W=13,187,822`, weighted child-rank mass `s=7,594,323,392`, deficit `mW-s=1,862,080`, and largest child 529. Its certificate includes the complete child histogram, exact rational moment bounds and semantic/row reserves; this note does not compare those moments with a different PR profile. Its children include 229,640 shared-role complements of width 384, `2N` data macros of width 529, `4N` data fronts of width 23, `N` endpoint copies of width 1, and all positive-width internal copied-center children `2v H'_r`. The copied-center histogram replaces 24 rank-24 transitions with rank-one transitions but retains every rank-23 copy transform. The 4,765,030 zero-rank bridges are omitted from the recursive child count; that does not make fixed routing, sign or frame adapters free.

The proof explicitly keeps all `2v` local cores and their scalar gates. It retains `g_h=592,224` and charges the semantic scalar bound `G_0=N+2v(g_h+2h)=2,401,613,632`. The exact recurrence, common odd grid `2^-P 21^-K`, all child widths and the completed-child semantic guard are separately retained. This boundary matters: PR #128 reduces workspace and whole-core exterior duplication, but it does not reduce the number of computed local cores or pass one core's logical result into another.

## PR #130: global three-stage cover

This is a distinct data-incidence construction. For its complex branch at `h=24`, `v=2024`, `R=28,705`, `ell=552`, and `m=70`:

| Profile | Per-vertex roles | Child rank mass | Deficit | Largest child |
|---|---:|---:|---:|---:|
| Complex three-stage cover | `W_0=2v+3R=90,163` | `s_0=6,309,018` | 2,392 | 68 |
| Bit three-stage cover | `W_0=90,140` | `s_0=6,037,356` | 2,024 | 66 |

The complex ledger has three independent auxiliary banks. It keeps three copies of the local auxiliary, data and copied-center histograms. Each of the two data banks pays a rank-two complement per port, and the source Pauli, output signs, bank exchange, rank-zero data adapters and finite routers are charged. The bit branch has its own `m=67` and profile. These two supplier rows do not share a common normalization with either PR #128's `m=576` profile or PR #144's `m=72` profile.

The source reports zero **positive-rank** interstage data connectors because exact frames line up; rank-zero representative adapters are still implemented and charged. This outside-cover saving is independent of any reused auxiliary slot.

## PR #144: three-stage auxiliary-bank reuse

Here `h=24`, `m=72`, `v=1,760`, `R=26,417`, and `ell=528`. The old three-bank per-vertex allocation would be `2v+3R=82,771`; the pinned one-bank allocation is `W_0=2v+R=29,937`, a reduction of `2R=52,834` auxiliary role slots per group vertex. This is a workspace count, not a count of recursive computations removed.

The exact per-vertex child multiset is

    n_r = 3(H_r + D_r + T_r) + 2v * 1[r=2] + sum_(a>0) s_a * 1[r=3a].

The factor 3 on `H+D+T` keeps all three local words and their data/copy children. The `2v` width-two children pay the two data-bank complements. Each selected auxiliary gauge contributes one **grouped** child of width `3a`; the chosen profile has 4,840 gauges of dimension 20, hence 4,840 width-60 children. The weighted child-rank mass is 2,153,528, the deficit is 1,936, and the largest child is 60. The pinned assembly checks its complete rational moment and the semantic/row reserves. The full stock is `W=|O(72,2)| W_0`; only the normalized moment cancels the group factor.

The route and scalar work also remain paid. The source defines `K=3VL+8W+4N+8m_cRV` and `G=64(m_c+1)^3(K+1)(W+1)^2` to cover local operations, completed-core sharing permutations, fixed role permutations and binary/phase adapters. The exact common grid retains the odd divisor 3 without rounding child returns; the completed outer tensor alone allows unscaling. Its external row reserve, internal row borrowing, semantic guard, endpoint correction and inherited fixed-tape interfaces are not removed by bank reuse.

PR #144 also changes the local paired-cube producer and its gauge selection. Its profile cannot be treated as PR #128 with only one term changed; no exponent difference is attributed to one technique here.

## Where a new cross-child payload would have to save work

In the original Section 4 recurrence, the only direct recursive term is `s_swap` calls, one for each pivot of the fixed edge matrices, each on a child stream of volume `V/W`: `F_k <= (s_swap/W)F_(k-1)+O(1)`. A genuine result handoff would have to identify at least two distinct occurrences with the same complete child input payload, shape, row class and entrance frame, and show that both consumers can use the same output without reapplying the permutation. A copy or conversion must be paid, as must restoration of any dirty spectator and the parent's fixed-tape state.

No such duplicate occurrence or payload is recorded in the PR #128/#130/#144 source. Therefore this audit identifies no specific child charge that can be removed. A possible future reduction in `s` or in a particular weighted child term is only a target for investigation, not a proposed recurrence or saving.
