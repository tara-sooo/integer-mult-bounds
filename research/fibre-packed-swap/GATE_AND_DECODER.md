# Gate, endpoint, and decoder check

## Required semantic endpoints

For all 20 independent triples \(T\), the complex scalar endpoint must
send \((X_T,Y_T,\zeta)\) to \((-Y_T,X_T,\zeta)\), preserving every
arbitrary private side/center/helper value. The bit endpoint separately
must exchange the full address chunks on every array row, include all
scratch roles, and restore the original row/role order. A lane decoder
must recover every original \(X_T,Y_T\) and every spectator exactly.

The storage \(D\circ E=\mathrm{id}\) from PACKING_CONTRACT.md meets only
that storage-recovery statement. Applying the original scalar network
lane by lane has the original independent work; a wrong
\(Y_T\leftrightarrow X_{\tau(T)}\) route fails on distinct lane values.
The checker also rejects a wrong sign, a dropped member of a
\(\tau\)-pair, and zero-filled padding that discards dirty state.

## Actual Section 3 consumer and failed retyping

The fixed \(A,B\) fibre is the stage-3 invocation in the original
construction. At its time-2 X-side copy gate, the common label for a
source triple \(T\) is
\[
L_T=(B_0\otimes F)\mathbin{\perp}
      (P_0\otimes\langle t_T\rangle),\qquad
P_0=\langle t_A\otimes t_B\rangle,\quad B_0=P_0^\perp.
\]
The remaining \(\tau\)-pair lines differ. \(P_{AB}\) correctly maps the
terminal source line \(u_{A,B,T}\) to \(u_{A,B,\tau(T)}\), but it does
not map the complete Section 3 gate label \(L_T\) to \(L_{\tau(T)}\).

Here is an exact \(h=6\) witness in the bit construction's rational
label form \(I-J/9\). Take \(A=\{1,2,3\}\), \(B=\{1,2,4\}\),
\(T=\{1,3,5\}\), and \(\tau(T)=\{2,4,6\}\). Put
\[
g=t_A\otimes t_B,\qquad
b=e_{(1,1)}-4e_{(4,5)}.
\]
Since \(\langle t_A,e_1\rangle=\langle t_B,e_1\rangle=2/3\) and
\(\langle t_A,e_4\rangle=\langle t_B,e_5\rangle=-1/3\),
\(\langle g,b\rangle=4/9-4/9=0\). Thus \(x=b\otimes e_1\) lies in the
common \(B_0\otimes F\) summand of \(L_T\). With \(p_1=1,q_1=2\),
\(\phi_1(x)=1\) and the other \(\phi\) values vanish, so
\[
P_{AB}x=x+g\otimes(e_2-e_1).
\]
The added \(P_0\)-component has third factor \(e_2-e_1\), which is not
in \(\langle t_{\tau(T)}\rangle
=\langle e_2+e_4+e_6\rangle\). Therefore
\(P_{AB}x\notin L_{\tau(T)}\). This is a concrete failure of the
candidate source-label map to retype this actual gate frame.

It is not a proof that every possible adapter fails. A replacement
would need an explicit physical map for the whole gate label, common
frames on every operand, and a typed decoder for the resulting lane
layout.

## Physical array bridge still absent

On the complex side, Section 3 uses \(\mathcal C_U\) on arrays with
\(2^m\) addresses. The label map \(P_{AB}\) acts on \(m\) coordinates
and does not identify \(\mathcal C_{U'}\mathcal C_U^{-1}\) for any pair
of labels. No common complex array gate for the ten contexts was built.

On the bit side, Section 4 assigns rational \(m\times m\) matrices to
all terminals and gates and requires
\(M_{\mathrm{out}(\rho(w))}-M_{\mathrm{in}(w)}=I_m\) for every role,
plus a total paid edge rank below \(Wm\). It then swaps both full
address chunks, restores row order, and includes arbitrary dirty
scratch. The label rank of \(P_{AB}-I\) supplies neither this all-role
identity nor a complete Section 4 role network. The stage-3 witness
above already blocks using \(P_{AB}\) as the missing common gate
retyping.

Therefore no full-array bit Swap, complex signed Swap, cross-pair
physical consumer, or operation-level decoder is claimed. No clean
scratch argument substitutes for the arbitrary-dirty contract.
