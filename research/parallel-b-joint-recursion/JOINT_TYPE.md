# Two candidate joint children

This checkpoint asks whether a multi-output type can remove a genuinely paid multiplication child. Types below are fully specified at the coefficient level. Neither is asserted to implement the original Section 4 address-swap child.

## Candidate A — shared-left full convolution `J_n`

Let `F` be a characteristic-zero field. The input is three independently supplied coefficient arrays

```text
A = (a_0,...,a_{n-1}), B = (b_0,...,b_{n-1}), C = (c_0,...,c_{n-1}) in F^n.
```

The complete output is two full products, each with `2n-1` coefficients:

```text
J_n(A; B,C) = (A B, A C) in F^(2n-1) × F^(2n-1).
```

`A` is read-only and shared; `B` and `C` are independent. The type has no dirty scratch on entry, preserves all three inputs, and returns both outputs to separate owners. A caller must retain/write both outputs. No carry or output window is implicit.

The proposed mechanism is to evaluate `A` once at each Toom node and replace two size-`n` multiplication trees by a recursive paired child. For an `r`-way Toom split, `t=2r-1` evaluation products are required for each output. At every evaluation point `λ`, the child receives `(A(λ); B(λ),C(λ))` and returns both products. The child DAG therefore has `t` calls of type `J_ceil(n/r)`, versus `2t` calls of type `M_ceil(n/r)` in an unpaired spelling. Expanding each paired child still yields two multiplication outputs. The cheapest fatal test is the output flattening rank of the bilinear map `F^n × F^(2n) → F^(4n-2)`; if it is `4n-2`, no bilinear scalar-multiplication leaf can disappear.

This is distinct from merely retaining completed child payloads: the proposed common operand is present before child products are formed. It can remove repeated linear evaluation or input traffic. The test below determines whether it removes a recursive multiplication leaf.

## Candidate B — guarded packing of two independent products

The input is four independent `n`-bit integers `A,B,C,D`. The output is `(AB,CD)`, both exact `2n`-bit products. Encode

```text
P = A + 2^(2n+1) C
Q = B + 2^(2n+1) D.
```

The exact product is

```text
PQ = AB + 2^(2n+1)(AD+CB) + 2^(4n+2)CD.
```

Since `AD+CB < 2^(2n+1)`, the three regions do not overlap. Decode the low `2n` bits as `AB`, the `2n` bits starting at position `4n+2` as `CD`, and discard the guarded cross term. The state is the two packed operands and the full packed product; all input packing, zero guards, output reads, and discarded middle bits are charged. The child DAG has one call `Mul_(3n+1)` instead of two `Mul_n` calls, so this is a real changed child size, not a rename. Its cheapest screen is the same-model comparison `M(3n+1)+O(n)` against `2M(n)+O(n)`.

This is standard guarded digit/Kronecker packing. Under a fixed-shape model `M(n)=Θ(n^α)`, `α≥1`, its leading ratio tends to `3^α/2>1`; for a near-linear regular cost `M(n)=nL(n)` with slowly varying `L`, the ratio tends to `3/2`. It therefore fails the paid-gain screen in these standard scaling models. An upper bound alone does not prove a lower bound for every possible irregular `M`; no such universal assertion is made.

## Selection

Candidate A is the pilot because it has a nontrivial correlated input, an exact full-output type, and a direct bilinear lower-bound test. Candidate B already reduces to a widened standard multiplication and loses under the relevant scaling screen. The selected result is scoped to field-bilinear Toom recursion; it does not rule out nonlinear bit-state or a redesigned global reduction.
