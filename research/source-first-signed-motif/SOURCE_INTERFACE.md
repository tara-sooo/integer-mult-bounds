# Pinned source interface

Primary state: **KNOWN source triples; no typed five-port multiplication interface found in the frozen sources.** The bounded work stops at MULTIPLICATION_PORT_TYPE_MISSING, as requested by [Issue 30](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/30).

Pins read for this FAST pass are [Issue 29's committed result](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/69e77d2d32b06b9f5b7e2d27d5946535d4d6f4f5), the [original manuscript commit](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a), [PR 130's commit](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/6a9970a530119174507904e23592fd59ede19a5d), and [PR 144's commit](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/c8b22bc5c10dba497ac25804e27d9647d818e2ff). The issue text gives the manuscript SHA as a 39-character prefix; the repository's frozen manifest and the commit API resolve it to the 40-character SHA linked above.

## The source values and their types

In manuscript Section 3, \(\mathcal T=\binom{[h]}{3}\) is the set of **three-element** subsets of \([h]\). The two data banks are \(X_a,Y_a\), indexed by \(a=(a_1,a_2,a_3)\in\mathcal T^3\). In one invocation, the other two coordinates are fixed and the varying coordinates \(T,S\in\mathcal T\) index the logical source and target values \(x_T,y_S\). The scratch and center wires are part of the typed scalar network; they are not extra data ports.

The source's side path and center path have different maps:

\[
\mathcal V:\text{source values}\to\text{side copies},\quad
\mathcal J:\text{side copies}\to\text{target values},\qquad
\mathcal G:\text{source values}\to\text{center values},\quad
\mathcal R:\text{center values}\to\text{target values}.
\]

For the exact triple-overlap rules in the manuscript, they obey
\[
\mathcal J\mathcal V+\mathcal R\mathcal G=I.
\]
This is the identity that makes one invocation add the source vector to the target vector. The three invocations then use \(Y\gets Y+X\), the inverse \(X\gets X-Y\), and \(Y\gets Y+X\), giving \((X,Y)\mapsto(-Y,X)\) while restoring arbitrary initial scratch values. The bit instance uses \(\mathbb F_2\) scalars; the complex instance uses \(\mathbb Z[i,1/2]\). Their side supports and coefficients are defined for triples and their intersection sizes.

## PR 144's three-pair geometry

For \(p=4,h=8\), PR 144 has four choices of three pair labels and eight selectors per choice: \(8\binom43=32\) ports. Each address is an indicator selecting one coordinate from each of three distinct coordinate pairs, so every address has weight three and self-pairing one. This is the positive control checked in [the exact receipt](receipt.json).

On these ports PR 144 defines
\[
B_{T,S}=(|T\cap S|-1)/2,\quad
B_{\rm block}=\bigoplus_{\text{three-pair cubes}} B|_{\rm cube},\quad
K=I-B_{\rm block},\quad H=B_{\rm block}-B.
\]
Thus \(K+H+B=I\), \(K^2=I\), and every nonzero \(K\) or \(H\) coefficient joins binary-orthogonal addresses. Within each eight-port cube, \(K=(P-A)/2\), with \(P\) the antipodal permutation and \(A\) distance-one adjacency. The copied center is the coordinate-star map \(S_i=\sum_{S\ni i}x_S\), followed by
\[
(Bx)_T=\frac12\sum_{i\in T}S_i-\frac16\sum_iS_i.
\]
The coefficient \(1/6\) and the source-star identity use the fact that each source port has exactly three selected coordinates. These formulas do not specify a five-selected-pair producer.

PR 144's signed dirty decoder is a separate typed contract. With source \(x\), arbitrary dirty carrier \(z\), target \(y\), source injection \(V\), carrier word \(M\), and decoder \(J\), its identity is
\[
JMV=I:\text{ source values}\to\text{ target values}.
\]
The signed sequence \(y\gets y-JMz,\ z\gets z+Vx,\ z\gets Mz,\ y\gets y+Jz,\ z\gets M^{-1}z,\ z\gets z-Vx\) restores every initial \(z\) and adds \(JMVx\) to \(y\). This is not the manuscript's \(\mathcal J\mathcal V+\mathcal R\mathcal G=I\): the former decodes a transformed carrier; the latter sums a side-copy path and a center path. [PR 144's construction note and graph source](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/c8b22bc5c10dba497ac25804e27d9647d818e2ff) define the three-pair graph and its actual roles.

