# Source interface checkpoint

## Result

**NO_SOURCE_TYPED_BRIDGE.** The five-stage construction has a precise source and target in its own Walsh–Hadamard RAM proof, but no role-preserving translation to the original integer-multiplication network is available. The natural attempt to assign its two twin bank pairs to original data pairs fails at the source frames.

## Original multiplication roles and endpoints

The source is the pinned manuscript at [OpenAI/math commit adc7f1241b42e322a6451854ab7e4b4c146bf78a](https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a): [Section 3](../../upstream/build/sections/03-motifs.tex), [Section 4](../../upstream/build/sections/04-swap.tex), and [Section 6](../../upstream/build/sections/06-transforms.tex). The vendored [source manifest](../../upstream/manifest.json) records this pin and the exact hashes of the three sections read here:

| Section | SHA-256 |
| --- | --- |
| 03-motifs.tex | ed76761194988a01af77ead0ea6469cb5dcd29690ab985a0b5a4006b0f2b69bb |
| 04-swap.tex | 412b170ccaab38dba96e95e3cbfae09f4876a9818f8d278776a746b0f8044906 |
| 06-transforms.tex | 924316e4bc905066281d8f9e8746a49d8829aeb393688608deb1e61c3c87853c |

For the manuscript's production finite network, let \(h=100\), \(\mathcal T=\binom{[h]}3\), \(v=|\mathcal T|=161700\), \(N=v^3\), and \(m=h^3=1000000\). Data roles are \(X_a,Y_a\), indexed by \(a=(a_1,a_2,a_3)\in\mathcal T^3\). The bit and complex constructions are distinct scalar networks:

| Contract | Scalar ring | Data action |
| --- | --- | --- |
| bit | \(\mathbb F_2\) | exchange \(X_a,Y_a\) |
| signed complex | \(\mathbb Z[i,1/2]\) | \((X_a,Y_a)\mapsto(-Y_a,X_a)\) |

At each of three coordinate stages, the other two coordinates are fixed and the selected coordinate varies; there are \(v^2\) invocations per stage. An invocation has one ordered side role \(A_{ST}\) for each allowed neighbor pair and center roles \(C_i\); the complex version also has \(C_\ast\). The bit side uses \(|S\cap T|=1\), copies \(x_T\) to \(A_{ST}\), and cancels the intersection-one part of the center coefficient \(|S\cap T|\bmod2\). The complex side uses distinct triples with even intersection, coefficient \(-(|S\cap T|-1)/2\), and center scatter \((\sum_{i\in S}C_i-C_\ast)/2\); it cancels the intersection-zero and intersection-two contributions. Each invocation owns separate side and center scratch, distinct from every other invocation and stage. Its eight rows subtract old side and center effects, copy and gather the source, add the new scatter and side effects, then undo gather and copy. For arbitrary initial side state \(a_0\), center state \(c_0\), source \(x\), and target \(y\), the composition is \((\mathcal J\mathcal V+\mathcal R\mathcal G)x=x\): it leaves target \(y+x\) and returns both scratch states to \(a_0,c_0\). The three completed data stages are

\[
Y\leftarrow Y+X,\qquad X\leftarrow X-Y,\qquad Y\leftarrow Y+X.
\]

Thus the signed endpoint is \((-Y,X)\); over \(\mathbb F_2\), it is the ordinary bank exchange.

The complex array/frame interface is more specific than the scalar identity. Its labels lie in \(\mathcal F=(\mathbb F_2^h)^{\otimes3}\). For \(u_a=t_{a_1}\otimes t_{a_2}\otimes t_{a_3}\), the source and sink labels are \(X_a:\langle u_a\rangle\to\mathcal F\), \(Y_a:0\to\langle u_a\rangle^\perp\), and each scratch role \(0\to\mathcal F\). All incidences of a pointwise gate share one frame. For physical input \(f\), the logical input is defined by \(g=D_{\rm in}^{-1}f\); the implemented map is \(D_{\rm out}\mathsf S_\Omega D_{\rm in}^{-1}\). On a routed role \(w\), the endpoint action is its scalar route sign times \(D_{\mathrm{sink}(\rho(w))}D_{\mathrm{source}(w)}^{-1}\). The bit interface has its own rational matrices and its own role permutation \(\rho\), with \(\rho(X_a)=Y_a\), \(\rho(Y_a)=X_a\), and \(\rho\) fixing every scratch role.

Section 4 turns the **bit** interface into the actual tape operation. For every input role \(w\), including scratch, it requires

\[
M_{\mathrm{out}(\rho(w))}-M_{\mathrm{in}(w)}=I_m,\qquad
s=\sum_e\operatorname{rank}_{\mathbb Q}(M_{\mathrm{head}(e)}-M_{\mathrm{tail}(e)})<Wm.
\]

