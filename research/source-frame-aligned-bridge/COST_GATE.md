# Cost gate

## Existing production bit budget

For the pinned source geometry at $h=100$, $v=\binom{100}{3}=161{,}700$, $N=v^3=4{,}227{,}952{,}113{,}000{,}000$, and $m=1{,}000{,}000$. The Section 3/4 bit supplier has

\[
W=177{,}176{,}569{,}091{,}445{,}000{,}000,
\quad s=177{,}176{,}569{,}088{,}785{,}861{,}287{,}000{,}000,
\quad D=mW-s=2{,}659{,}138{,}713{,}000{,}000.
\]

Pair the third-coordinate triples for each fixed first and second coordinate. Since $v$ is even, this gives $N/2$ classes.

## Adapter rank screen

The issue's deliberately optimistic screen charges two rank-one transitions per class (one entry and one return), leaves $(W,m)$ fixed, and assumes no sharing. The added rank mass is then $N$, giving

\[
D'_{\mathrm{rank1}}=D-N=-1{,}568{,}813{,}400{,}000{,}000.
\]

Thus even this optimistic screen fails the strict Section 4 condition $s'<Wm$ unless old charges save more than $N-D=1{,}568{,}813{,}400{,}000{,}000$. Improving the original deficit (D) requires savings greater than $N$.

For the existing Section 3 bit frames on the $h=4$ fixture, the direct source-projector and dual-sink-projector differences have rank two over \(\mathbb Q\). A direct common-frame hop on one role and its return cost at least two rank units each way by the Section 4 edge rule. If that unchanged-frame adapter is used for every class, the diagnostic addition is $2N$, and

\[
D'_{\mathrm{old\ frames}}=D-2N=-5{,}796{,}765{,}513{,}000{,}000.
\]

This is an endpoint-rank screen, not a full new circuit recurrence. It assumes unchanged $(W,m)$, no sharing, and one adapted target role per class. If adapters need helper roles, a different stock $(W')$, ambient width $m'$, and the full role endpoint ledger must be derived before any moment $M'(a)$ is meaningful. None is derived here because the five-stage word has no all-role multiplication embedding.

Under the same unchanged-stock assumption, offsetting this rank-two screen requires old-charge savings greater than $2N-D=5{,}796{,}765{,}513{,}000{,}000$ just to restore a positive deficit, and greater than $2N=8{,}455{,}904{,}226{,}000{,}000$ to improve the old deficit.

## Complex and bit costs stay separate

- **Complex:** for the $h=4$ local fixture, the actual Section 3 phase-frame change between the dual target hyperplanes uses two residual-vector kernels in each direction. The local Gate C round trip therefore uses four such factors. The corresponding source-line transition also uses two factors in each direction. These are complex array operations; they do not reduce to bit children.
- **Bit:** $P\bmod2$ is an involution on labels, but the multiplier's Section 4 operation needs a separate \(\mathbb F_2\) gate network, the rational all-role endpoint equation, and its charged edge-rank sum. The local XOR gate does not provide that supplier. In the unchanged Section 3 rational frame assignment, the one-role entry/return screen above is rank two per direction.


## Full adapter ledger before a recurrence can be claimed

| Required path per paired class | Complex frame work | Existing bit-frame rank | Evidence/status |
| --- | --- | --- | --- |
| Align and restore the dual target role around Gate C | two residual-vector kernels in, two out | rank two in, rank two out | exact local typed identity; not induced by label-space $P$ |
| Align and restore the source line for a full bridge | two residual-vector kernels in, two out | rank two in, rank two out | Section 3 frame change identified; no all-stage role proof |
| Copies, auxiliary roles, Section 6 decoder, original dirty scratch | not counted | not counted | no owner map or endpoint circuit; WHT helper preservation alone does not supply it |

If both known frame paths are required independently, the finite fixture therefore has eight complex residual-kernel factors or eight existing-frame bit rank units per class before copies, helper roles, decoder, or scratch restoration. Across the $N/2$ classes, that is $4N$ factors or rank units respectively; these are different cost models and must not be combined. For the bit supplier, this known two-path screen changes $D$ to

\[
D-4N=-14{,}252{,}669{,}739{,}000{,}000.
\]

The less expensive one-target-role screen above already fails. The $4N$ figure is the best available unchanged-stock ledger for both source and dual roles, not a paid new recurrence: copies, auxiliary-role stock, recorded-order decoding, and arbitrary-dirty scratch restoration have no proved mapping or charge. A full recurrence cannot be stated until those endpoints are constructed.

[PR 209](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/209)'s five invocations versus six and its WHT saving belong to its exact-complex RAM layout. No complete original multiplication child is shown deleted, so the matched multiplication saving $E$ is zero in this checkpoint. Extra copies, a new role stock, shared adapters, full-array decoding, and the original arbitrary-dirty scratch mapping remain unconstructed or unpriced. A stage-count difference alone supplies no offset to the rank screen.

## Early stop

For the unshared per-class adapters with the existing role stock, the optimistic rank-one bound already makes $D'<0$; the original bit frames charge more. No same-output, same-machine old child saving has been established. Stop with `ADAPTER_OVERHEAD_ERASES_GAIN` for this proposed adapter route. This does not rule out a different encoding with proved sharing or a changed recursion/role stock.
