# Completed-core and recursive-call contracts

Audit tier: **FAST source map** plus the small exact checks in `check_small.py`. The cited conditional constructions assume their inherited analytic, precision, fixed-tape, recovery and streaming interfaces; this note proves none of those all-size interfaces.

The frozen inputs are upstream PR #128 at commit `530588a019b4a74f09180680c9e3961bf649ec89`, PR #130 at `6a9970a530119174507904e23592fd59ede19a5d`, and PR #144 at `c8b22bc5c10dba497ac25804e27d9647d818e2ff`. They are separate construction checkpoints, not three successive profiles that can be combined.

## PR #128: scalar core, raw frame and shared group

### Scalar input/output contract

For an outer triple label `b`, the complete scalar core has the logical contract

    (d, a) -> (L_b d, a)

for every original auxiliary vector `a`. The vector may be nonzero and correlated across all scratch roles. In the transparent carrier word, `M` is the reversible carrier transform, `V` injects the source, and `J` reads out the side/center results. The chronological operations are

    M; -J; M^-1; V; M; J; M^-1; -V.

The target increment is `-JMa + JM(a + Vx) = JMVx`; the inverse cleanup restores each auxiliary role separately. The source proves `JMV=I` for its scalar word. This is the reason the next core may receive the arbitrary dirty state left by the prior core. Dropping either cleanup operation breaks that contract.

This logical identity does **not** say the physical address/frame action on scratch is identity. In the common Walsh coordinates the source defines

    C_U = H^-1 diag(i^q_U(x)) H,    q_U(x) = wt(P_U x) mod 4.

Before the terminal exterior, stage one leaves residual `C_A`, where `A = F_2^24 tensor <t_b>`. Stage two has source `C_(A-perp)` and pre-exterior sink `C_F`; its residual is `C_F C_(A-perp)^-1 = C_A`. The source inverse is essential: reversing the logical shear alone does not make this residual `C_A^-1`.

### Source-defined sequential sharing witness

The pinned `pr-network-mrp24-signed.json`, `groups[83]` (zero-based; one of the four partial groups), contains these eight triple labels in `F_2^24`:

    (0,1,2), (1,2,5), (6,7,8), (7,8,11),
    (12,13,14), (13,14,17), (18,19,20), (19,20,23).

For the first two, the intersection has size two, so their binary dot product is zero. The full source group has Gram matrix `I`; the small checker verifies all eight rows. Let `A_b = F_2^24 tensor <t_b>`. One role `u` in the source allocation `(stage, J, u)` is used by these cores consecutively. After the first scalar core its logical scratch values are restored, while its raw address residual is `C_A_b1`. After the second they are still logically restored and the raw residual is `C_A_b1 C_A_b2 = C_(A_b1 direct-sum A_b2)`, with the exact phase included. No prior core output is passed as a logical input value to the next core.

After all eight cores, `G_J = direct-sum_(b in J) A_b` has dimension `24*8=192` inside the 576-dimensional address space. The shared role then receives the paid correction `C_(G_J-perp)`, of width 384, to make the full `C_F` action. The 83 full groups of 24 need no complement; each of the four partial groups does. This is reallocation of original role slots, not aliasing of independent dirty values. The core-sharing step keeps every scalar gate, internal transform, copied center and data correction; it replaces per-core terminal exteriors with the correctly charged group correction. PR #128 separately changes the copied-center histogram, whose rank and copy costs remain in the child list.

The outer complement is itself signed. The partial-group basis uses eight weight-three directions and eight unit directions; the eight inverse directions use `C^-1 = -i Z C Z`, and the binary basis adapters and `Z` signs are paid. The scalar `(-i)^8=1` does not remove those operations or the width-384 child. The source distinguishes these outer complements from the 3,308 internal alternating rank-two residuals.

## PR #130: three-stage data cover, independent auxiliary banks

The complex branch uses `E=A perp B perp C`, with dimension `m=3h-2=70` at `h=24`. Each data port visits three invocation vertices. The logical data shears are `Y <- Y+X`, `X <- X-Y`, `Y <- Y+X`; their active spaces are `B+q`, `A`, `C+q`. At stage boundaries the data frames match. Exact representatives that differ are reconciled by real rank-zero adapters, so there are no positive-rank data connectors; the adapters remain in the scalar/router charge.

In each local invocation, the complete scalar word has the arbitrary-dirty contract `(d,z) -> (L_b d,z)`; its signed readout adds `JMVx` and its inverse word restores every original auxiliary. The middle global stage uses the full reverse/complement local word, with source and target exchanged and the scalar sign reversed.

