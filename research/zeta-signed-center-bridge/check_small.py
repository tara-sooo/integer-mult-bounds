#!/usr/bin/env python3
"""Exact signed-center factorization and bounded zeta inventory."""
from fractions import Fraction as Q
import hashlib
from itertools import combinations, product
import json
from pathlib import Path


def triples(h):
    return [tuple(s) for s in combinations(range(h), 3)]


def p4_ports():
    return [tuple(sorted(2 * i + b for i, b in zip(I, bits)))
            for I in combinations(range(4), 3)
            for bits in product((0, 1), repeat=3)]


def mask(s):
    return sum(1 << i for i in s)


def matrix_check(ports):
    h, n = max(max(s) for s in ports) + 1, len(ports)
    x = [Q(1)] * n
    z = [[Q(int(not (mask(s) >> i & 1))) for s in ports] for i in range(h)]
    factored = []
    expected = []
    for t in ports:
        factored.append([x[j] - Q(1, 2) * sum(z[i][j] for i in t)
                         for j in range(n)])
        expected.append([Q(len(set(t) & set(s)) - 1, 2) for s in ports])
    assert factored == expected
    twice_B = [[int(2 * value) for value in row] for row in expected]
    digest = hashlib.sha256(json.dumps(twice_B, separators=(",", ":")).encode()).hexdigest()
    return dict(
        h=h, ports=n, rows=n, columns=n, coefficient_pairs_checked=n * n,
        twice_B_sha256=digest,
        all_coefficients_dyadic=all(v.denominator & (v.denominator - 1) == 0
                                     for row in factored for v in row),
    )


def dyadic_vector_check(ports):
    h = max(max(s) for s in ports) + 1
    x = [Q((j % 7) - 3, 8) for j in range(len(ports))]
    total = sum(x)
    checked = 0
    for t in ports:
        z = [sum(x[j] for j, source in enumerate(ports) if i not in source)
             for i in range(h)]
        factored = total - Q(1, 2) * sum(z[i] for i in t)
        direct = sum(Q(len(set(t) & set(source)) - 1, 2) * x[j]
                     for j, source in enumerate(ports))
        assert factored == direct
        checked += 1
    assert any(value.denominator == 8 for value in x)
    return dict(target_vectors_checked=checked, input_denominator=8, exact=True)

def zeta_dag(h):
    full = (1 << h) - 1
    inputs = list(range(1, full))
    index = {u: i for i, u in enumerate(inputs)}
    args = [None] * len(inputs)
    prev = {u: index[u] for u in inputs}
    for bit in range(h):
        cur = {}
        for w in inputs:
            node = prev[w]
            lower = w ^ (1 << bit)
            if (w >> bit) & 1 and lower != 0 and lower in prev:
                args.append((node, prev[lower]))
                node = len(args) - 1
            cur[w] = node
        prev = cur
    roots = [(t, prev[full ^ t]) for t in inputs if full ^ t]
    return inputs, args, roots


