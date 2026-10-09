# What is shared, and what is not

## Scope matrix

| Mechanism | Physical role or value shared | Pinned status | What remains paid |
|---|---|---|---|
| PR #128 | One original dirty auxiliary role is assigned to a whole orthogonal group and used by its complete scalar cores one after another within each stage. | Proved for its 87 source-defined groups and exact phase identity. | Every core's scalar gates, internal transitions, copied centers, data corrections and cleanup. Each partial group pays its signed orthogonal-complement child and adapters. |
| PR #130 | Data ports pass through three stage invocations with aligned data frames. | Proved as a global three-stage cover; its three auxiliary banks are independent. | Three local-word/histogram copies, data complements, rank-zero frame adapters, signs, Pauli/output correction, routers and copied centers. This is not one reused dirty auxiliary bank. |
| PR #144 | One physical auxiliary bank is routed sequentially through three orthogonal stage blocks. | Proved for the pinned paired-cube construction, including its raw gauge and correction ledger. | Three local word copies, copied centers, frame/gauge transitions, grouped `3 dim sigma` corrections, data rank-two complements, endpoint Pauli/phase adapters, routing and semantic/row guards. |
| Section 4 `Swap` | Fixed tapes and work areas are reused sequentially across recursive calls; the parent parks and restores inactive role streams around a child. | Explicit fixed-tape schedule in the original theorem. | Every one of the `s` pivot children is still called and charged in `(s/W)F_(k-1)`, plus each parent's linear-volume split/copy/restore work. |
| Computed logical payload across distinct recursive children | A value computed by one child and consumed by another distinct child. | **Not identified** in these pinned sources. | No charge can be removed until an exact repeated child input/output and ownership contract is found. |
| Multitype recursion | Switching among independently paid complete profiles. | Separate question, not a property of core sharing. | PR #83's result is limited to its 64 independently charged profiles; Issue #12's finite toy changed a local profile but kept the same asymptotic spectral radius. |

A dirty role receiving a new physical address transform is not a logical payload handoff. In PR #128 and PR #144 the preceding complete scalar word has restored its logical auxiliary values; the next invocation accepts an arbitrary dirty state under its own entrance gauge. The raw frame residual still changes and is accounted for. The proofs do not commute a prior residual through an internal gate or assume a clean scratch bank.

## Why the real two-core PR #128 example works

Take the first two labels in zero-based source group `groups[83]`: `(0,1,2)` and `(1,2,5)`. They overlap in two coordinates, so their dot product in `F_2^24` is zero. The first full core restores every scalar auxiliary value. Its raw address residual is `C_A0`. The next full core therefore receives an arbitrary transformed raw scratch state; its logical contract is valid for that state and restores it again, leaving raw residual `C_A0 C_A1`. Orthogonality gives `C_A0 C_A1 = C_(A0 direct-sum A1)` exactly, including the Walsh-diagonal phase.

This schedule continues over all eight labels in that actual source group. Once the eight cores finish, one role has residual `C_G`, not `C_F`; the paid `C_(G-perp)` child completes it. A size-24 group spans the whole address space and needs no positive-width correction. The allocation changes from separate `(stage,b,u)` role slots to `(stage,J,u)` slots; it does not declare two old independently dirty values equal.

The mechanism shares the **same physical workspace after each scalar core finishes** and combines the outer correction for the **whole orthogonal group**. It does not share an intermediate scalar output between those cores. The source explicitly retains all `2v` cores and their scalar gates, and says the scalar count is unchanged by sequential role reuse.

## PR #130 and PR #144 are different configurations

PR #130's central construction is its global data incidence cover. At `h=24`, its complex address dimension is 70 and its per-vertex allocation is `2v+3R=90,163`: three independent auxiliary banks. The three data shears line up their exit and entrance frames; rank-zero adapters still implement differences in exact representatives. Each data bank receives its paid rank-two complement and its actual source Pauli/sign/bank normalization. No PR #128-style cross-core auxiliary bank is removed here.

PR #144 keeps a three-stage cover but changes auxiliary ownership. Each `(g,r)` bank slot is routed to the local role `r` at `gH_j` for stage `j`; the active blocks `gP_1,gP_2,gP_3` are orthogonal. One role is used stage by stage, and the three relative physical actions tensor exactly. The local input gauge is part of that operator: `U=F_A T_sigma^-1`, with exact complete inverse `U^-1=T_sigma F_A^-1`. Omitting `T_sigma` changes the raw operator. For the selected 4,840 gauges of dimension 20, the final grouped correction is a real width-60 child, not a free return. A rank-zero Pauli and phase adapter also remains charged.