The exact data entrance gauges are `(T,I)` and terminal gauges `(F,FT^-1)`. The raw output is `(-Fy, F T^-2 x)`. Since `T^2` is the actual Pauli translation on the transported source, the source pays that translation together with output sign and bank exchange to obtain `(Fx,Fy)`. Each data bank also pays its rank-two complement.

This is an outside-cover/data-incidence change. The source says the three auxiliary banks are independent and charges three copies of the local auxiliary, data and copied-center histograms. Its per-vertex role count is `2v+3R`, not a reused `R`-slot bank. It therefore does not establish the PR #128 scratch-slot sharing or a shared recursive payload.

## PR #144: one auxiliary bank through three orthogonal stages

PR #144 adopts the completed-core principle in a different three-stage cover. The physical auxiliary bank is indexed by `(g,r)`. In stage `j`, it routes to local role `r` at vertex `g H_j`; the active subspaces are the three orthogonal blocks `gP_1`, `gP_2`, `gP_3`. Each stage runs its complete local core in sequence. The role is never used concurrently by two invocations.

Each local core has the same scalar input/output shape `(d,z) -> (L_b d,z)` for arbitrary dirty `z`; all signed old-value reads, copied centers and inverse cleanup belong to that word. For a selected entrance gauge `T_sigma`, it restores the logical dirty value `\hat z`, while the raw core maps `z=T_sigma \hat z` to `F_A \hat z`. Its exact operator and complete reverse are

    U = F_A T_sigma^-1,       U^-1 = T_sigma F_A^-1.

The reverse includes signed old-value corrections, copied centers and full inverse cleanup; it is not the inverse of the positive DAG alone. The three stage-relative actions tensor because their active blocks are orthogonal, with their phases intact. For a forward block the final correction is `F_A U^-1 = F_A T_sigma F_A^-1`, of Fourier rank `dim sigma`; for the reversed block it is `F_A (U^-1)^-1 = F_A^2 T_sigma^-1`, of the same rank. The grouped tensor correction is one paid child of width `3 dim sigma`. The endpoint's exact ratio to the canonical ambient transform is a fixed Pauli and phase, charged in the router guard. No commutativity of distinct intermediate frame representatives is assumed.

In the selected local profile, 4,840 source-selected roles have `dim sigma=20`; the grouped correction is consequently 4,840 children of width 60. The stage data banks separately pay their rank-two complements. This is cross-stage physical workspace reuse plus combined whole-core correction, not an identified share of a value computed by one Section 4 child and consumed by another.

## Original Section 4: recursive `Swap` call boundary

The pinned original manuscript's Proposition `prop:power-interchange` and Lemma `lem:chunk-swap` define a different interface. A call takes an arbitrary bit array with two `q^e` address chunks and a preceding row field divisible by `W^k`, where `e=m^k`; it swaps the two chunks and preserves every other field and payload bit. At a recursive level, each one in the partial permutation matrix `Pi` of an edge factorization `A_e=E_1 Pi E_2` calls `Swap_(k-1)` on one pivot pair of `b=e/m` digit fields in one role stream.

If `s_swap` is the sum of the rational edge ranks and `W` is the fixed role count, the source recurrence is `F_0=O(1)` and `F_k <= (s_swap/W)F_(k-1)+O(1)`. It explicitly charges `O(V)` per parent for row splitting/merging, gate and triangular work, descriptors, parking the `W-1` inactive streams, copying and erasing the active stream, copying the child output back, and restoring/erasing parked streams. The child is an address permutation on the full arbitrary stream, not a named complex scalar intermediate. This Section 4 call boundary does not expose a mutable typed result that persists between sibling calls. The widths in the PR #128/#130/#144 outer child profiles are a different recurrence level; no source maps one profile row to a particular Section 4 pivot call.

## Sources for the equations

- PR #128 `research/completed-core-sharing/PROOF.md`: §§1–4, especially lines 13–34, 72–91, 93–144, 146–201, 203–240 and 242–276; `README.md` lines 37–52 and 64–70.
- PR #130 `notes/three-stage-cover-complex.tex`: lines 1–27, 29–69, 71–101 and 103–127; `notes/three-stage-cover-rows.tex` lines 1–34, 35–69 and 70–100.
- PR #144 `notes/paired-cube-sharing.tex`: lines 1–59 and 61–96; `notes/paired-cube-construction.tex` lines 113–140; `notes/paired-cube-assembly.tex` lines 1–50 and 50–92; `notes/general-clifford-frames.tex` lines 39–102.
- Original pinned manuscript `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, `build/sections/04-swap.tex`: Lemma `lem:matrix-shear`, Proposition `prop:power-interchange`, equation `eq:swap-recurrence`, lines 86–100, 103–127, 129–143, 151–187, 197–242 and 285–301.

See `SOURCES.md` for hashes and attribution.
