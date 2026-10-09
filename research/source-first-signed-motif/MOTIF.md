# Five-pair local motif

Status: **KNOWN local algebra; no multiplication claim.** This is the proposed five-pair geometry in [Issue 30](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/30), checked exactly by [check_small.py](check_small.py). The source distinction is documented in [SOURCE_INTERFACE.md](SOURCE_INTERFACE.md).

## Addresses and binary cap

For \(\epsilon\in\mathbb F_2^5\), define
\[
T_\epsilon=\{2j+\epsilon_j:0\le j<5\},\qquad
q_\epsilon=\chi_{T_\epsilon}\in\mathbb F_2^{10}.
\]
There are 32 distinct addresses. Every \(q_\epsilon\) has weight five and
\[
q_\epsilon\cdot q_\delta
=|T_\epsilon\cap T_\delta|
=5-d_H(\epsilon,\delta)\pmod 2.
\]
Thus each diagonal entry of the 32-by-32 Gram/cap matrix is one, and an entry between opposite selector parities is zero. There are 16 selectors of each parity. This is a necessary local cap condition for the proposed cross-parity operator.

Let \(x,y\in\mathbb F_2^4\). Complete each four-bit selector to an even or odd five-bit selector by choosing its last bit so the total parity has the requested value. On the even and odd sectors, set
\[
A_{x,y}=\frac{(-1)^{x\cdot y}}4,\qquad
K_*=\begin{pmatrix}0&A\\A^{\mathsf T}&0\end{pmatrix}.
\]
The standard Walsh character sum gives \(AA^{\mathsf T}=I_{16}\) over exact rationals, hence \(K_*^2=I_{32}\). All 512 directed nonzero entries join opposite-parity selectors, so all 512 pass the binary cap. Each coefficient is \(+1/4\) or \(-1/4\), in the formal ring \(\mathbb Z[i,1/2]\).

The receipt includes all Gram rows as 32-bit hexadecimal words (least significant bit is column zero), all port masks, all 16 Walsh sign rows, exact matrix digests, and the coefficient counts. The Walsh identity and \(K_*^2=I\) are computed with Fraction arithmetic; the binary cap and span are computed over \(\mathbb F_2\).

## Distinction from the PR 144 positive control

The [PR 144 source](https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/c8b22bc5c10dba497ac25804e27d9647d818e2ff) chooses three of \(p\) coordinate pairs, then one coordinate from each chosen pair. At \(p=4,h=8\), that gives four eight-port cubes and 32 weight-three ports. The exact positive-control matrices have 128 \(K\), 384 \(H\), and 544 \(B\) nonzeros; \(K^2=I\), \(K+H+B=I\), and every \(K/H\) support pair is binary-orthogonal. These checks reproduce the Issue 29 receipt pinned at [its commit](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/69e77d2d32b06b9f5b7e2d27d5946535d4d6f4f5).

The candidate instead uses all five pairs for every port. Its port vectors span rank six in \(\mathbb F_2^{10}\); the PR 144 \(p=4,h=8\) control spans rank eight. Its port weight is five rather than three. Both are invariant under a permutation of port indices, so an index relabeling cannot turn this family into the source's triple-port address family. PR 144's full \(p=5\) triple-pair family has \(8\binom53=80\) ports, not this 32-port set. No p=5 certificate or cost is imported.

The exact check establishes only the proposed binary Gram matrix and formal involution. It supplies no \(B_*\), \(H_*\), side roots, center, data meanings, physical Walsh word, bit network, source/target frame, or multiplication decoder.
