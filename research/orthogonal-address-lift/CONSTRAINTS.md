# Exact address constraints

This screen follows [Issue 29](https://redirect.github.com/tara-sooo/integer-mult-bounds/issues/29) and holds the operator pinned at [Issue 28 commit c4c9c6461d86b84774b9a8cd0b5907549275c740](https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/c4c9c6461d86b84774b9a8cd0b5907549275c740). No coefficient is tuned.

Let $E_K=\{(T,S):K'_{T,S}\ne0\}$ and $E_H=\{(T,S):H'_{T,S}\ne0\}$. The exact domains contain 136 and 386 directed edges, with 6 shared edges and 516 edges in their union. The receipt lists every edge with its doubled coefficient; its union list records each edge and old address parity. Full doubled matrices also retain every zero. Thus edges introduced from zero by the shear are included.

For every $(T,S)\in E_K\cup E_H$, define $R_{T,S}=q_T\cdot q_S$. The required equation is

$$
R_{T,S}+u_T^{\rm tgt}\cdot u_S^{\rm src}=0\quad\text{in }\mathbb F_2.
$$

In rank 1, each appended label is a bit, so its product must equal $R_{T,S}$.

## Rank 1 common labels: exact UNSAT

Model A sets $u_i^{\rm src}=u_i^{\rm tgt}=u_i$. Three checked edges suffice:

| Edge | Matrix coefficient | Old address parity | Required product |
|---|---:|---:|---:|
| $(0,10)$ in $K'$ | $-1/2$ | 1 | $u_0u_{10}=1$ |
| $(2,8)$ in $K'$ | $+1/2$ | 1 | $u_2u_8=1$ |
| $(0,2)$ in $K'$ | $-1/2$ | 0 | $u_0u_2=0$ |

The first two equations force $u_0=u_2=1$, contradicting the third. The checker asserts the exact coefficients and old parities, so this is a finite UNSAT certificate, not a failed search.

## Rank 1 distinct source and target labels: exact UNSAT

Model B has independent target bits $x_i=u_i^{\rm tgt}$ and source bits $y_i=u_i^{\rm src}$. It is checked separately:

| Edge | Matrix coefficient | Old address parity | Required product |
|---|---:|---:|---:|
| $(0,10)$ in $K'$ | $-1/2$ | 1 | $x_0y_{10}=1$ |
| $(2,8)$ in $K'$ | $+1/2$ | 1 | $x_2y_8=1$ |
| $(0,8)$ in $H'$ | $-1/2$ | 0 | $x_0y_8=0$ |

The first two equations force $x_0=y_8=1$, contradicting the third. This is UNSAT even before requiring an encoder or decoder. No result from this model is counted as common-address success.

## Rank 2 common labels: exact Gram witness

Because common rank 1 is exactly UNSAT, one rank 2 common-label experiment was run. In coordinate order 8, 9, a complete assignment is

| Port indices | Appended vector |
|---|---|
| 0, 10, 12 | $(1,0)$ |
| 2, 4, 8 | $(0,1)$ |
| all other 26 ports | $(0,0)$ |

For every one of the 516 edges in $E_K\cup E_H$, the checker verifies

$$
q_T\cdot q_S+u_T\cdot u_S=0.
$$

The receipt carries the full 32-vector list and lifted masks. This is an exact partial Gram completion for the fixed support. It is not a source-defined physical encoding, and no separate-label rank 2 search was run.

The same lifted labels were also checked on every nonzero edge of the original baseline supports: all 128 K edges and all 384 H edges pass, with zero violations in either set. The checker records both counts and empty violation lists. B remains the separate 544-entry coordinate-star center channel; it is not included in the K/H pairwise cap.

## Independent no-isometry control

The old witness has $q_0\cdot q_{10}=1$. A common orthogonal transformation of the old $\mathbb F_2^8$ space preserves that value, so it cannot fix the Issue 28 support. The checker keeps this as a negative control and never enumerates an orthogonal group.
