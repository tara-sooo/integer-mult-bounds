# First-pass map of barriers to κ = 1

**Snapshot:** 2026-10-08. Fork base: `tara-sooo/integer-mult-bounds` commit
`0605a24a28836168ad29d6239b46064b892298fc`. The PR witnesses below are pinned
to the immutable construction commits named in Issue #10. This report does
not follow later upstream changes. Source IDs resolve in [`sources.json`](sources.json).

## Finding

The pinned material gives no theorem that rules out κ = 1 for integer
multiplication. The model's output length proves only `T(n) = Ω(n)`, which
permits `O(n)`. It does not prove an `Ω(n log n)` lower bound. The original
OpenAI manuscript states a fixed-alphabet, fixed-finite-tape theorem at
κ = 2⁻¹⁸²; the fork's audited release improves its conditional exponent, but
both are fixed-point proofs with strict margins. Neither may be continued to
κ = 1 by taking a limit. [S1, S4]

The strongest usable obstruction in this bounded pass is local to the exact
PR #63 finite profile and its inherited balanced-assembly parameterization.
For that profile, the exact bit moment rejects the next saving grid point, and
the assembly's `g3` margin is the tightest final inequality. These are useful
restricted-family ceilings, not lower bounds for other networks or for
integer multiplication in general. [S8]

## Dependency chain

1. **Multiplication reduction.** The pinned manuscript reduces exact integer
   multiplication to Gaussian-resampled transforms, synthetic polynomial
   transforms, and exact coefficient recovery. The theorem is for one
   deterministic machine with a fixed finite alphabet and a fixed finite
   number of one-dimensional tapes. [S1]
2. **Recursive network.** A finite network has parameter `m`, `W` role streams,
   and a complete multiset of child widths `t` with multiplicities `n_t`.
   The base paper's equal-width recurrence is
   `F(e) ≤ (s/W) F(e/m) + O((eK)^τ + 1)`, where `F` is time divided by logical
   volume and `s` is the total child rank. For a recorded mixed-width profile,
   the exact sufficient bit-recurrence test used by the pinned witnesses is

   ```text
   M_b(a) = (1/(m W)) Σ_t n_t t (m/t)^a < 1.
   ```

   This permits a recursive cost with exponent saving `a` only for that full
   child profile and the inherited transfer argument. At `a = 0`,
   `M_b(0) = (Σ n_t t)/(mW) = s/(mW)`; at positive `a`, the complete width
   histogram matters. The rank sum or role count alone does not determine the
   exponent. [S2, S6, S7, S8]
3. **Assembly.** The bit saving `a_b` is not the final `κ`. The candidate
   witnesses combine `a_b` with a fixed complex saving `a_c`, a semantic and
   row-stock bridge, and strict exponent/cost inequalities. Their final κ is
   the accepted value under 47 assembly constraints and seven positive cost
   margins. In the pinned balanced assembly, `q = a_b(1−2η)`,
   `ε = (1−η)/(1+q)`, and the controlling margin is `g3 = εq`; hence
   `κ < g3 < a_b/(1+a_b)`. This is the source's rank/bit-saving-to-κ
   conversion for that parameterization, not a universal formula for every
   multiplication architecture. [S7, S8, S8-script]
4. **All-size transfer.** The finite profiles feed claims about residual
   compilation, arbitrary dirty scratch, framed-word transfer, sequential
   fixed-tape storage, arithmetic precision, routing, prime selection,
   exact recovery, setup, and eventual thresholds. The finite certificates
   check candidate instances; they do not by themselves discharge the
   all-size arguments. [S4, S6, S7, S8]

The original paper fixes strict rational parameter inequalities and a single
positive κ. Its cost table has terms with exponents such as
`1 − εc(1−τ)`, `1 − ε(1−λ′)`, and `τ + ε(2−τ)`. The selected values leave
strict slack; they do not establish a uniform estimate as κ tends to one.
At κ = 1 the target simplifies to `O(n)`, but the existing positive-slack
arguments cannot be evaluated at that endpoint without a new parameter and
proof analysis. [S3]

## Pinned finite witnesses

All values in this table are claims recorded in the cited exact proof notes
and certificates. This pass read the pinned files but did not regenerate their
physical profiles or rerun their arithmetic checkers.

