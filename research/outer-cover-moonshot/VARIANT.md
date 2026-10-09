# One outer-incidence variant

## Definition and predeclared lever

Keep the coordinate pairs and the 3-subsets of pair labels, but retain only selector strings of even parity in each cube:

```text
baseline cube: epsilon in {0,1}^3              (8 ports)
candidate:     epsilon in {0,1}^3, sum epsilon=0 mod 2  (4 ports)
```

This is a genuine port-set change: at p=4 it changes four distinct 8-port cubes into four 4-port sets, halves the total count from `v=32` to `v=16`, and halves each coordinate's incidence from 12 to 6. Cardinality and incidence distinguish it from coordinate relabeling, selector renaming, block naming, or carrier rerouting.

The measurable lever was declared before checking the identity: lower every per-port outer term by halving `v`. In particular, the paid `2v` width-two data-complement children would fall from 64 to 32 per full-group local ledger if all endpoint proofs survived. The `2v` data-role term would also fall by 32 before accounting for any replacement word. This is only a candidate saving; `R`, new local channels, centers and frame corrections were not presumed unchanged.

## Exact result

Apply the frozen formulas to one p=4 cube, with selector ports `000, 011, 101, 110`. Every two distinct selected strings have Hamming distance two, so their coordinate supports intersect in one position. Thus

```text
B_block[epsilon,epsilon] = 1
B_block[epsilon,epsilon'] = 0  when epsilon != epsilon'
B_block = I_4
K = I_4 - B_block = 0
K^2 = 0 != I_4.
```

For the first port, the exact counterexample is `(K^2-I)[000,000]=-1`. The required signed involution fails before any outer router or supplier question. The checker also confirms the nominal complement count would be 32, so the apparent lever is real as a count but cannot be booked as a legal saving.

## Minimal missing condition

Under the frozen `B_block` and `K=I-B_block` definitions, each cube must retain the antipode and its three distance-one neighbors for every selector, with the full eight-selector 3-cube incidence. Those entries give `K=(P-A)/2` and `K^2=I`. The even-parity half-cube omits all odd-parity targets, erasing every such within-block K entry.

A smaller port set would need a new local involution `K'` and a new producer/cover proof establishing, together, `K'+H'+B'=I`, `K'^2=I`, orthogonal source supports for every side read, full data coverage, signed dirty restoration, and frame-compatible endpoints. No such term or theorem is present in either pinned baseline. Reusing the old K word or its frame proof is invalid. The selected variant therefore fails the required geometry identity; this does not rule out other outer covers.

This is the only geometry variant tested in this milestone. No port search or supplier regeneration followed the exact counterexample.
