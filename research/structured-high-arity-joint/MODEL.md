# Structured high-arity joint recursion: scoped rank obstruction

**Checkpoint outcome:** `SCOPED_DECODER_COST_OBSTRUCTION` for linear exact-
convolution children. The selected family is a search class, not a new
multiplier. Its most aggressive natural target, one length-`m` child per
input block, is impossible by a known bilinear-rank theorem. The theorem
does not rule out `r+1` or more children and gives no new `κ`.

## Typed target and candidate class

Work over `K = Q`. For `s ≥ 1`, define
\[
 \operatorname{Conv}_s:K^s\times K^s\to K^{2s-1},\qquad
 \operatorname{Conv}_s(a,b)_k=\sum_{i+j=k}a_i b_j.
\]
When `n = r m`, write the inputs as `r` consecutive length-`m` blocks,
but allow a child to mix coefficients from every block. A `q`-child linear
reduction consists of fixed maps
\[
 U_t,V_t:K^{rm}\to K^m,\qquad
 W_t:K^{2m-1}\to K^{2rm-1}\quad(1\le t\le q)
\]
and the joint operation
\[
 z_t=\operatorname{Conv}_m(U_ta,V_tb),\qquad
 D(z_1,\ldots,z_q)=\sum_{t=1}^q W_tz_t.
\]
The exact contract is
\[
 \sum_{t=1}^q W_t\operatorname{Conv}_m(U_ta,V_tb)
 =\operatorname{Conv}_{rm}(a,b)\quad\text{for every }a,b\in K^{rm}.
\]
All child inputs are fixed before recursion starts. Each child is a real
length-`m` convolution and returns all `2m−1` coefficients. No child is
credited merely for sharing a scalar or a completed result.

The proposed structural lever is cross-block encoding with full-vector
child outputs. It could beat Toom's `2r−1` children only if the same child
convolutions jointly span the full output tensor with fewer calls. Unlike
ordinary Toom, the maps above need not be polynomial evaluations or a
Vandermonde decoder. This wider model is the point of the screen; it is not
a claim that such maps exist.

## Selected falsifiable target

The first target is the maximal-sharing subfamily `q=r`: one exact child
per input block, with arbitrary rational linear encoders and decoder. Its
smallest nontrivial pilot is `(r,m)=(3,2)`. If it survived, the next target
would be the rank-compatible case `q=4` there. The pilot rejects `q=3` and
leaves `q=4` open.

The known theorem used is that over an infinite field the bilinear rank of
length-`s` polynomial convolution is exactly `2s−1`: the lower bound is
Fiduccia–Zalcstein; Toom supplies the matching upper bound. Since a linear
composition of one `Conv_m` child has rank at most `2m−1`, every reduction
in this class must satisfy
\[
 q\ge\left\lceil\frac{2rm-1}{2m-1}\right\rceil
   =r+\left\lceil\frac{r-1}{2m-1}\right\rceil.
\]
Thus `q=r` is impossible for every `r≥2`; at `m=1` the bound is the exact
classical `2r−1` count. For `m>1` it leaves a real gap, so it is not a
general no-go theorem for high-arity joint recursion.

Here bilinear rank means the least `R` for which
`F(a,b)=Σ_(i=1)^R f_i(a)g_i(b)c_i`, with linear forms `f_i,g_i` and fixed
output vectors `c_i`. Linear pre/post maps preserve the upper bound `R`,
and ranks are subadditive under sums; these two facts give the child-count
corollary.

## Known comparison and scope

- The `2r−1` evaluation/interpolation construction is classical Toom–Cook.
  It is the baseline, not a new decoder.
- The pinned manuscript already has synthetic Fourier transforms for its
  own typed cyclic-convolution pipeline. Reusing that transform or its
  fixed-tape theorem would be a known-method comparison, not a new lever.
- The original manuscript's Section 4 child is a full-array address
  interchange with an edge-rank recurrence. A `Conv_m` child has different
  input/output types and no proved bridge to that recurrence.
- The present theorem covers only exact bilinear reductions with linear
  maps over `Q` and recursive children exactly of type `Conv_m`. It says
  nothing about non-linear encoders, alternate rings, approximate
  arithmetic, modular multi-prime states, or other child types.

For binary integers, take the `N` input coefficients in `{0,1}`. Their exact
integer convolution has coefficients `0≤c_k≤N`, and the usual binary carry
recurrence recovers the product. A `Q`-linear identity is therefore a valid
algebraic identity on those inputs, but rational intermediate values,
normalization, and their costs must still be paid. No bit-complexity or
fixed-tape improvement follows from the rank statement.
