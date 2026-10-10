#!/usr/bin/env python3
"""Exact n=2 NTT/CRT convolution pilot; standard library only."""

import itertools
import json
import platform
import time


N = 2
BETA = 4
L = 4
MODULI = ((17, 4), (97, 22))


def dft(values, p, root, inverse=False):
    n = len(values)
    assert n and n & (n - 1) == 0
    if inverse:
        root = pow(root, -1, p)
    out = list(values)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            out[i], out[j] = out[j], out[i]
    length = 2
    while length <= n:
        step = pow(root, n // length, p)
        for start in range(0, n, length):
            twiddle = 1
            for offset in range(length // 2):
                left = out[start + offset]
                right = out[start + offset + length // 2] * twiddle % p
                out[start + offset] = (left + right) % p
                out[start + offset + length // 2] = (left - right) % p
                twiddle = twiddle * step % p
        length *= 2
    if inverse:
        scale = pow(n, -1, p)
        out = [scale * value % p for value in out]
    return out


def residues_for_prime(a, b, p, root):
    aa = list(a) + [0] * (L - len(a))
    bb = list(b) + [0] * (L - len(b))
    fa = dft([x % p for x in aa], p, root)
    fb = dft([x % p for x in bb], p, root)
    pointwise = [x * y % p for x, y in zip(fa, fb)]
    return dft(pointwise, p, root, inverse=True)


def crt_pair(x, y):
    p, q = MODULI[0][0], MODULI[1][0]
    return x + p * ((y - x) * pow(p, -1, q) % q)


def exact_convolution(a, b):
    by_prime = [residues_for_prime(a, b, p, root) for p, root in MODULI]
    return [crt_pair(by_prime[0][k], by_prime[1][k]) for k in range(2 * N - 1)]


def direct_convolution(a, b):
    out = [0] * (2 * N - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def carry_digits(coefficients, beta):
    digits = []
    carry = 0
    for coefficient in coefficients:
        carry, digit = divmod(coefficient + carry, beta)
        digits.append(digit)
    while carry:
        carry, digit = divmod(carry, beta)
        digits.append(digit)
    return digits


def digits_value(digits, beta):
    return sum(digit * beta**i for i, digit in enumerate(digits))


def kronecker_coefficients(a, b, radix):
    packed_a = sum(x * radix**i for i, x in enumerate(a))
    packed_b = sum(x * radix**i for i, x in enumerate(b))
    product = packed_a * packed_b
    coefficients = []
    for _ in range(2 * N - 1):
        product, coefficient = divmod(product, radix)
        coefficients.append(coefficient)
    assert product == 0
    return packed_a, packed_b, coefficients


def main():
    start = time.perf_counter()
    assert L >= 2 * N - 1
    assert 17 * 97 > N * (BETA - 1) ** 2
    for p, root in MODULI:
        assert (p - 1) % L == 0
        assert pow(root, L, p) == 1
        assert pow(root, L // 2, p) == p - 1
        assert (L * pow(L, -1, p)) % p == 1

    # The four basis-pair products are the full 2 x 2 -> 3 bilinear tensor.
    for i, j in itertools.product(range(N), repeat=2):
        a = [0] * N
        b = [0] * N
        a[i] = b[j] = 1
        expected = [0] * (2 * N - 1)
        expected[i + j] = 1
        assert exact_convolution(a, b) == expected

    # Exhaust the whole bounded pilot domain, not only random vectors.
    checked = 0
    for values in itertools.product(range(BETA), repeat=2 * N):
        a, b = values[:N], values[N:]
        coefficients = exact_convolution(a, b)
        assert coefficients == direct_convolution(a, b)
        assert all(0 <= c <= N * (BETA - 1) ** 2 for c in coefficients)
        product_digits = carry_digits(coefficients, BETA)
        x = digits_value(a, BETA)
        y = digits_value(b, BETA)
        assert digits_value(product_digits, BETA) == x * y
        checked += 1

    # Adverse control: p=17 alone aliases coefficient 18 to 1.
    a = b = [3, 3]
    true_coefficients = direct_convolution(a, b)
    bad_coefficients = residues_for_prime(a, b, *MODULI[0])[: 2 * N - 1]
    bad_product = digits_value(carry_digits(bad_coefficients, BETA), BETA)
    true_product = digits_value(a, BETA) * digits_value(b, BETA)
    assert true_coefficients == [9, 18, 9]
    assert bad_coefficients == [9, 1, 9]
    assert bad_product != true_product

    # A product decoder promising canonical base-four digits must carry.
    assert any(c >= BETA for c in true_coefficients)
    assert digits_value(carry_digits(true_coefficients, BETA), BETA) == true_product

    # The alternative Kronecker map is exact but its child is wider here.
    assert 32 > N * (BETA - 1) ** 2
    packed_a, packed_b, packed_conv = kronecker_coefficients(a, b, 32)
    assert packed_conv == true_coefficients
    assert packed_a == packed_b == 99
    assert packed_a.bit_length() == 7
    assert digits_value(a, BETA).bit_length() == 4
    assert packed_a.bit_length() > digits_value(a, BETA).bit_length()

    elapsed_ms = (time.perf_counter() - start) * 1000
    receipt = {
        "status": "PASS",
        "command": "python3 -B research/parallel-a-typed-reduction/check_exact.py",
        "python": platform.python_version(),
        "pilot": {"n": N, "beta": BETA, "L": L, "primes": [p for p, _ in MODULI], "crt_modulus": 17 * 97},
        "checks": {
            "primitive_roots_and_inverse": "PASS",
            "complete_bilinear_basis_pairs": 4,
            "exhaustive_bounded_input_pairs": checked,
            "single_prime_alias_control": "PASS",
            "missing_carry_control": "PASS",
            "kronecker_identity_and_width_control": "PASS",
        },
        "elapsed_ms": round(elapsed_ms, 3),
    }
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
