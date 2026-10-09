# Paid cost boundary

## Existing Section 4 charge

For the original paper's bit network,

```text
m = 1,000,000
W = 177176569091445000000
s_swap = 177176569088785861287000000 < W*m
F_k <= (s_swap/W) F_(k-1) + O(1).
```

The selected real edge has rank 100 and therefore contributes exactly 100
`Swap_(k-1)` calls, one for each one in `Pi`. The two occurrences studied here
are two of those calls. At `k=2`, each has the full active-stream volume
`V/W = W q_*^(2m^2)` and cost term `(V/W) F_1`; the pair contributes
`2(V/W) F_1` before the parent overhead. No role or child is removed by this
audit.

The source's `O(V)` parent term already pays the finite matrix operations and
every recursion boundary operation: park the other `W-1` streams, copy the
active stream into child I/O, erase the parent copy, push/pop descriptors,
copy the returned child output back, and restore the parked streams. The
lower-triangular factors and the pre/post affine updates are also paid in this
term. The complete child shape includes every spectator field and payload
bit; the recursive cost is not charged only on the two active coordinates.

## Reuse ledger

The inputs fail the exact equality test, and the children implement different
coordinate swaps. Therefore the legal cacheable-child count is zero in this
pair, the actual saved child term is zero, and the paid multiset remains
unchanged. There is no value owner that can fan one returned array into two
independent consumers: the first child returns to the active role, its parent
post-update mutates that stream, and call 2 then consumes the new version.

For scale, a hypothetical cache would have to retain and move a full
`V/W`-bit returned stream, plus preserve the current live stream while the
first output is used. Any field permutation, frame conversion, snapshot,
restore, fixed-tape parking, and return copy would be additional paid work.
Those costs are not assigned zero. Since neither the complete inputs nor the
child operations match, no handoff is legal and a hypothetical transfer
ledger cannot create a saving. The existing Section 4 schedule and its paid
child multiplicities are kept intact.

The paper gives asymptotic `O(V)` bounds rather than exact finite tape-step
constants, so no sharper numerical transfer cost or positive cost interval
is claimed here.

## Claim limits

This exact pair does not improve `s_swap`, the full recurrence moment, or
`kappa`. It does not prove a typed recursive interface. It is a no-go only for
the tested pair on this one real edge, not an impossibility theorem for all
edges or all multiplication algorithms.