## Frames, stages, and the bit supplier

The manuscript's array representation assigns one common linear frame to every incidence of a gate. Its endpoint action depends on the source frame, sink frame, and signed role permutation, not only on a scalar matrix identity. The manuscript's own parameter is \(m=h^3\). The complex phase frames use binary subspace labels and Gaussian-dyadic kernels; binary orthogonality is a support condition, while coefficients remain in \(\mathbb Z[i,1/2]\).

PR 130's three-stage cover is another, conditional layer over its triple word. It uses \(E=A\perp B\perp C\), with dimensions \(h,h-1,h-1\), so the local active space has \(m=3h-2\). A typed triple port \((g,S)\) visits \(gR_{12,S},g,gR_{23,S}\); the middle word reverses and complements the source/target roles and signs. PR 144's later sharing construction embeds a \(3h-2\) data cover in an ambient \(m=3h\) space and routes through three orthogonal \(h\)-blocks. These values describe their own triple-port covers; none assigns an \(m\), group, role count, or endpoint frame to this candidate.

The bit supplier is separately typed. PR 130's bit note uses a retained triple word at \(h=23\), a rational space \(\mathbb Q^{23}\), and \(H_0=(I-J/9)/2\), with \(q_S^{\mathsf T}H_0q_S=1\) for triple indicators. It is not the complex dyadic graph reduced modulo two. The five-pair motif has no map to these rational bit roles or frames.

Pinned manuscript Section 4 (`build/sections/04-swap.tex` at the [original manuscript commit](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a)) states the full-array Swap theorem. For an array laid out as \([P]\times[2^u]\times[G]\times[2^u]\times[B]\), it interchanges the two \([2^u]\) coordinates by \((p,h,g,d,z)\mapsto(p,d,g,h,z)\), in time \(O(Vu^\tau)\) for \(V=PGB2^{2u}\); \(B=1\) is allowed. The stated work includes shape processing, padding and unpadding, and fixed-tape workspace cleanup.

Its prerequisites are a finite bit circuit with \(W\) roles, including scratch roles; common rational gate and terminal frames \(M_v\); a signed role permutation \(\rho\); and, for every role \(w\), the endpoint equation \(M_{\rm out(\rho(w))}-M_{\rm in(w)}=I_m\). For its edge set, \(s=\sum_e\operatorname{rank}_{\mathbb Q}(M_{\rm head(e)}-M_{\rm tail(e)})<Wm\), and the role-row splitting with fixed-tape cleanup gives \(F_0=O(1)\), \(F_k\le(s/W)F_{k-1}+O(1)\). These are the pinned Section 4 hypotheses and recurrence; the candidate \(K_*\) supplies none of them.

## The missing source theorem

The proposed \(T_\epsilon\) selects one coordinate from **all five** pairs and has weight five. The frozen source input type is a three-element subset, and neither the manuscript nor PR 130/144 defines a five-element port as a multiplication input/output value, an encoding into the \(\mathcal T^3\) data banks, or a typed \(V,J,M\) decoder for it. Equal cardinality with PR 144's \(p=4\) control (32 ports) does not define such a map. PR 144's full \(p=5\) family has \(8\binom53=80\) three-pair ports; those certificates and costs are not used here.

The smallest missing result is a new outer reduction theorem defining actual source and target value spaces and proving a non-tautological decoder on those values. Depending on its construction, it must prove the correctly typed \(JMV=I\) carrier identity or a correctly typed \(\mathcal J\mathcal V+\mathcal R\mathcal G=I\) side-plus-center identity, together with legal supports and the multiplication interchange. It must also state how its values meet the separate bit, frame, endpoint, and recursion contracts before any cost claim follows. This is a gap in the pinned source interface, not a no-go theorem for other reductions.
