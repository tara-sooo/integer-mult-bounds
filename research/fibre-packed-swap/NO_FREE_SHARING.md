# Direct-sum rank obstruction

Let \(k=v/2\) be the ten independent \(\tau\)-pair contexts at \(h=6\),
and let \(Q=P_{AB}^{\oplus k}\) be the operation that applies the
proposed rank-three label transform independently in every context.
Then
\[
Q-I=(P_{AB}-I)^{\oplus k},\qquad
\operatorname{rank}(Q-I)=k\operatorname{rank}(P_{AB}-I)=10\cdot3=30.
\]
This holds over both \(\mathbb Q\) and \(\mathbb F_2\). The finite checker
certifies the rank-three factor with a unit minor; the block-diagonal
unit minor gives rank 30.

For any invertible linear packing \(E\) of these same independent
contexts, conjugation preserves rank:
\[
\operatorname{rank}(EQE^{-1}-I)
=\operatorname{rank}(E(Q-I)E^{-1})
=\operatorname{rank}(Q-I)=30.
\]
Thus a common formula, lane permutation, or other invertible coordinate
relabeling cannot turn this direct sum into a rank-three logical
operation. If an entry and a return both apply this involution, the
abstract label-rank proxy is 30 each way, 60 total.

This is a lower bound only for the same independent direct-sum action
under invertible relabeling. It does not rule out a changed typed
operation, a nonlinear code, or a new recursion with a proved decoder.
None is constructed in this checkpoint.

The rank is on the \(m\)-coordinate label operator. It is not the
rank of a Section 4 gate edge by definition, and it is not the rank of
the \(2^m\)-entry complex array frame. Those physical costs require
separate endpoint and array-operator proofs.
