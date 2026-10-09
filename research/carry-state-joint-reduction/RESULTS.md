# Results: ordinary block multiplication, no new saving

**Outcome:** `KNOWN_EQUIVALENCE_ONLY` plus a scoped residual-width theorem.

## Proved

- For every even power-of-two input width \(n=2m\), four exact
  \(m\)-bit child products recover adjacent windows by
  \[
  AB=L+2^mH,
  \quad L=p_{00}\bmod2^m,
  \quad H=\lfloor p_{00}/2^m\rfloor+p_{01}+p_{10}+2^mp_{11}.
  \]
  This follows by expanding the two block decompositions. Each child is a
  strictly smaller fully specified multiplication.
- In the stated interface where the upper computation sees only upper
  operand blocks and a carry state, but cannot reread or recompute the low
  operands, an exact state at a cut of \(k\ge2\) bits needs at least \(k\)
  bits. The quotient \(\lfloor A_0B_0/2^k\rfloor\) has at least
  \(2^k-1\) possible values even with both upper blocks zero.
- The recurrence for this candidate is \(J(n)=4J(n/2)+O(n)\), hence
  \(\Theta(n^2)\) with one-bit leaves. This is the conventional two-block
  schoolbook recurrence; the shared child result is ordinary full-product
  reuse, not a new reduction.

## Checked exactly

`check_pilot.py` exhaustively checks all 256 four-bit input pairs and all
16 two-bit child products with exact Python integers. For every top-level
pair it checks the low window, high window, full padded product, child
widths, and carry state. It also checks and rejects three adverse controls:
an omitted cross product, a decremented carry, and a dirty output buffer.
The residual-state examples realize all three required values `0, 1, 2`
for the two-bit pilot, ruling out a one-bit state there.

## Not established

- No saving over the best combination of separately computed truncated or
  middle products; no lower bound on that unrestricted comparison.
- No result against growing, nonlinear states that can access additional
  low-side data, or child types other than the four full subproducts.
- No general lower bound for integer multiplication, no transfer to the
  manuscript's address-interchange recurrence, and no positive or improved
  \(\kappa\).
- The checker verifies finite semantics, not a physical Turing-machine
  implementation. The asymptotic tape ledger is for the explicit
  depth-first schedule in COST.md. No independent mathematical review was
  performed.

## Next mathematical question

Any useful successor must share a recursive operation across adjacent
windows without making one window recompute the other or treating a full
child as free. The next lemma should give an explicit child type and prove
that its combined low/high recursion uses fewer paid children than the
best separate truncated-window recurrences, including state width,
input access, copies, cleanup, and fixed-tape movement. If that inequality
cannot hold for a specified family, prove the scoped child-count
obstruction for that family. The constant-width carry-state route is
already ruled out above.

## Reproduction and attribution

Run `python3 research/carry-state-joint-reduction/check_pilot.py` from the
repository root. The deterministic output is recorded in `receipt.json`.
This folder and checker were prepared with substantial OpenAI Codex
assistance. The cited manuscript remains attributed to OpenAI; no
upstream source code or certificate was copied.
