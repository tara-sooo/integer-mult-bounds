# Typed formula and scope

## Domains

For an integer h ≥ 3, let U_h = {1, …, 2^h−2}, the nonempty, nonfull masks. The pinned zeta operator is

\[
D_h[t,u]=[t\mathbin{\&}u=0],\qquad D_h:A^{U_h}\to A^{U_h}.
\]

For triple-mask encoding into U_h, require h≥4 so every triple mask is nonempty and nonfull. The first legal paired-cube case is h=8 and p=4. Partition [8] into the four pairs {1,2}, {3,4}, {5,6}, {7,8}. The 32 ports P_4 choose one coordinate from each of three distinct pairs. Encode a triple by its characteristic mask m(S)=∑_{i∈S}2^{i−1}, which lies in U_8.

The candidate input map E:A^{P_4}→A^{U_8} places each x_S at m(S) and has zero data contribution at every other mask. Selecting the singleton row gives

\[
Z_i=(D_8Ex)_{\{i\}}=\sum_{\substack{S\in P_4\\i\notin S}}x_S,\qquad
S_i=\sum_{\substack{S\in P_4\\i\in S}}x_S,\qquad
X=\sum_{S\in P_4}x_S.
\]

The total is the separate map X:A^{P_4}→A with X(x)=∑_{S∈P_4}x_S. Let R_1:A^{U_8}→A^8 select the eight singleton rows, (R_1y)_i=y_{\{i\}}. PR172 omits the empty-mask target that would sum all input masks.

## Exact signed identity

Let \(\mathcal T_h=\binom{[h]}3\), with h≥4 for the mask embedding. Extend E to all of \(\mathcal T_h\) by the same characteristic-mask rule. The proof below holds on \(\mathcal T_h\); restricting its rows and columns to P_4 gives the requested 32-port operator.

Define C_B:A×A^8→A^{P_4} by [C_B(a,z)]_T=a−(1/2)∑_{i∈T}z_i. For a basis input e_S, X=1 and each Z_i is 1 exactly when i∉S. Therefore, for every T,S∈\(\mathcal T_h\),

\[
\begin{aligned}
[C_B\circ(X,R_1D_hE)]_{T,S}
 &=1-\frac12\sum_{i\in T}[i\notin S]\\
 &=1-\frac12(3-|T\cap S|)\\
 &=\frac{|T\cap S|-1}{2}=B_{T,S}.
\end{aligned}
\]

Equivalently, on arbitrary x, Z_i=X−S_i. The exact checker compares every coefficient in the h=4 triple matrix and every coefficient in the P_4, h=8 matrix.

## Coefficient rings

E, D_h, X, and the singleton sums use integer coefficients. B and C_B use only 1/2, so the displayed map is defined over \(\mathbb Q\) and the complex dyadic ring \(\mathbb Z[i,1/2]\).

For every triple-port family of size h,

\[
\sum_{i=1}^{h}Z_i=(h-3)X.
\]

At h=8 this is \(\sum_i Z_i=5X\). Division by 5 is valid over \(\mathbb Q\), but 1/5 is not in \(\mathbb Z[i,1/2]\), and it is not invertible modulo 5. In a q-adic ring, the quotient needs q∤(h−3) and an explicit denominator/prime contract. At h=24, h−3=21 has prime factors 3 and 7.

The coefficient 1/2 cannot be reduced in \(\mathbb F_2\). A bit supplier needs its own operator, decoder, and H_0-compatible physical support.

## Scope of the source identities

On P_4, the PR144 scalar identity is K+H+B=I, with K=I−B_block, H=B_block−B, and K²=I. Since B_z=B as a matrix, K+H+B_z=I remains an abstract algebra identity. This candidate supplies only B; it does not implement its physical broadcaster or the K and H schedules.

The original Sections 3–4 also require the separate bit and complex suppliers and their typed source/target interfaces. The factorization does not establish the full JV+RG=I construction or the PR130 three-stage endpoint-frame condition.
