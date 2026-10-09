# Scaling gate

## Status

**NO_SOURCE_TYPED_BRIDGE.** The checkpoint stops before \(t=2\) multiplication construction. The WHT network has an exact \(t=2\) bridge in its own model, but its two independent bank pairs cannot be mapped directly to the original multiplication data roles while preserving the equal twin source frames.

## Scoped obstruction

For \(h=100\), the original source pair index is \(a\in\mathcal T^3\), with frame line \(\langle t_{a_1}\otimes t_{a_2}\otimes t_{a_3}\rangle\). Distinct indices give distinct lines. A direct WHT twin map to indices \(a,b\) must have equal \(X\)-source frames, hence \(a=b\). That aliases the two independent WHT pairs and makes the inter-pair gates ill-typed on the original source roles. This is an obstruction to the direct role-preserving map only; it is not an impossibility theorem for a newly designed multiplication supplier with additional data roles or source-copy steps.

## No \(t=3\) claim

No \(t=3\) fixture, invocation-count formula, or general \(S_t\) construction is proposed. Phase 0's hard stop forbids treating an untyped WHT pair label as an original triple-data index. In particular, no \(2t+1\) invocation rule is inferred from the two-pair case.

The abstract signed target

\[
S_t((X_i,Y_i)_{i=1}^t,z)=((-Y_i,X_i)_{i=1}^t,z)
\]

is only a specification to be met by a future source-typed construction. It is not the original Section 3 theorem, whose data index, scratch ownership, role permutation, and bit-array endpoints are specified separately.

## Theorem needed to resume

First prove a two-pair typed embedding or a replacement full-array interface. For general \(t\), that proof must supply all of the following as one parameterized statement:

1. A class/incidence map onto the complete \(\mathcal T_h^3\) data set, with \(t\) independent pairs per class and an explicit decoder. Every original data index and output role must be covered exactly as stated; no aliases or omitted triples are allowed.
2. A stage chronology with one common frame at every cross-pair gate, explicit source/target ownership, and exact equality of each stage's outgoing and next stage's incoming data frames.
3. The complete scalar action over the signed ring, a separate complete \(\mathbb F_2\) action, and restoration of all arbitrary initial side, center, helper, and spectator values.
4. A full-array Section 4 endpoint proof and a uniform cost formula \(W_t,m_t,s_t\), including recursive child ranks, data movement, copied centers, auxiliary births, bank packing, and decoder work.
5. A falsifiable paid-lever lemma: some data, copied-center, or residual/dirty child family changes with \(t\), and the corresponding saving survives all compensation as \(t\) grows. A stage-count reduction alone does not satisfy this condition.

Only after the \(t=2\) statement exists should one check a \(t=3\) instance and attempt a general scaling claim. No recurrence or \(\kappa\) value can be imported from the WHT proof by analogy.
