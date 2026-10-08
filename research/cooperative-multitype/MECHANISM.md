# Cooperative pair producer: exact toy mechanism

**Status: `OPEN_INTERFACE_OBSTRUCTION`.** A small Boolean circuit has a real
shared-child producer and a changed typed child profile. Its exact recurrence
does not improve the contraction eigenvalue. Whether the same interface can
be built in either pinned multiplication construction remains open.

## Types and functions

This toy uses pure Boolean functions on `n = 2^k` input bits. The three types
are:

| Type | Input | Output | Scratch |
|---|---|---|---|
| `F` | `n` bits | one bit `F_k` | none |
| `G` | `n` bits | one bit `G_k` | none |
| `C` | `n` bits | `(F_k, G_k)` | none |

The base functions and split recurrences are

```text
F_0(x) = x                 G_0(x) = NOT x
F_k(u,v) = F_(k-1)(u) XOR F_(k-1)(v)
G_k(u,v) = F_(k-1)(u) AND G_(k-1)(v)
```

Here `u` and `v` are the equal halves of the input. Thus `F` has children
`F(u), F(v)`, while `G` has children `F(u), G(v)`. A `C` producer computes
both outputs by evaluating `F(u)` once and calling `C(v)` for the two values
needed on the right:

```text
f_left = F(u)
(f_right, g_right) = C(v)
return (f_left XOR f_right, f_left AND g_right)
```

This is a new typed producer, not a reassignment of the original `F` and `G`
children. Each recursive child has half the input size. The child profiles
follow directly from the definitions; no matrix entries are selected by hand.

Claim status within this bounded scope:

- **PROVED:** the three child lists and the equality of the two spectral radii.
- **FINITE-CHECKED:** function outputs through depth 2 and costs through depth
  8 in the included checker.
- **ASSUMED (toy convention):** each recursive invocation costs one frame
  unit, and circuit wires may fan out without a gate.
- **UNKNOWN:** whether a paired type can be emitted and consumed in a legal
  PR #62/#63 physical frame with its ownership, dirty-state, and tape rules.

## Exact cost convention

The finite toy counts one unit per recursive child frame and one per Boolean
gate. Wire fan-out is free, as in this circuit model. The local costs are two
child frames plus one gate for `F` and `G`, and two child frames plus two gates
for `C`. `G_0` and `C_0` each use one NOT gate. There is no type conversion in
this toy: every child receives exactly the function and input specified above.
Returning the pair from a `C` child uses the same one frame unit as a scalar
child; this is an explicit toy assumption, not a claim about tape layout.

The convention is explicit so it can be replaced by physical frame, tape, and
scratch costs later. Those costs are not claimed for the integer-multiplication
constructions.

## Child-work operators

Rows are parent types and columns are child types, in order `F,G,C`. The
standalone `F,G` operator and the cooperative operator are

```text
B = [[2, 0], [1, 1]]
A = [[2, 0, 0],
     [1, 1, 0],
     [1, 0, 1]]
```

`C` has the new row `[1, 0, 1]`: one `F` child on the left and one `C` child
on the right. If `q` is the input-size growth exponent, every child-size ratio
is `1/2`, so the recurrence operators are `2^-q B` and `2^-q A`. Both
matrices are triangular. Their spectral radii are exactly

```text
rho(2^-q B) = rho(2^-q A) = 2^(1-q).
```

For the paired output, output-coordinate normalization uses weights `(1,1,2)`
for `F,G,C`. It changes `C`'s row to `[1/2, 0, 1]`, with row sum `3/2`, but is
a diagonal similarity transform and leaves the spectral radius unchanged.
This is the precise obstruction in this candidate: sharing changes the row
profile, yet the recurrent `F` branch keeps the dominant eigenvalue at `2`.

`q` is a generic toy growth exponent, not Issue 10's bit saving `a_b` or a
claimed `κ`. No conclusion about the pinned profiles follows from this model.

## What would make this relevant

The needed missing interface is a producer in the pinned construction that
can return both typed child states in one legal frame while preserving their
source ownership, arbitrary dirty scratch, and fixed-tape layout. Its complete
physical cost would have to make the charged child-work operator's
spectral radius strictly smaller, after charging frame creation, conversions,
resets, and tape movement. The PR #62/#63 ledgers do not record such a typed
pair boundary.

Even a successful small interface would require a regenerated mixed profile
and the outer assembly checks (47 strict constraints and seven margins) before
it could affect the conditional exponent.