## Section 4 sibling calls do not carry a shared result

At a parent edge, the original theorem factors its rational matrix as `E_1 Pi E_2`. Every one in `Pi` invokes a child on its own pivot pair `(H_i,D_j)`, within a row-class stream whose remaining fields are spectators. The call swaps those address chunks on an arbitrary full bit array. Its returned array becomes the active parent stream; the next pivot may then mutate that stream again.

The source's storage schedule is sequential: park the other `W-1` role streams; copy/erase the active stream into the child area; push the descriptor; execute the child; copy the output into the designated parent role; pop and restore the parked streams; erase temporary stack cells. All this contributes `O(V)` per parent. This is **workspace reuse**. The recurrence still has one `(V/W)F_(k-1)` cost for each of the `s` pivot children. The source does not identify two pivots whose complete stream values, address fields, row class, frame and consumers coincide, nor does it identify a logical value produced by a child that the next child consumes without recomputation.

To turn this into computed-value sharing, one would need a source-defined pair of distinct child occurrences with an exact equality of the full input payload and shape, compatible entrance and exit `Phi_M` frames, clear ownership of a saved result, a proof that both consumers need the same output, arbitrary dirty spectator restoration, and paid copies/transfers/adapters. Nothing in the PR #128/#130/#144 core-sharing proof supplies that contract for Section 4 calls.

## Exact negative controls

Run `python3 research/completed-core-sharing-boundary/check_small.py` for deterministic, exact controls. It uses standard-library integer arithmetic, `Fraction`, and enumeration of spaces of dimension at most four.

1. **Phase and orthogonality.** The checker verifies `C_U C_V=C_(U direct-sum V)` for two nondegenerate orthogonal subspaces on every Walsh coordinate. It also checks that a triple line has `q=3 mod 4`, hence phase `-i`, so replacing the source phase by `+i` or `1` fails.
2. **Nonorthogonal cores.** For `U=<e0>`, `V=<e0+e1,e1+e2>`, and nondegenerate `U+V`, at Walsh coordinate `x=e0` the exact exponents are `q_U=1`, `q_V=2`, `q_(U+V)=1`. Thus the product gives `i^3=-i`, while the proposed combined transform gives `i`; merging a nonorthogonal pair is false.
3. **Incomplete dirty cleanup.** A two-role reversible shear uses `M(a,b)=(a+b,b)`, `Vx=(0,x)` and `J=(1,0)`, for which `JMV=1`. The complete signed word restores every tested integer dirty vector. Omitting the final inverse cleanup leaves `(1,1)` from dirty `(0,0)` with `x=1`.
4. **Entrance gauge.** In the exact two-coordinate subcase `F=C tensor C`, `T_sigma=C tensor I`, `U=F T_sigma^-1=I tensor C`. On `|00>`, the coefficient of `|10>` in `U|00>` is zero, while it is `1/2` in `F|00>`. Treating the raw input gauge as identity therefore changes the operator. This is a small algebraic control of the source equation, not a claim about a physical event ID.
5. **Unpaid complement.** For `A=<e0>` in the same two-coordinate model, `C_A` does not equal the full `C tensor C`; on `|00>` even the `|10>` coefficient is `(1-i)/2` in `C_A` and `1/2` in the full transform. The complement child supplies a real missing transform.

The controls test the identity boundaries, not the full upstream compiled words. PR #128's exact phase proof, signed group generator and paid profiles remain the primary source for its 24-dimensional construction.

## Limits of nearby negative results

- PR #83's pinned body proves no benefit from adaptive switching among 64 **complete, independently paid** profiles in that defined family, using its exact nonuniform child weights. It explicitly does not rule out computation shared between child occurrences or arbitrary multiplication algorithms.
- Issue #12's paired-output toy saved finite depth-four work (50 versus 91 under its stated one-frame paired-return assumption) but both operators kept spectral radius 2. It shows that a finite gate saving need not lower the asymptotic recurrence; it does not disprove a new source-backed payload handoff.
- Issue #21's PR #63 h=23 candidate reduced five whole-word XORs while adding two roles and 46 event-plus-endpoint rank units. Its complete child moment was not recomputed. It is a stopping point for that one-carrier search, not a global impossibility result.
