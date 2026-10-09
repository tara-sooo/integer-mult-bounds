# Exact fibre label theorem

## Definition

Let \(h\) be even, \(\mathcal T_h={ [h] \choose 3 }\), \(m=h^3\), and
\(u_{A,B,T}=t_A\otimes t_B\otimes t_T\in\mathbb Z^m\). Pair
\(p_i=2i-1,q_i=2i\), and let \(\tau\) transpose every pair. For fixed
\(A,B\in\mathcal T_h\), choose \(\alpha\in A\) and \(\beta\in B\), and set

\[
d_i=t_A\otimes t_B\otimes(e_{q_i}-e_{p_i}),\qquad
\phi_i(x)=x_{(\alpha,\beta,p_i)}-x_{(\alpha,\beta,q_i)},\qquad
P_{AB}=I+\sum_{i=1}^{h/2}d_i\phi_i.
\]

The finite checker uses \(A=\{1,2,3\}\), \(B=\{1,2,4\}\), and
\(\alpha=\beta=1\) at \(h=4,6\). The proof below works for every fixed
\(A,B\) and every such \(\alpha,\beta\).

## Proof

The vectors \(d_i\) have disjoint third-coordinate supports, and the
\(\phi_i\) have disjoint coordinate supports. Direct evaluation gives
\[
\phi_i(d_j)=-2\delta_{ij},\qquad
\phi_i(u_{A,B,T})={\bf1}_{p_i\in T}-{\bf1}_{q_i\in T}.
\]
Thus, with \(D\) having columns \(d_i\) and \(\Phi\) having rows \(\phi_i\),
\[
P_{AB}=I+D\Phi,\quad \Phi D=-2I,\quad
P_{AB}^2=I+2D\Phi+D(\Phi D)\Phi=I.
\]

For a fixed pair \(\{p_i,q_i\}\), the contribution to \(D\Phi u_T\)
is zero if \(T\) contains both or neither, and otherwise changes the
selected basis vector from \(p_i\) to \(q_i\) or back. Hence
\[
P_{AB}u_{A,B,T}=u_{A,B,\tau(T)}
\]
for every \(T\in\mathcal T_h\). A triple fixed by \(\tau\) would be a
union of two-element pair orbits, so \(\tau\) has no fixed triple.

The \(h/2\) by \(h/2\) minors of \(D\) at coordinates
\((\alpha,\beta,q_i)\), and of \(\Phi\) at coordinates
\((\alpha,\beta,p_i)\), are both identity matrices. Therefore \(D\) has
full column rank and \(\Phi\) full row rank over \(\mathbb Z\),
\(\mathbb Q\), and \(\mathbb F_2\). The unit minors make \(D\) injective
and \(\Phi\) surjective, so
\(\operatorname{rank}(D\Phi)=h/2\) over \(\mathbb Q,\mathbb F_2\)
(and its image has \(\mathbb Z\)-rank \(h/2\)). Therefore
\(\operatorname{rank}(P_{AB}-I)=h/2\) over \(\mathbb Q\) and
\(\mathbb F_2\). The determinant lemma gives
\(\det P_{AB}=\det(I+\Phi D)=(-1)^{h/2}\). In particular it is
unimodular over \(\mathbb Z\) and invertible after reduction modulo two.

Since \(P_{AB}^{-1}=P_{AB}\), the correct dual map is
\(P_{AB}^{-T}=P_{AB}^{T}\), not generally \(P_{AB}\). If
\(\lambda^Tu_{A,B,T}=0\), then
\[
 (P_{AB}^{-T}\lambda)^Tu_{A,B,\tau(T)}
 =\lambda^TP_{AB}^{-1}u_{A,B,\tau(T)}
 =\lambda^Tu_{A,B,T}=0.
\]
Invertibility and equal hyperplane dimensions give equality of the
annihilators. The checker transports a complete integral basis of each
annihilator and reduces it modulo two.

## Exact finite checks

The checker, check_fibre.py, checks every third triple at \(h=4,6\),
the involution on every ambient basis vector, the dual action on every
annihilator basis vector, and exact unit minors certifying rank. Results:

| \(h\) | \(m\) | \(|\mathcal T_h|\) | rank over \(\mathbb Q,\mathbb F_2\) | determinant |
|---:|---:|---:|---:|---:|
| 4 | 64 | 4 | 2 | \(+1\) |
| 6 | 216 | 20 | 3 | \(-1\) |

The wrong-sign control \(I-D\Phi\) fails on each selected \(u_T\) over
\(\mathbb Z/\mathbb Q\). For the wrong-dual control at \(h=6\), take
\(T=\{1,2,3\}\) and covector \(e_{(1,1,4)}\). It annihilates
\(u_{A,B,T}\), but applying \(P_{AB}\) gives pairing \(-8\ne0\) over
\(\mathbb Z/\mathbb Q\) with
\(u_{A,B,\tau(T)}\). The inverse-transpose check, including reduction
modulo two, passes. The sign control is stated over characteristic zero;
minus and plus coincide in \(\mathbb F_2\).

This proves a label-space identity. It does not identify \(P_{AB}\) with
the paper's complex array frame or with a paid Section 4 bit edge.
