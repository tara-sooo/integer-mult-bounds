#!/usr/bin/env python3
"""Exact exhaustive four-bit check of adjacent product windows."""
import json
from collections import Counter


def decode(p00, p01, p10, p11, n):
    m = n // 2
    low_mask = (1 << m) - 1
    low = p00 & low_mask
    carry = p00 >> m
    high = carry + p01 + p10 + (p11 << m)
    return low, high, carry


def multiply(a, b, n, nodes):
    assert n >= 1 and n & (n - 1) == 0
    assert 0 <= a < 1 << n and 0 <= b < 1 << n
    nodes[n] += 1
    if n == 1:
        product = a * b
        return product, product, 0, 0

    m = n // 2
    mask = (1 << m) - 1
    a0, a1 = a & mask, a >> m
    b0, b1 = b & mask, b >> m
    p00 = multiply(a0, b0, m, nodes)[0]
    p01 = multiply(a0, b1, m, nodes)[0]
    p10 = multiply(a1, b0, m, nodes)[0]
    p11 = multiply(a1, b1, m, nodes)[0]
    assert all(0 <= p < 1 << (2 * m) for p in (p00, p01, p10, p11))
    low, high, carry = decode(p00, p01, p10, p11, n)
    product = low + (high << m)
    assert product == a * b
    assert 0 <= low < 1 << m
    assert 0 <= high < 1 << (2 * n - m)
    return product, low, high, carry


def child_products(a, b, n):
    m = n // 2
    mask = (1 << m) - 1
    a0, a1 = a & mask, a >> m
    b0, b1 = b & mask, b >> m
    return tuple(
        multiply(x, y, m, Counter())[0]
        for x, y in ((a0, b0), (a0, b1), (a1, b0), (a1, b1))
    )


def main():
    n = 4
    checked = 0
    for a in range(1 << n):
        for b in range(1 << n):
            nodes = Counter()
            product, low, high, carry = multiply(a, b, n, nodes)
            expected = a * b
            assert product == expected
            assert low == expected & 0b11
            assert high == expected >> 2
            assert low + (high << 2) == expected
            assert 0 <= carry < 4
            assert nodes == Counter({4: 1, 2: 4, 1: 16})
            checked += 1

    child_pairs = 0
    for a in range(4):
        for b in range(4):
            assert multiply(a, b, 2, Counter())[0] == a * b
            child_pairs += 1

    residuals = {(a * b) >> 2 for a in range(4) for b in range(4)}
    assert residuals == {0, 1, 2}
    required_residual_bits = (len(residuals) - 1).bit_length()
    assert required_residual_bits == 2 > 1

    a, b = 1, 4
    p00, p01, p10, p11 = child_products(a, b, n)
    low, high, _ = decode(p00, p01, p10, p11, n)
    omitted_low, omitted_high, _ = decode(p00, 0, p10, p11, n)
    omitted_expected = a * b
    omitted_got = omitted_low + (omitted_high << 2)
    assert low + (high << 2) == omitted_expected == 4
    assert omitted_got == 0 and omitted_got != omitted_expected

    a, b = 3, 3
    p00, p01, p10, p11 = child_products(a, b, n)
    low, high, carry = decode(p00, p01, p10, p11, n)
    corrupt_got = low + ((high - 1) << 2)
    assert carry == 2
    assert corrupt_got == 5 and corrupt_got != a * b

    a, b = 0, 0
    p00, p01, p10, p11 = child_products(a, b, n)
    low, high, _ = decode(p00, p01, p10, p11, n)
    dirty_got = (low + 1) + (high << 2)
    assert dirty_got == 1 and dirty_got != a * b

    print(json.dumps({
        "status": "PASS",
        "candidate": "four-way block product with adjacent carry windows",
        "input_bits": n,
        "binary_integer_pairs_checked": checked,
        "two_bit_child_products_checked": child_pairs,
        "recursive_nodes_per_product": {"4": 1, "2": 4, "1": 16},
        "scalar_multiplication_leaves_per_product": 16,
        "window_boundary_bit": 2,
        "residual_values_with_zero_high_halves": sorted(residuals),
        "minimum_residual_bits_in_pilot": required_residual_bits,
        "adverse_controls": [
            {"fault": "omit p01", "inputs": [1, 4], "expected": 4,
             "got": omitted_got, "rejected": True},
            {"fault": "decrement carry", "inputs": [3, 3], "expected": 9,
             "got": corrupt_got, "rejected": True},
            {"fault": "dirty low accumulator", "inputs": [0, 0],
             "expected": 0, "got": dirty_got, "rejected": True}
        ],
        "scope": "exact integer semantics; fixed-tape cost is analyzed separately"
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
