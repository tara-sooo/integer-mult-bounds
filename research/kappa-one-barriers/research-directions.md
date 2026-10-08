# Independent directions after the first barrier pass

These directions are deliberately outside another slot-order sweep. Each
targets a different layer of the proof: finite producers, recursive profile,
or the outer multiplication reduction.

## 1. Lower-bound legal producer and carrier families

**Tractability:** highest of these three. **Conceptual leverage:** medium to
high; a result could explain whether the current role-deficit improvements can
scale or have a precise family ceiling.

**Hypothesis.** With the current leave-two-out outputs, original core/cover
envelopes, and paid-copy rules fixed, every legal producer/carrier graph has a
child moment bounded below by a positive function that keeps `a_b` far below
one. The current identity `s = mW − N + L` and fixed `N−L` are evidence only
inside the recorded constructions; they are not yet a lower bound over every
legal graph. [S6, S7, S8]

**Proof obligation.** Optimize the complete weighted child objective
`Σ_t n_t t (m/t)^a` subject to all support, chronology, frame-containment,
distinct-use, and paid-clearing constraints. A valid no-go must cover every
graph in the declared family, not just the stored matching or observed role
count.

**Tiny first test.** Extend the exact small-strip/assembly enumeration already
described in the pinned pair-assembly proof to enumerate all legal core/cover
continuations on a toy instance, and minimize the weighted moment rather than
only unmatched additions. First check whether the known `k ≤ 8` strip and
nine-piece assembly optima agree with that objective. If not, the proposed
relaxation is too weak before scaling it to the full graph. [S7]

## 2. Multi-type, nonuniform recursion

**Tractability:** medium. **Conceptual leverage:** high; a new recurrence may
avoid the ceiling of a single fixed `m` and one child histogram.

**Hypothesis.** A finite collection of different recursive networks, applied
according to the current profile type or depth, can have a smaller effective
growth rate than any one network's scalar moment test. This would require a
matrix or operator-valued potential, not substituting a different scalar `m`
at each level without accounting for interfaces.

**Proof obligation.** Give a multi-type recurrence whose state includes the
full bit/complex profile and tape-layout state; prove a spectral-radius or
Lyapunov contraction with a strict rational gap; then show that conversions
between types preserve arbitrary dirty scratch and fixed-tape storage. The
result must compose with exact recovery and the analytic reduction. The
current PR #63 bit and inherited complex profiles provide a concrete starting
pair of types. [S4, S8]

**Tiny first test.** Form a two-type toy recurrence from two already pinned
child profiles and compute its spectral-radius bounds with rational interval
arithmetic. Compare that bound to the best scalar moment for the same combined
profile. If no strict improvement survives the type-conversion costs, this
specific multi-type route is falsified before building a new producer.

## 3. Replace a stage of the outer multiplication reduction

**Tractability:** lowest. **Conceptual leverage:** highest; this is the route
most likely to remove a bottleneck shared by all current finite witnesses.

**Hypothesis.** A different transform/layout or convolution reduction can
lower or remove the costs currently budgeted through Gaussian resampling,
prime-axis setup, bulk tape routing, and exact recovery. Improving only the
finite bit network cannot remove those inherited obligations.

**Proof obligation.** Supply a complete fixed-finite-tape multiplication
pipeline with exact output recovery and explicit all-size error, setup,
storage, and routing bounds. Its exponent inequalities must remain strict for
the proposed saving and state which new theorem replaces each inherited
analytic or prime-selection input. [S1, S3, S4]

**Tiny first test.** Choose one concrete outer term from the pinned cost table
(for example, a Gaussian line-map or axis-routing term) and derive its lower
and upper exponent in a toy layout using exact parameter bounds. If the term
still forces exponent one under the proposed replacement, that architecture
cannot support a sublinear logarithmic factor saving without changing another
stage too. [S3]

## Attribution

These proposed directions and the first-pass synthesis were prepared with
OpenAI Codex assistance. Candidate results remain attributed to the authors
and assistance disclosures recorded in [`sources.json`](sources.json); no
inherited construction is claimed as new here. The repository's Apache-2.0
license applies to these notes, while source-specific notices remain in force.
