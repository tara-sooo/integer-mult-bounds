# Matched data and Section 4 cost ledger

## h=10 source network: full type and local 80-port restriction

Section 3 has `m=h^3=1000`. For a port set of size `v`, array volume
`N=v^3`, and `I=3v^2` completed invocations, the source's scalar wire stock
is `W=2N+I(vz+c)`, where `z` is the directed side-neighbor count per target
and `c` is the center-wire count. The local p=5 block and the original full
three-element type have distinct stocks:

| Scope | `v` | omitted triples | `z_bit / z_complex` | `c_bit / c_complex` | `N` | `I` | `W_bit` | `W_complex` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| p=5 local selector block | 80 | 40 | 39 / 40 | 10 / 11 | 512,000 | 19,200 | 61,120,000 | 62,675,200 |
| full `T=binom([10],3)` | 120 | 0 | 63 / 56 | 10 / 11 | 1,728,000 | 43,200 | 330,480,000 | 294,235,200 |

The 80-port row is a local truncated invocation family. It is not an additive
part of the 120-port full network, because full invocations also use the 40
repeated-pair triples and their side incidences.

The existing source/copy/read chronology is also unchanged. Each ordered side
neighbor gets its own dirty carrier: stage copy reads the source into it,
side injection reads it at the target, and the old-value correction and
inverse-copy rows restore it. Each source contributes to three coordinate
centers in the bit network and to those three plus `C_*` in the complex
network. The center source-read column counts those `G` incidences. Each
target reads its old and gathered side vector once in the two injection rows,
and its old and gathered center vector once in the two scatter rows.

| Scope | ring | side carriers over all stages | center source reads over all stages | center roles over all stages | new handoff births |
|---|---|---:|---:|---:|---:|
| local 80-port | bit | 59,904,000 | 4,608,000 | 192,000 | 0 |
| local 80-port | complex | 61,440,000 | 6,144,000 | 211,200 | 0 |
| full 120-port | bit | 326,592,000 | 15,552,000 | 432,000 | 0 |
| full 120-port | complex | 290,304,000 | 20,736,000 | 475,200 | 0 |

Thus the two target-side read counts are twice the corresponding carrier or
center source-incidence count. The handoff adds no register or
consumer-specific copy.

## Exact bit rank transitions

For the original Section 3 labels at `h=10`, put `a=h^(j-1)`. The data edges
in one stage have ranks `(a-1)(h-1)` and `h-1` on each of `X,Y`; the X-source
sign contributes one additional rank-one edge per full data role. This gives
the complete data submultiset below. The final data edges have rank zero.

| Scope | rank-one X-source edges | rank 9 | rank 81 | rank 891 | data rank mass |
|---|---:|---:|---:|---:|---:|
| local `L^3`, `|L|=80` | 512,000 | 3,072,000 | 1,024,000 | 1,024,000 | 1,023,488,000 |
| full `T^3`, `|T|=120` | 1,728,000 | 10,368,000 | 3,456,000 | 3,456,000 | 3,454,272,000 |

The full p=5 local Section 4 bit ledger is completely reconstructed from the
paper's edge-residual table. The nondata side and center histogram is
unchanged by the candidate:

| Scope | complete stock `W` | `m` | all-edge rank `s` | `Wm-s` | auxiliary rank mass |
|---|---:|---:|---:|---:|---:|
| local 80-port network | 61,120,000 | 1,000 | 61,123,328,000 | -3,328,000 | 60,099,840,000 |
| full 120-port h=10 network | 330,480,000 | 1,000 | 330,486,912,000 | -6,912,000 | 327,032,640,000 |

Both h=10 profiles fail `s<Wm`; neither is a Section 4 saving supplier. This
is a bound for these small h=10 profiles only. At the full `T^3` boundary the
candidate's baseline and changed ledgers are identical:

- all source, target, side, center, and scratch roles remain;
- every rank transition above survives at the same width and multiplicity;
- the center's old-value corrections and each side copy's inverse cleanup
  remain in their original stage;
- stage 1, 2, and 3 still use private scratch, with no shared-bank routing;
- no source birth, phase conversion, exterior correction, or new shared
  state is introduced;
- the signed source/sink frames and endpoint permutation are unchanged.

Thus the actual number of removed or reduced data children is **zero**.
The p=5 exact ledger is complete for this original Section 3/4 h=10
specialization. It is not a new all-size supplier profile.

## Paired-cube wrapper boundary

The frozen paired-cube sharing note at [PR 144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144)
uses a separate `m=3h` cover and records
`n_r=3(H_r+D_r+T_r)+2v·1_(r=2)+Σ_a s_a·1_(r=3a)`. If instantiated
with `v=80`, its two final width-two complement children per port would
remain 160 children; the three complete local cores and all exterior gauge
children would also remain. That profile is not mixed with the manuscript's
`m=h^3=1000` ledger above. A p=5 physical paired-cube supplier and its
`R_5` stock are not regenerated here, so no normalized moment is claimed for
that separate cover.

## Prior paid-data stopping gate

At pinned [PR 203](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/203),
retaining [PR 193](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/193)'s
complex or [PR 187](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/187)'s bit data children
cannot reach the diagnostic saving `0.01`, even after granting all auxiliary
work and center loss for free. The proof's exact data submultisets and ceilings
are:

| Profile | data children `(rank:multiplicity)` | `a` ceiling with center loss free | `a` ceiling retaining center loss |
|---|---|---:|---:|
| [PR 193](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/193) complex, `h=22,v=1320,ell=440` | `1:15840, 2:6600, 18:7920` | `<0.008866683` | `<0.004433342` |
| [PR 187](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/187) bit, `h=24,v=1760,ell=528` | `1:18480, 2:6160, 20:5280, 21:2640, 22:2640` | `<0.008897440` | `<0.004893592` |

This is the stopping rule for a candidate that leaves those data paths intact.
It does not bound a genuinely changed full data itinerary.

The source-assisted change in [PR 193](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/193)
selects donor/recipient pairs to avoid
parity erasure and reduces dirty births by 1,412 in its pinned complex flow;
the data path and bit supplier remain inherited. The completed entrance banks in
[PR 207](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/207)
remove 2,200 rank-60 exterior children in a separate p=72 supplier,
with nine replicas and all bank routing charged. Its own full-source-assisted
port rewrite fails donor stock, its selective A0 rewrite adds 440 rows, and
its G12 rewrite leaves the paid profile unchanged. None of these auxiliary
changes is a stage-1-to-2 data child reduction in the present h=10 ledger.
