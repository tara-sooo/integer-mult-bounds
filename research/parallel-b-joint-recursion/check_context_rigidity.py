#!/usr/bin/env python3
"""Exact 8x8 Section 06 layout control for one omitted chunk exchange."""

from fractions import Fraction
from itertools import product

N = 8
MOD = 17
ROOT = 2  # primitive eighth root in F_17; also the reduction of zeta_8
ADDRS = tuple(product(range(N), repeat=2))
CONTROL = ("D=2", "ell=3", "K=1", "q=2", "prefix-high-bits", "two-chunks-per-axis")


def bit_reverse_3(x):
    return ((x & 1) << 2) | (x & 2) | ((x & 4) >> 2)


def physical_address(x, y, omit_middle_chunk_exchange):
    xb = [(x >> k) & 1 for k in (2, 1, 0)]
    yb = [(y >> k) & 1 for k in (2, 1, 0)]
    if omit_middle_chunk_exchange:
        bits = [xb[0], yb[0], xb[1], xb[2], yb[1], yb[2]]
    else:
        bits = [xb[0], yb[0], xb[1], yb[1], xb[2], yb[2]]
    return sum(bit << (5 - i) for i, bit in enumerate(bits))


def storage_map(omit_middle_chunk_exchange=False):
    result = {
        (x, y): physical_address(
            bit_reverse_3(x), bit_reverse_3(y), omit_middle_chunk_exchange
        )
        for x, y in ADDRS
    }
    assert len(set(result.values())) == N * N
    return result


def store(logical, mapping):
    physical = [0] * (N * N)
    for address, target in mapping.items():
        physical[target] = logical[address[0] * N + address[1]]
    return physical


def restore_order(physical, mapping):
    return [physical[mapping[x, y]] for x, y in ADDRS]


def dft2(values):
    out = []
    for j, k in ADDRS:
        total = 0
        for x, y in ADDRS:
            total += values[x * N + y] * pow(ROOT, (-j * x - k * y) % N, MOD)
        out.append(total % MOD)
    return out


def inverse_dft2(values):
    inv_volume = pow(N * N, -1, MOD)
    out = []
    for x, y in ADDRS:
        total = 0
        for j, k in ADDRS:
            total += values[j * N + k] * pow(ROOT, (j * x + k * y) % N, MOD)
        out.append(total * inv_volume % MOD)
    return out


def pointwise_product(left, right):
    return [x * y % MOD for x, y in zip(left, right)]


def digit_array(mask):
    values = [0] * (N * N)
    for x, y in product(range(2), repeat=2):
        values[x * N + y] = (mask >> (x + 2 * y)) & 1
    return values


def encoded_integer(values):
    return sum(values[x * N + y] << (x + N * y) for x, y in product(range(2), repeat=2))


def direct_convolution(left, right):
    out = [0] * (N * N)
    for x, y in ADDRS:
        for u, v in ADDRS:
            out[((x + u) % N) * N + (y + v) % N] += left[x * N + y] * right[u * N + v]
    return out


def carry_integer(coefficients):
    result = 0
    carry = 0
    for exponent in range(N * N):
        coefficient = 0
        for x, y in ADDRS:
            if x + N * y == exponent:
                coefficient = coefficients[x * N + y]
                break
        total = coefficient + carry
        result |= (total & 1) << exponent
        carry = total >> 1
    assert carry == 0
    return result


def transformed_product(left, right, forward_mapping, decoder_mapping=None):
    left_f = dft2(left)
    right_f = dft2(right)
    if decoder_mapping is None:
        decoder_mapping = storage_map(False)
    product_physical = pointwise_product(
        store(left_f, forward_mapping), store(right_f, forward_mapping)
    )
    return inverse_dft2(restore_order(product_physical, decoder_mapping))


def contextual_call(left, right, dirty, omit_middle_chunk_exchange):
    mapping = storage_map(omit_middle_chunk_exchange)
    output = transformed_product(left, right, mapping)
    return output, CONTROL, dirty


def exact_bad_witness_real_parts():
    """Return exact cyclotomic real-part intervals for X=2, Y=1."""
    true_map = storage_map(False)
    omitted_map = storage_map(True)
    omitted_inverse = {physical: logical for logical, physical in omitted_map.items()}
    counts = [[0] * 8 for _ in range(N * N)]

    # f=delta_(1,0), g=delta_(0,0); the unchanged decoder uses true_map.
    for j, k in ADDRS:
        alt_j, _ = omitted_inverse[true_map[j, k]]
        for x, y in ADDRS:
            counts[x * N + y][(j * x + k * y - alt_j) % N] += 1

    sqrt2_lo = Fraction(141421356, 100000000)
    sqrt2_hi = Fraction(141421357, 100000000)
    assert sqrt2_lo * sqrt2_lo < 2 < sqrt2_hi * sqrt2_hi
    intervals = []
    for c in counts:
        rational = Fraction(c[0] - c[4], 64)
        sqrt_coefficient = Fraction(c[1] - c[3] - c[5] + c[7], 128)
        if sqrt_coefficient >= 0:
            lo = rational + sqrt_coefficient * sqrt2_lo
            hi = rational + sqrt_coefficient * sqrt2_hi
        else:
            lo = rational + sqrt_coefficient * sqrt2_hi
            hi = rational + sqrt_coefficient * sqrt2_lo
        intervals.append((lo, hi))
    return intervals


def main():
    true_map = storage_map(False)
    omitted_map = storage_map(True)
    assert true_map != omitted_map

    # Exact modular control for every pair of independent 2x2 binary payloads.
    failures = 0
    for left_mask, right_mask in product(range(16), repeat=2):
        left = digit_array(left_mask)
        right = digit_array(right_mask)
        expected = direct_convolution(left, right)
        assert all(
            value == 0 or (index // N <= 2 and index % N <= 2)
            for index, value in enumerate(expected)
        )
        assert max(expected) < MOD
        original = transformed_product(left, right, true_map, true_map)
        assert original == expected
        assert carry_integer(original) == encoded_integer(left) * encoded_integer(right)

        common_layout = transformed_product(left, right, omitted_map, omitted_map)
        assert common_layout == expected

        omitted = transformed_product(left, right, omitted_map, true_map)
        if omitted != expected:
            failures += 1
    assert failures > 0

    # Exact Q(zeta_8) rounding witness: every decoded real coefficient rounds to 0.
    intervals = exact_bad_witness_real_parts()
    assert all(lo > Fraction(-1, 2) and hi < Fraction(1, 2) for lo, hi in intervals)
    assert carry_integer([0] * (N * N)) == 0
    assert encoded_integer(digit_array(2)) == 2
    assert encoded_integer(digit_array(1)) == 1

    # The fixed schedule descriptor and a separate arbitrary dirty scalar are spectators.
    for dirty in range(MOD):
        _, returned_control, returned_dirty = contextual_call(
            digit_array(2), digit_array(1), dirty, True
        )
        assert returned_control == CONTROL
        assert returned_dirty == dirty

    print(f"PASS: original decoder and matched common layout for 256 pairs; omitted swap fails on {failures}")
    print("PASS: exact Q(zeta_8) witness X=2, Y=1 rounds to the wrong integer product 0")
    print("PASS: fixed descriptor and arbitrary spectator dirty value are restored")


if __name__ == "__main__":
    main()