| Pinned construction | `m` | `W` | Total child rank `s` | Deficit `mW−s` | Largest child | Bit saving `a_b` | Reported `κ` |
|---|---:|---:|---:|---:|---:|---:|---:|
| PR #58, dual-suffix + joint frames | 575 | 150,593,466 | 86,589,396,050 | 1,846,900 | 529 | 1187740349/25000000000000 | 475073569/10000000000000 |
| PR #62, interval strips (standalone) | 575 | 140,924,496 | 81,029,738,300 | 1,846,900 | 529 | 4986382/100000000000 | 4986133/100000000000 |
| PR #62 graph + PR #57 frame compiler | 575 | 137,151,806 | 78,860,441,550 | 1,846,900 | 529 | 5101952/100000000000 | 5101691/100000000000 |
| PR #63 rank-first compiler on PR #62 graph | 575 | 137,151,806 | 78,860,441,550 | 1,846,900 | 529 | 5103018/100000000000 | 5102757/100000000000 |

For all four, the notes define the full recurrence profile, not just the
aggregate rank. PR #63 changes the actual transition paths and child profile;
its proof reports 27,918 / 36,586 auxiliary roles at dimensions 23 / 25,
with all 1,612 / 2,092 signal-clearing XORs paid. It reports 36,378 / 50,419
distinct profile matrices and 6,049 / 8,127 CRT-checked matrices, with no CRT
disagreements. The compiler changes neither `m`, `N`, `L`, `W`, the total rank,
nor the deficit; its claim rests on the recomputed child moment, not role count
alone. [S8]

The fork's current audited release at the snapshot is κ =
`971668963/25000000000000`. Issue #5's requested PR #54 reproduction baseline
is separately pinned at commit `7210de7d0f9ccaeb64c3f60f188419e02be08d95`,
with κ = `141532521/3125000000000`. These are context points, not evidence of
a ceiling for later or different constructions. [S0, S4]

## Restricted obstruction: fixed PR #63 profile and assembly

Fix the complete child multiset recorded by PR #63's
`screen-certificate.json`, with `m = 575`, `W = 137151806`, all child widths
`1 ≤ t ≤ 529`, and the same rank-first physical profile. Its exact interval
certificate accepts `a_b = 5103018/10^11` and proves the lower moment exceeds
one at `5103019/10^11`. For every child, `log(m/t) > 0`, so

```text
M_b(a) = Σ_t [n_t t/(mW)] exp(a log(m/t))
```

is strictly increasing in `a`. Therefore the same profile cannot satisfy this
moment test at any `a_b ≥ 5103019/10^11`. This is a rigorous obstruction for
the fixed child list and this sufficient recurrence test. It says nothing
about changing `m`, the graph, the frame compiler, or the child profile. Under
the same assembly conversion `κ < a_b/(1+a_b)`, this gives the scoped ceiling
`κ < 5103019/100005103019` (approximately `5.10275860525885×10^-5`). The
selected fixed assembly point is tighter still because `g3` is its controlling
margin. [S8, S8-script]

With the exact PR #63 assembly parameterization held fixed (`β = 1/20`,
backoff `η = 10^-12`, `a_c = 717/10^7`, `C1 = 1`, and row stock `p^2000`), the
certificate records 47 positive strict constraints and these seven κ-slacks:

| Margin | Exact slack above κ | Approximate slack |
|---|---:|---:|
| `g1` | 17634539705619730410313/2500127575449999744849100000000000 | 7.05346×10⁻¹² |
| `g2` | 261/100000000000 | 2.61×10⁻⁹ |
| `g3` | 151344121301697306654639/25001275754499997448491000000000000 | 6.05346×10⁻¹² |
| `g4` | 261/100000000000 | 2.61×10⁻⁹ |
| `g5` | 257151359535415689116517/40002041207199995917585600000000000 | 6.42846×10⁻¹² |
| `g6` | 1385761900695078435376549/200010206035999979587928000000000000 | 6.92846×10⁻¹² |
| `g7` | 2499872424562634794856519730410313/2500127575449999744849100000000000 | 0.999898 |

