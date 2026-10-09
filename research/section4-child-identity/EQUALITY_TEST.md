# Complete-input equality test

## What must match

The two examined calls have deceptively similar profiles: they are both
rank-one pivots of the same rank-100 edge, run on the same `C_1` role stream,
at the same recursion level and with the same complete array shape. Their
target fields are different:

```text
call 1: (H_1, D_999901)
call 2: (H_2, D_999902)
```

A cache of a `Swap_1` result is valid only for the same complete input bit
array and the same field pair/frame. Equal rank, row class, field width, or
array dimensions do not meet that condition.

## Exact live-state separator

Let `Z_0` be the complete stream after the edge's invertible triangular
pretransforms. Choose it to be a one-hot bit array in row `g=0`, at an address
with

```text
H_1=0, D_999901=1, H_2=0, D_999902=0,
all other address coordinates = 0.
```

All values are legal in every permitted radix field. Since the source-frame
and triangular pretransforms are permutations, this `Z_0` has a valid
arbitrary dirty source array as its preimage.

For call 1 the pre-shear sees `H_1=0`, so it leaves the one-hot address where
it is. Its complete input `Z_1` has the one at the address above. The three
operations for this pivot have the exact address effect

```text
(H_1,D_999901) = (h,d)
 -> (h,d+h) -> (d+h,h) -> (d+h,d)
```

Thus the completed first pivot is `(H_1,D_999901) <-
(H_1+D_999901,D_999901)`. It moves the one to
`H_1=1, D_999901=1`. Call 2's own pre-shear sees
`H_2=D_999902=0` and does not move it. Its complete input `Z_2` therefore has
the one at the changed address. Hence `Z_1 != Z_2` as full bit arrays for this
legal input. The complete arbitrary-payload input maps are not universally
equal.

This is an exact source-faithful counterexample, not a run on an invented
network. It uses the source-defined `C_1` scratch role, the real rational edge
above, the exact two `Pi` pivots, and the theorem's arbitrary-dirty input
domain. A particular symmetric payload (for example, the all-zero array) can
make two concrete bit strings coincide; it does not give an input-independent
handoff for the algorithm.

## Negative controls

1. **Equal rank and width, different operation.** At an address with
   `H_1=1,D_999901=0,H_2=0,D_999902=0`, swapping call 1's pair moves the bit
   address; swapping call 2's pair leaves these four fields unchanged. The
   two child functions are different even before charging copies or frames.
2. **Dirty spectator included.** A one-hot bit differing only in any of the
   other `2m-2` coordinate fields (or row `g`) is part of the complete child
   input. Both calls preserve it as a spectator. A cache keyed only by the
   active pair would conflate distinct full inputs.
3. **Sequential live version.** The first pivot changes the full active
   stream before call 2. Reusing call 1's prior output as if it were call 2's
   input omits the exact `(H_1,D_999901)` update shown above.

`check_small.py` checks the exact projector factorization, the first two
coordinates, the separating one-hot state, the distinct swap functions, and
the spectator-preservation control. It keeps the million-dimensional
Kronecker lift symbolic; the displayed rank-one identities prove the lift
exactly.
