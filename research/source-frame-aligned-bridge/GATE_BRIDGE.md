# [PR 209](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/209) gate bridge check

## Pinned gate and its own types

The pinned [PR 209](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/209) commit is documentation-only: it adds one attribution line. The actual five-stage construction is in the separately pinned WHT Lean project. The selected gate is its final inter-pair layer, `BR.Bridge2.gateC`, in `Work/Bridge/Cert.lean`.

Its gate source map `pC` and coefficients `kCc` implement

\[
Y_1\leftarrow Y_1-Y_2,\qquad X_2\leftarrow X_2+X_1.
\]

`Bridge2.S8` assigns the same full frame to $(X_1,X_2)$, the same frame $YF(g,t)$ to $(Y_1,Y_2)$, and identity frames to its helper roles. `Bridge2.gateC` proves this layer is an `XRoute` from `S8` back to `S8`. The scalar chain records the intermediate signed values and leaves the WHT helper slots unchanged; the certificate then applies its signed role exchange. These are facts in the WHT role type and exact-complex RAM model.

## Local typed identity with original multiplication target roles

Use the fixture from [ADAPTER.md](ADAPTER.md), with independent pair data. At the chosen output gate, Section 3's original multiplication target types are

| Role | Original target frame label |
| --- | --- |
| $(X_a,X_b)$ | $\mathcal F$ |
| $Y_a$ | $U_a^\perp$ |
| $Y_b$ | $U_b^\perp$ |

At the scalar gate, let $(x_1,x_2,y_1,y_2)$ be arbitrary independent logical values. Write $D_U$ for the actual Section 3 array frame operator associated with label $U$, and set

\[
T^\vee=D_{U_b^\perp}D_{U_a^\perp}^{-1}.
\]

The fully typed pre-adapter → gate → post-adapter identity is

\[
\begin{array}{lll}
\text{before:}&Y_1=D_{U_a^\perp}y_1,&Y_2=D_{U_b^\perp}y_2,\\
\text{entry:}&Y_1\gets T^\vee Y_1=D_{U_b^\perp}y_1,&X_i=D_{\mathcal F}x_i,\\
\text{gate C:}&Y_1\gets Y_1-Y_2=D_{U_b^\perp}(y_1-y_2),&X_2\gets X_2+X_1=D_{\mathcal F}(x_2+x_1),\\
\text{exit:}&Y_1\gets (T^\vee)^{-1}Y_1=D_{U_a^\perp}(y_1-y_2).&
\end{array}
\]

Both gate operands share their frame, pair values stay independent, the WHT helpers are untouched, and the output returns to the original $Y_a$ target frame. The signs match `gateC`; changing subtraction to addition changes $y_1-y_2$ to $y_1+y_2$. In label space, $P^{-T}$ is the correct map $U_a^\perp\to U_b^\perp$. The physical $T^\vee$ above is the required lift. The algebra of $P$ alone does not prove $T^\vee$ equals an operator induced by $P^{-T}$.

The same Section 3 frame machinery can realize this **complex-side local transition**: for the fixture's orthogonal lines, the dual hyperplanes differ by removing one residual vector and adding one, so $T^\vee$ and its inverse each use two translation-kernel factors. This is a rank-two frame change in each direction, not a one-factor adapter.

On the bit side, the gate coefficients reduce locally to XORs, and the original Section 4 frame matrices for these target roles differ by rational rank two. A local in-place transition and inverse can therefore be charged as two recursive rank children each in that existing frame model. This verifies one local gate wrapper; it does not provide the separate all-role bit supplier.

## Why the multiplication bridge stops here

The local $D$-level identity is not the proposed $P$ operator. The remaining source-typed bridge would have to prove that the source retyping, all five invocation stages, and the dual output retyping are induced by these actual array operators with the original source/sink matrices. It would also need to map every class onto the complete $\mathcal T_h^3$ index set without aliasing, and map [PR 209](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/209)'s shared helper roles to the original private $(A_{ST},C_i,C_\ast)$ scratch owners.

The [PR 209](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/209) WHT proof checks its own arbitrary helper-state contract. No assignment to the original multiplication's scratch roles or dirty-state endpoints follows from that proof. The original signed complex endpoint $(X_a,Y_a,z)\mapsto(-Y_a,X_a,z)$ and the separate bit endpoint $(X_a,Y_a,z)\mapsto(Y_a,X_a,z)$, with all scratch fixed, have not been constructed from this gate layer. Section 4's all-role endpoint equation and Section 6's recorded-order inverse transform/decoder are not supplied by the WHT certificate.

## Adverse controls

- **No adapter:** $U_a\ne U_b$, so the required twin frame equality is absent.
- **Aliased data:** setting pair 2 equal to pair 1 replaces $x_1+x_2$ by $2x_1$ and loses an independent input.
- **Wrong dual:** applying $P$ instead of $P^{-T}$ fails on coordinate $(1,2,4)$.
- **Wrong sign:** `Y1 += Y2` fails for independent values; the complex output becomes $y_1+y_2$, not $y_1-y_2$.

The exact finite checker covers these controls. No full five-stage multiplication Swap is claimed.
