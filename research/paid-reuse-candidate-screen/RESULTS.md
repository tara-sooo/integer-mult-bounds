# Results

**FAST: PASS. FOCUSED: PASS. The best local carry saves five XORs but adds two roles. No overall recurrence-cost improvement is established.** The scan covers the frozen PR 63 h=23 circuit and distinguishes repeated graph operands from separately charged compiler demands.

Value 62985 is the strongest measured candidate. Forcing its two legal carry edges changes the full word from 149,172 to 149,167 physical XORs, while increasing roles from 27,918 to 27,920 and event-plus-endpoint rank mass from 642,620 to 642,666. The full rank histogram changes as recorded in `COSTS.md`. Since the role/rank side worsens and the complete child cost is not computed, the five-XOR reduction is a tradeoff, not a proven net bound improvement.

Value 21 has the largest baseline copy count among the focused copy-heavy family—nine XORs across twelve demands—but no eligible other-role span hit at any demand. Value 62985 has a span hit at all six demands, but none can be expressed by one, two, or three currently eligible retired roles. This does not support another PR 74-style reconstruction pass in the fixed schedule.

The local search stops here. The next investigation should move to typed recurrence interfaces or the outer multiplication construction rather than keep scanning similar one-carrier exchanges.

## Evidence boundaries

- The frozen baseline word is reproduced byte-for-byte. Each forced alternative has its own complete word hash.
- The all-demand form screen covers 15,102 values and 79,075 physical demand points. It finds 1,080 span hits across 786 values. A hit does not establish arbitrary-dirty reconstruction or a paid schedule.
- The full h=23 rank histogram includes frame raises and output/retirement endpoints. Physical XOR count, role count, and rational-rank profile are reported separately.
- Local block M/inverse checks pass for the touched dirty role basis vectors. A full global dirty-basis replay was not run.
- The complete child histogram and recurrence moment were not recomputed. No κ improvement, Section 4 call identity, or cross-child sharing is established.
- PR 74's h=25 deferred reconstruction is a method comparator only; its costs are not transferred to h=23.
