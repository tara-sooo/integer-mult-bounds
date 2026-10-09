# One predeclared shear

## Definition

Port labels use the exact [PR 144](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/144) order recorded in `BASELINE.md`. Choose the
first cross-cube ordered pair `(a,b)` in that order: `a=0`, with cube
`(0,1,2)`, bits `000`, port `(0,2,4)`; `b=8`, with cube `(0,1,3)`, bits
`000`, port `(0,2,6)`. Set `lambda=+1`, and let `E_ab` have its only nonzero
entry at row `a`, column `b`.

```text
C       = I + E_ab
C^-1    = I - E_ab
K'      = C K C^-1
B'      = B
H'      = I - K' - B'
```

The exact matrices, digests and every changed coefficient are in
`small_exact_receipt.json`. The doubled-integer checker confirms `CC^-1=I`,
`K'^2=I`, and `K'+H'+B'=I`.

## Exact obstruction

This formal conjugation moves the original coefficient `K[b,S]=-1/2` into
`K'[a,S]=-1/2` for `S=(0,3,6)` (source-order index 10). The addresses are

```text
q_a = e_0 + e_2 + e_4,    address mask 21
q_b = e_0 + e_2 + e_6,    address mask 69
q_S = e_0 + e_3 + e_6,    address mask 73
```

`q_b dot q_S = 0` because the original source and target share two
coordinates. `q_a dot q_S = 1` because the moved source and target share
only coordinate 0. Therefore the changed nonzero `K'` entry at
`(T,S)=((0,2,4),(0,3,6))` violates the pinned physical cap. `H'` has a
violation on the same pair. Each candidate matrix has four violations
among all of its nonzero entries.

The changed K/H operators are different matrices in the fixed port basis,
but they are a paid similarity transform and this support is illegal. They
do not constitute a source-typed lawful operator. `C` and `C^-1` each mix
two actual port roles and require their own scalar, frame, routing and dirty
restoration charges; neither is a free coordinate rename. Since the cap
fails, no further candidate search or typed implementation is performed.

This is scoped to the single first-ordered `lambda=+1` shear. It is not a
no-go result for other signed decompositions, other encodings, or all
cross-cube mixings.
