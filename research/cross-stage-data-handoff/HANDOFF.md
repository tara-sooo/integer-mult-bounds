# Typed stage 1 → 2 handoff

## Candidate and falsifiable equation

The first candidate is the existing `Y_a` data role. For every
`a in T^3`, let

```text
H_a := Y1_a = Y0_a + X0_a.
```

The candidate handoff claims that this one value is available first as the
stage-2 source and remains the stage-3 target input:

```text
Y2_source,a = H_a = Y3_target,in,a.
```

Stage 2 leaves `Y_a` untouched, so the equality is exact. The required target
updates are `X2_a=X0_a-H_a=-Y0_a` and `Y3_a=H_a+X2_a=X0_a`. This equation is
falsifiable at a real array address and is checked at `a=({0,2,4}, {0,2,4},
{0,2,4})` in the full h=10 triple type.

The handoff does not claim that a Section 4 recursive child result is
reusable. To claim a paid saving, the complete child input, operation,
frames, spectators, and returned output would have to match across histories,
or the changed itinerary would need a new exact factorization and ledger. This
candidate changes no edge or frame, so it removes no such child.

## Chronology, owner, and arbitrary dirty scratch

For one local invocation, write `a` for arbitrary side scratch and `c` for
arbitrary center scratch. The source's eight-row forward schedule first
subtracts `J a + R c`, injects `Vx,Gx`, adds `J(a+Vx)+R(c+Gx)`, then applies
the inverse injections. The result is

```text
target' = target + (J V + R G)x = target + x
side'   = a
center' = c.
```

This is an identity for every initial `a,c`, not only zero scratch. The
stage-2 operation is the exact time reverse with source `Y1` and target `X1`,
so it subtracts `Y1` and restores its own scratch. Stage 3 uses fresh,
invocation-owned scratch. The signed data sequence is therefore
`Y+=X`, `X-=Y`, `Y+=X` in strict completed-stage order.

No dirty bank is shared between stage calls. Each stage's source remains
unchanged during its own shear; its inverse cleanup runs before a later stage
can write that source. At the interstage boundary, `Y1` is the same logical
value, with the source-pinned outgoing and incoming frames equal. There is no
phase adapter, gauge conversion, copied center, or endpoint change added by
this handoff. Existing source/target endpoints and the two final role
complements in any retained paired-cube wrapper remain paid.

The bit schedule is checked over `F2` using its own intersection-one side
edges and parity center. It is not obtained by reducing the complex dyadic
schedule.

## Exact p=5 local block and negative controls

The fixture enumerates all 80 ports and ten full eight-selector cubes. It
checks all entries of `K+H+B=I`, every cube's `K^2=I`, all nonzero side-support
orthogonality conditions, the coordinate-star factorization, and the
source/center matrix identity. It separately checks the original Section 3
side-plus-center identity on all 120 triples.

The stage exchange is checked on a basis of both banks, for both the signed
complex action and the characteristic-two bit permutation. Each local
forward and inverse schedule is run with nonzero arbitrary side and center
scratch across every source basis vector; all scratch returns to its original
contents.

Two adverse controls pass:

1. **Interstage chronology:** stop stage 1 before inverse cleanup, let stage 2
   overwrite `X`, then attempt stage-1 cleanup from the changed `X`. The
   chosen one-hot source leaves both side and center scratch nonzero.
2. **Dirty cleanup and sign:** omitting stage-1's final cleanup strands the
   injected source in scratch. In the complex case, replacing stage 2's
   required minus with plus sends a one-hot `Y0` to `Y3=2` instead of the
   required `Y3=0`.

The exact scripts and receipt are in `check_small.py` and `receipt.json`.