def zeta_inventory():
    h = 8
    inputs, args, roots = zeta_dag(h)
    v = len(inputs)
    forms = [1 << i for i in range(v)]
    for node in range(v, len(args)):
        a, b = args[node]
        assert a < node and b < node and not (forms[a] & forms[b])
        forms.append(forms[a] | forms[b])
    index = {u: i for i, u in enumerate(inputs)}
    for t, node in roots:
        want = sum(1 << index[u] for u in inputs if not (u & t))
        assert forms[node] == want

    ops = [(node, source) for node in range(v, len(args))
           for source in args[node]]
    singleton_terms = []
    total_pre_reads = 0
    for t, root in roots:
        adj = [0] * len(args)
        adj[root] = 1
        for dst, src in reversed(ops):
            adj[src] += adj[dst]
        assert max(adj) == 1
        terms = sum(value != 0 for value in adj)
        total_pre_reads += terms
        if t & (t - 1) == 0:
            singleton_terms.append(terms)

    ports = p4_ports()
    active = {mask(s) for s in ports}
    singleton_support = [u for u in inputs if not (u & 1)]
    assert len(inputs) == 254 and len(ports) == 32
    assert active <= set(inputs) and len(active) == 32
    assert len([u for u in inputs if u.bit_count() == 3]) == 56
    assert len([u for u in inputs if u.bit_count() != 3]) == 198
    assert len(inputs) - len(active) == 222
    assert len(singleton_support) == 127
    assert sum(u in active for u in singleton_support) == 20
    assert len(singleton_support) - 20 == 107
    assert len(args) - v == 1008
    assert len(args) == 1262
    assert len(roots) == 254
    assert sum(t & (t - 1) == 0 for t, _ in roots) == 8
    assert singleton_terms == [253] * 8
    assert total_pre_reads == 11846
    assert len(ops) == 2016
    assert 2 * len(ops) == 4032

    return dict(
        h=h, input_masks=v, p4_data_inputs=len(active), zero_data_inputs=v-len(active),
        zero_inputs_split=dict(nontriple_masks=198, triple_masks_outside_P4=24),
        appended_accumulator_nodes=len(args)-v, total_roles=len(args),
        roots=len(roots), singleton_roots=8, other_roots=246,
        singleton_source_slots=127, singleton_P4_contributions=20,
        singleton_zero_contributions=107,
        scalar_updates=dict(forward=len(ops), inverse=len(ops),
                            forward_plus_inverse=2*len(ops)),
        raw_dirty_preread_terms=dict(all_roots=total_pre_reads,
                                     singleton_roots=sum(singleton_terms),
                                     per_singleton_root=singleton_terms,
                                     maximum_adjoint_coefficient=1),
        graph_table_R=len(args),
        readme_claimed_additions=h*(1 << (h-1))-((1 << h)-1),
        readme_claim_disagrees_with_appended_nodes=(
            h*(1 << (h-1))-((1 << h)-1) != len(args)-v),
        source_data_histogram={"1": v*(h-3), "2": v},
        source_data_histogram_mass=v*(h-1),
    )


def binary_rank(rows):
    basis = {}
    for value in rows:
        x = value
        for pivot, row in sorted(basis.items(), reverse=True):
            if x >> pivot & 1:
                x ^= row
        if x:
            pivot = x.bit_length() - 1
            for j, row in list(basis.items()):
                if row >> pivot & 1:
                    basis[j] = row ^ x
            basis[pivot] = x
    return len(basis)


