#!/usr/bin/env python3
"""Exact Conv_6 semantics and the scoped 3-child rank-capacity obstruction."""
import json
from itertools import product as cartesian_product
from time import perf_counter


def main():
    start = perf_counter()
    r, m = 3, 2
    n = r * m
    target_rank = 2 * n - 1  # classical exact rank of Conv_n over Q
    child_rank = 2 * m - 1

    checked = 0
    for i in range(n):
        for j in range(n):
            product = [0] * (2 * n - 1)
            product[i + j] += 1  # Conv_n(e_i, e_j)
            expected = [int(k == i + j) for k in range(2 * n - 1)]
            assert product == expected
            checked += 1

    integer_pairs = 0
    for a in cartesian_product((0, 1), repeat=n):
        a_value = sum(bit << i for i, bit in enumerate(a))
        for b in cartesian_product((0, 1), repeat=n):
            b_value = sum(bit << i for i, bit in enumerate(b))
            coeffs = [
                sum(a[i] * b[k - i] for i in range(n) if 0 <= k - i < n)
                for k in range(2 * n - 1)
            ]
            carry = 0
            recovered = 0
            for k, coefficient in enumerate(coeffs):
                carry += coefficient
                recovered |= (carry & 1) << k
                carry >>= 1
            bit = 2 * n - 1
            while carry:
                recovered |= (carry & 1) << bit
                carry >>= 1
                bit += 1
            assert recovered == a_value * b_value
            integer_pairs += 1

    q_candidate = r
    q_min = (target_rank + child_rank - 1) // child_rank
    assert target_rank == 11
    assert child_rank == 3
    assert q_candidate * child_rank == 9 < target_rank
    assert q_min == 4
    assert 4 * child_rank == 12 >= target_rank  # rank gate cannot decide q=4

    print(json.dumps({
        "status": "PASS_SCOPED_RANK_GATE",
        "field_for_rank_statement": "Q",
        "integer_target_tensor_basis_pairs_checked": checked,
        "binary_integer_product_pairs_checked": integer_pairs,
        "r": r,
        "m": m,
        "n": n,
        "target_rank_from_classical_theorem": target_rank,
        "child_rank_from_classical_theorem": child_rank,
        "rejected_candidate_child_count": q_candidate,
        "rejected_candidate_rank_capacity": q_candidate * child_rank,
        "rank_lower_bound_on_child_count": q_min,
        "q4_rank_capacity": 4 * child_rank,
        "q4_status": "NOT_DECIDED",
        "runtime_seconds": round(perf_counter() - start, 6),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