`g3` is the smallest κ-slack and equals the controlling margin `G = εq`.
The certificate's coarse scoped limit `a_b/(1+a_b)` is exactly
`2551509/50002551509` (approximately `5.102757605360902×10^-5`); the actual
strict assembly bound is `κ < G`, with `G` equal to the exact `g3` margin in
the certificate. The selected κ is `5102757/10^11`, while the next `10^-11`
grid point fails. The 47 named
checks are: `K_dominates_log`, `K_geometry`, `a_below_b`, `a_positive`,
`alpha_below_one`, `alpha_below_one_fourth`, `alpha_positive`,
`artificial_boundary`, `b_below_one_over32`, `beta_below_one`,
`beta_positive`, `c_below_one`, `c_positive`, `cell_above_band`,
`compact_leaf`, `compact_reservations`, `delta_below_one_eighth`,
`delta_positive`, `epsilon_below_one`, `epsilon_positive`,
`g1_above_kappa` through `g7_above_kappa`, `gamma_sublinear`, `guard_width`,
`lambda_above_internal`, `lambda_above_sigma`, `lambda_above_tau`,
`lambda_prime_above_lambda`, `lambda_prime_below_one`,
`literal_scalar_guard`, `phase_boundary`, `phase_leaf_above_bit`,
`phase_local`, `prime_interval_packing`, `q_below_internal`, `q_below_leaf`,
`q_below_reservations`, `q_positive`, `record_suffix`, `row_product_gap`,
`short_record_fallback`, and `small_field_exposure`. Their exact rational
values are in the pinned certificate. This is a one-point finite check under
the fixed parameterization, not a proof against retuning those parameters or
changing the outer reduction. [S8]

## Barrier map and status

| Obstacle or claim | Status | Domain and what must change |
|---|---|---|
| Output requires Ω(n) steps | **PROVED** | Exact output has `2n` bits and a fixed finite alphabet emits only a bounded number of bits per step. This permits κ=1 and only rules out κ>1. |
| PR #58/#62/#63 moment crossings | **FINITE-CHECKED** | Exact rational bounds apply to each pinned finite child multiset. To improve them, change the child profile or recurrence; do not extrapolate across networks. |
| PR #63's 47 constraints and seven margins | **FINITE-CHECKED** | Checked at one rational parameter point. `g3` is tightest there; a new parameterization or cost bound is needed to move the assembly ceiling. |
| Role compilation, carrier/frame legality, dirty-state restoration | **CONDITIONAL** | Finite words/profile transitions are replayed; the all-size residual compiler and framed-word transfer remain inherited proof obligations for the newer candidate. |
| Fixed-tape storage, finite-alphabet accounting, routing and geometry | **CONDITIONAL** | The arguments rely on the cited transfer/layout hypotheses and fixed rational parameter family; the certificates do not re-prove them for all sizes. |
| Gaussian resampling, analytic estimates, prime selection, setup, exact recovery, eventual cutoff | **CONDITIONAL** | These are inherited from the pinned framework and fork audit. A κ→1 claim needs strict end-to-end bounds, not only a larger finite-network saving. |
| κ=1 impossible for integer multiplication | **OPEN** | No such theorem appears in the inspected pinned sources. The Ω(n) output bound is consistent with linear time. |
| κ=1 achievable in this framework | **OPEN** | No pinned argument reaches the endpoint. A proof needs a different or substantially stronger recursive family plus new outer-cost and all-size proofs. |

## Bounded reproduction record

Input: the immutable PR #63 certificate at `aa7701b68540b7863d3b66a414e4319915d6282d`.
The extraction command is:

```sh
git show aa7701b68540b7863d3b66a414e4319915d6282d:research/rank-pair/screen-certificate.json \
  | python3 -c 'import json,sys; d=json.load(sys.stdin); a=d["assembly"]; print("a_b", d["bit_saving"]); print("next a_b", d["next_bit_saving"]); print("kappa", d["kappa"]); print("scoped limit", a["scoped_limit"]); print("constraints", len(a["constraints"]), "margins", len(a["margins"])); print("g3 slack", a["constraints"]["g3_above_kappa"])'
```

Recorded output:

```text
a_b 5103018/100000000000
next a_b 5103019/100000000000
kappa 5102757/100000000000
scoped limit 2551509/50002551509
constraints 47 margins 7
g3 slack 151344121301697306654639/25001275754499997448491000000000000
```

This extraction reproduces the values stored in the pinned certificate; it
does not regenerate the XOR words, CRT profiles, or rational moment enclosure.
The PR #63 source's full focused reproduction is `python3
research/rank-pair/frame_compile.py` followed by `python3
research/rank-pair/screen.py`; neither was run in this first pass. The
repository-wide `make verify` was not run.

## Next concrete step

Prove or falsify a lower bound on `M_b(a)` over a clearly delimited class of
legal producer/carrier/frame constructions, starting with the exact core/cover
and source/output constraints of PR #62/#63. This targets a family-wide
obstruction while leaving open different recursive or outer multiplication
architectures.

## Attribution and license

This first-pass synthesis was prepared with OpenAI Codex assistance. Candidate
results remain attributed to the contributors and AI assistance recorded in
[`sources.json`](sources.json); no inherited construction is claimed as new.
The repository's Apache-2.0 license applies to these notes, while
source-specific notices remain in force.