A rank-\(r\) edge is paid as \(r\) recursive address-chunk interchanges. The finite circuit first realizes the shear \(H\leftarrow H+D\); three shears give the complete chunk permutation \((H,D)\mapsto(D,H)\). Prefix, gap, suffix, row order, all non-role fields, and arbitrary scratch values are preserved. The resulting recurrence is \(F_k\le(s/W)F_{k-1}+O(1)\). This endpoint and cost contract is the manuscript's data-moving operation; a scalar signed involution does not imply it.

Section 6 uses that chunk interchange inside the recorded transform layout \(L\), where \(B\) is the stored bit-reversal permutation. The forward transform stores \(LB F_{\boldsymbol t}^{-}\); pointwise normalized polynomial products and signed coefficient recovery retain that record order; the opposite transform consumes it with \(F_{\boldsymbol t}^{+}B^{-1}L^{-1}\), scales by the axis count, and returns the array in its original order and coefficient format. No Walsh–Hadamard output decoder or multiplication reduction follows from the five-stage word alone.

## Walsh–Hadamard types reported by [upstream PR 209](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/209)

[Upstream PR 209](https://redirect.github.com/CrocSwap/integer-mult-bounds/pull/209) is a documentation-only contribution pointing to the separately pinned [WHT project commit fdfb7815c15ec43af0fb54818a6a57ae4025126b](https://redirect.github.com/jacobalansussman/wht-power-saving-lean/commit/fdfb7815c15ec43af0fb54818a6a57ae4025126b). Its Lean statement has input \((k,I,x)\), with \(x:\mathrm{Fin}(2^k)\to\mathbb C\), and output

\[
\operatorname{wht}(k,x)_j
=\sum_{\ell\in\mathrm{Fin}(2^k)}
(-1)^{\operatorname{popcount}(j\mathbin{\&}\ell)}x_\ell
\]

in natural Sylvester order. The reported saving \(7.474547\times10^{-4}\) is for \(O(N(\log N)^{1-\delta})\) in that exact-complex RAM model. It is not an integer-multiplication \(\kappa\).

In the pinned WHT construction, a class \((g,t)\) has two distinct bank pairs \(X_1,Y_1\) and \(X_2,Y_2\). Their twin \(X\)-roles begin in the same line frame, and their twin \(Y\)-roles begin at the same zero frame. The five invocations are forward/backward/forward on pair 1, then backward/forward on pair 2. Three free inter-pair gate layers are legal only at equal frames. The abstract chain sends each pair to \((-y_i,x_i)\), then applies the usual signed exchange. The construction uses shared helper slots; an invocation accepts arbitrary helper matrices and the full bridge chain restores its helper values in its own contract.

The concrete WHT geometry uses \(h=22\), \(v=1320\), \(m=5h=110\), and \(R=9412\) helper arrays; its live stock per group is \(W=4v+R=14692\). It also explicitly pays for idle climbs and the five helper-circuit invocations. These are WHT labels, roles, and prices. They are not the manuscript's \(h=100\), \(m=h^3\), \(\mathcal T^3\) role set or its Section 4 endpoint matrices.

## Translation attempt and exact failure

The natural attempted map sends the WHT twin pairs at a class to two original data pairs \((X_a,Y_a)\), \((X_b,Y_b)\) and must preserve the equal twin source frames. In the original source, those frames are \(\langle u_a\rangle\) and \(\langle u_b\rangle\). The map \(a\mapsto\langle u_a\rangle\) is injective: over \(\mathbb F_2\) a nonzero line has a unique vector; equality of nonzero simple tensors forces equality of their factor lines; and the indicator line \(\langle t_T\rangle\) uniquely identifies each triple \(T\). Therefore equal original \(X\)-source frames imply \(a=b\).

If \(a\ne b\), the twin-frame equality needed by the WHT free inter-pair gates fails. If \(a=b\), the two WHT pairs alias the same original \(X_a,Y_a\) roles instead of carrying four independent bank values; for example, the gate \(X_1\leftarrow X_1+X_2\) ceases to be the stated two-role gate. Mapping one twin to a side or center scratch role also fails: original scratch has the endpoint type \(0\to\mathcal F\), is fixed by \(\rho\), and is not an independent data pair. This rules out the direct role-preserving embedding, not every possible new multiplication architecture.

There is also no coefficient-reduction shortcut for a bit supplier. The complex source ring in Section 3 inverts 2, while \(2=0\) in \(\mathbb F_2\). A unital ring map \(\mathbb Z[i,1/2]\to\mathbb F_2\) cannot exist: \(2(1/2)=1\) would map to \(0=1\). The bit network must be built and proved separately.

The missing result is a typed embedding theorem that supplies four independent, legal original-style bank roles per bridged class (or a new complete source type), maps every class and data index with no omissions or aliases, matches every inter-pair gate's common frame, preserves signed outputs and arbitrary dirty-state restoration, and gives a separate \(\mathbb F_2\) role network satisfying the full Section 4 endpoint equation and a complete paid rank ledger. Without that theorem, Phase 0 stops here.
