# Rank-one source-line adapter

## Exact fixture and result

Take `h=4`, `m=64`, `A={1,2,3}`, `B={1,2,4}`, `a=(A,A,A)`, and `b=(A,A,B)`. Flatten `[4]^3` in lexicographic order. The vectors `u_a,u_b ∈ Z^64` have weight 27 and overlap 18. Choose `i=(1,1,3)` in `supp(u_a)` but not `supp(u_b)`, and `j=(1,1,4)` in `supp(u_b)` but not `supp(u_a)`. Set

\[
d=u_b-u_a,\qquad \varphi(x)=x_i-x_j,\qquad P=I+d\varphi.
\]

The exact values are

\[
\varphi(u_a)=1,\quad \varphi(u_b)=-1,\quad \varphi(d)=-2.
\]

For any field or ring where these coordinates are interpreted,

\[
P^2=I+(2+\varphi(d))d\varphi=I.
\]

The determinant lemma gives `det(P)=1+φ(d)=-1`, so `P` is unimodular over `Z`, invertible over `Q`, and invertible modulo 2. Since `d≠0` and `φ≠0`, `P-I=dφ` has rank one over `Q` and rank one over `F_2`. It sends `u_a` to `u_b` and `u_b` to `u_a`.

Modulo 2, `d=u_a+u_b`, `φ(x)=x_i+x_j`, `φ(u_a)=φ(u_b)=1`, and `φ(d)=0`. Thus the same exchange and involution hold in characteristic two; the determinant −1 becomes +1.

## Dual target frame

The dual action is the inverse transpose, not `P`:

\[
P^{-T}=(P^{-1})^T=P^T,
\qquad P^{-T}(U_a^\perp)=U_b^\perp,
\qquad P^{-T}(U_b^\perp)=U_a^\perp.
\]

For \(\lambda\in U_a^\perp\),
\[
(P^{-T}\lambda)^T u_b=\lambda^T P^{-1}u_b=\lambda^T u_a=0.
\]
Invertibility preserves the hyperplane dimension, giving equality. This holds over \(\mathbb Z\), \(\mathbb Q\), and \(\mathbb F_2\) (with annihilator modules/subspaces in the respective rings).

The transpose matters in this fixture. The basis vector `e_(1,2,4)` lies in `U_a^⊥` but not `U_b^⊥`; `P` fixes it, while `P^{-T}` sends it into `U_b^⊥`. The checker verifies this witness and maps a 63-vector basis of each annihilator. Its gate control keeps pair values independent; identifying the two pairs fails.

## What the rank does and does not measure

This is exact label-space algebra. It does not make `P-I` one paid Section 4 edge or define the array operator needed at a multiplication gate.

The pinned manuscript uses different physical frame objects on the two sides:

- Its complex labels are subspaces of `F_2^m`, but the frame `C_U` acts on arrays indexed by `Ω=F_2^m`, which have `2^m` entries. A physical transition is `C_V C_U^{-1}`, not the `m×m` label matrix `P`. For this fixture, `U_a⊥U_b` over `F_2`; the Section 3 transition between their complex frames factors through `U_a⊕U_b` and uses two residual-vector kernels in each direction.
- Its bit frame matrices use the rational form `I-J/9` on each factor. Here the tensor-frame inner products are `⟨u_a,u_a⟩=8`, `⟨u_b,u_b⟩=8`, and `⟨u_a,u_b⟩=4`. The old source projectors `Π_Ua,Π_Ub` differ by rank two over `Q`, as do the dual sink projectors. Thus an entry and return between these old frames costs rank two each way in that interface. This is not the rank-one matrix `P-I`.

The exact check is in [check_adapter.py](check_adapter.py); its receipt is [receipt.json](receipt.json). The gate arithmetic in the checker is an abstract 64-coordinate frame model. It verifies adapter/inverse and dual-frame algebra with independent values, while explicitly leaving the lift to the manuscript's `2^m`-entry arrays unproved.

## Scope relative to [Issue 37 checkpoint](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/03c030320085b211d9b5f2c5d94715db4547136b)

The previous direct assignment failed because distinct multiplication indices have distinct source lines; identifying the indices aliases independent bank values. `P` repairs the equality of the two **labels** in this fixture. It does not supply the physical edge, the full all-role endpoint equation, or the array decoder that the previous result lacked.