def main():
    # FAST: symbolic coefficient reduction and exact complete matrices.
    symbolic = [dict(overlap=k, candidate=str(Q(1)-Q(3-k, 2)),
                     source_B=str(Q(k-1, 2))) for k in range(4)]
    assert all(Q(1)-Q(3-k, 2) == Q(k-1, 2) for k in range(4))
    h4 = matrix_check(triples(4))
    p4 = p4_ports()
    p4_check = matrix_check(p4)
    assert h4["coefficient_pairs_checked"] == 16
    assert p4_check["coefficient_pairs_checked"] == 1024
    dyadic_h4 = dyadic_vector_check(triples(4))
    dyadic_p4 = dyadic_vector_check(p4)
    assert all(2 * Q(k-1, 2) == k-1 for k in range(4))
    assert Q(1, 2).denominator == 2
    assert Q(1, 2).denominator & (Q(1, 2).denominator - 1) == 0

    # Exact controls: omitting X, confusing disjointness with B, or dropping 1/2.
    same = (0, 2, 4)
    missing_x_value = -Q(1, 2) * sum(int(i not in same) for i in same)
    missing_x_B = Q(1)
    assert missing_x_B == 1 and missing_x_value == 0
    assert missing_x_value != missing_x_B
    miss_x = dict(target=[1, 3, 5], source=[1, 3, 5], B=str(missing_x_B),
                  without_X=str(missing_x_value))
    overlap_two = ((0, 2, 4), (0, 2, 6))
    t, s = overlap_two
    correct = Q(len(set(t) & set(s))-1, 2)
    z_sum = sum(int(i not in s) for i in t)
    assert correct == Q(1, 2) and z_sum == 1
    disjointness = int(not (set(t) & set(s)))
    assert disjointness == 0 and disjointness != correct
    disjoint_control = dict(target=[i+1 for i in t], source=[i+1 for i in s],
                            intersection=2, B=str(correct), disjointness_indicator=disjointness,
                            no_half_decoder=str(Q(1)-z_sum),
                            no_half_value_differs=True)
    assert Q(1)-z_sum != correct
    h, p = 8, 4
    div = h-3
    assert div == 5 and Q(1, div).denominator == 5
    assert Q(1, div).denominator & (Q(1, div).denominator-1) != 0
    division_control = dict(h=h, h_minus_3=div, inverse="1/5",
                            dyadic_denominator=False,
                            basis_vector_sum_singleton_roots=div,
                            basis_vector_X=1,
                            both_sides_mod_5=dict(root_sum=0, X=1))
    assert division_control["both_sides_mod_5"]["root_sum"] != division_control["both_sides_mod_5"]["X"]
    disjoint = ((0, 2, 4), (1, 3, 5))
    h0_pair = (Q(len(set(disjoint[0]) & set(disjoint[1]))) -
               Q(len(disjoint[0]) * len(disjoint[1]), 9)) / 2
    assert h0_pair == Q(-1, 2)

    # Address-span dimensions use PR144's binary address field, not scalar coefficients.
    ports = p4
    root_uses = [sum(i in t for t in ports) for i in range(8)]
    assert root_uses == [12]*8
    star_ranks = [binary_rank([mask(s) for s in ports if i in s]) for i in range(8)]
    complement_ranks = [binary_rank([mask(s) for s in ports if i not in s])
                        for i in range(8)]
    total_rank = binary_rank([mask(s) for s in ports])
    assert star_ranks == [6]*8 and complement_ranks == [7]*8 and total_rank == 8

    # FOCUSED: exact pinned PR172 h=8 DAG/root chronology and dirty-read inventory.
    inventory = zeta_inventory()
    assert inventory["readme_claimed_additions"] == 769
    assert inventory["appended_accumulator_nodes"] == 1008
    assert inventory["graph_table_R"] == 1262

    receipt = dict(
        status="SIGNED_CENTER_IS_EXISTING_STAR_METHOD",
        algebra=dict(symbolic_overlap_cases=symbolic, h4_triple_space=h4,
                     p4_h8_all_ports=p4_check,
                     dyadic_vectors=dict(h4=dyadic_h4, p4_h8=dyadic_p4),
                     coefficient_ring=dict(Q=True, Z_i_1_over_2=True,
                                           half_is_in_dyadic_ring=True,
                                           half_is_defined_in_F2=False,
                                           h8_inverse_1_over_5_is_dyadic=False)),
        negative_controls=dict(missing_X=miss_x,
                               disjoint_indicator_and_missing_half=disjoint_control,
                               forbidden_h_minus_3_division=division_control,
                               literal_H0_disjoint_triples=dict(pairing=str(h0_pair),
                                                               required_pairing=0)),
        p4_center_span_inventory=dict(
            star_root_dimensions=star_ranks, star_total_dimension=sum(star_ranks),
            complement_root_dimensions=complement_ranks,
            complement_total_dimension=sum(complement_ranks),
            full_X_source_span_dimension=total_rank,
            direct_X_plus_complement_total_dimension=sum(complement_ranks)+total_rank,
            source_note="source-span dimensions only; a derived sum is not a physical frame charge"),
        decoder_inventory=dict(p4_ports=32, X_uses=32,
                               singleton_root_uses=root_uses,
                               total_singleton_root_uses=sum(root_uses),
                               shared_half_schedule=dict(half_scalings=8,
                                                        signed_additions=96)),
        zeta_h8_focused_inventory=inventory,
    )
    path = Path(__file__).with_name("small_exact_receipt.json")
    path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print("FAST exact matrices PASS: h=4 pairs=16; P4/h=8 pairs=1024")
    print("FOCUSED zeta inventory PASS: inputs=254 nodes=1008 roles=1262; singleton pre-reads=2024")
    print("receipt=" + str(path))


if __name__ == "__main__":
    main()
