# First bounded result

**Outcome: `OPEN_INTERFACE_OBSTRUCTION`.** The model constructs a legal
shared-child pair producer, but the exact recurrence has the same spectral
radius as the separate `F/G` baseline for the same paired output. This
establishes neither a recurrence contraction gain nor a multiplication
improvement.

## Derived profile and exact comparison

From the Boolean definitions in [`MECHANISM.md`](MECHANISM.md):

| Parent | Recursive children | Local gates |
|---|---|---:|
| `F` | `F(u), F(v)` | 1 XOR |
| `G` | `F(u), G(v)` | 1 AND |
| `C=(F,G)` | `F(u), C(v)` | 1 XOR, 1 AND |

The child operators are `B = [[2,0],[1,1]]` for `F,G` and
`A = [[2,0,0],[1,1,0],[1,0,1]]` after adding `C`. Their diagonal entries give
`rho(B) = rho(A) = 2`, exactly. At the rational check point `q=1`, both
size-scaled operators have spectral radius `1`. The `C` row changes from the
fixed profiles, but the `F` self-recursion still determines the spectral
radius. Issue 11's unchanged-row routing bound does not apply to the new row;
this candidate instead fails at the eigenvalue comparison.

The comparison target is the same pair `(F_k,G_k)`: the fixed-producer
baseline runs both scalar producers, while `C` returns both coordinates.
After normalizing by output-coordinate widths `(1,1,2)`, `C`'s row action is
`(3/2) 2^-q` (equal to `3/4` at `q=1`), below the scalar rows' `2 2^-q`
(equal to `1` at `q=1`). The full operator still has radius `1` at that point
because its `F` row is recurrent. Thus this is a changed child profile with a
strictly smaller local row action, but no smaller global contraction.

The finite work recurrence includes every gate and one frame unit per child
call. For depth `k`, it starts at `(T_F,T_G,T_C)=(0,1,1)` and adds local costs
`(3,3,4)` to the child-work rows above. At depth 4, `C` computes the same
paired outputs for 50 units; separate `F` and `G` invocations cost 91. This
finite saving uses the stated one-frame paired-return assumption. The repeated
depth eigenvalue stays unchanged, so the finite saving is not an exponent
saving.

## Controls

- **Fixed-profile control:** Issue 11's exact pinned-profile experiment remains
  the control for routing unchanged children. At its common exponent,
  `M_A > M_B`; zero-fee alternating radius is strictly above the better
  standalone `M_B` interval. The proof there gives the general nonnegative
  row-sum obstruction for this routing-only model.
- **Positive switching overhead:** the same pinned experiment checks
  `delta = 1/10^10`; its alternating-radius lower bound is
  `999999997651128320058560/10^24`, above the `M_B` upper bound
  `999999995103647183328969/10^24`. The `delta = 1/1000` control is above one.
- **Illegal free conversion:** at depth one and input `(u,v)=(1,0)`, the true
  `G_1` is `F_0(1) AND G_0(0) = 1`. Replacing `G_0(0)` by `F_0(0)` without a
  converter gives `0`. The checker asserts this mismatch.

## Reproduction

Run:

```sh
python3 research/cooperative-multitype/experiment.py
```

The deterministic standard-library checker exhausts all inputs through depth
2, asserts the stated child matrices and output-width normalization, verifies the
triangular spectral radii at integer `q=0,1,2`, checks finite gate/frame costs
through depth 8, and exercises the free-conversion counterexample. Recorded
runtime on Termux: under one second.

Validation status: **FAST PASS** (the bounded checker and the pinned Issue 11
toy were run); **FOCUSED NOT RUN**; **FULL NOT RUN**. `make verify` was not run.

## Scope and next step

This is a self-contained finite Boolean circuit model. It shows how a joint
producer can change a typed child profile by sharing a recursive value. Under
the explicit rank and size accounting, that mechanism alone does not lower
the recurrence spectral radius. The remaining concrete question is whether a
real producer can reduce the *charged* frame/layout work or the rank-weighted
child operator while retaining a typed state at the next layer. The pinned
profile certificates do not expose the semantic child state needed to test
that interface; solving that data/interface gap is the next step.

Prepared with OpenAI Codex assistance. The source constructions and prior
research retain their original attribution; this toy claims no inherited
construction and no value of `κ`.
