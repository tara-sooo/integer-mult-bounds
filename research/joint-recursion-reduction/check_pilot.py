#!/usr/bin/env python3
"""Exact n=4 bilinear-tensor check for the typed Karatsuba pilot."""
import json


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def karatsuba(a, b):
    n = len(a)
    if n == 1:
        return (a[0] * b[0],)
    m = n // 2
    a0, a1 = a[:m], a[m:]
    b0, b1 = b[:m], b[m:]
    p0 = karatsuba(a0, b0)
    p2 = karatsuba(a1, b1)
    p1 = karatsuba(add(a0, a1), add(b0, b1))
    middle = sub(sub(p1, p0), p2)
    out = [0] * (2 * n - 1)
    for i, x in enumerate(p0):
        out[i] += x
    for i, x in enumerate(middle):
        out[m + i] += x
    for i, x in enumerate(p2):
        out[2 * m + i] += x
    return tuple(out)


def wrong_decoder(a, b):
    """Adverse control: omit -p2 from the middle term."""
    n = len(a)
    if n == 1:
        return (a[0] * b[0],)
    m = n // 2
    a0, a1 = a[:m], a[m:]
    b0, b1 = b[:m], b[m:]
    p0 = wrong_decoder(a0, b0)
    p2 = wrong_decoder(a1, b1)
    p1 = wrong_decoder(add(a0, a1), add(b0, b1))
    middle = sub(p1, p0)
    out = [0] * (2 * n - 1)
    for i, x in enumerate(p0):
        out[i] += x
    for i, x in enumerate(middle):
        out[m + i] += x
    for i, x in enumerate(p2):
        out[2 * m + i] += x
    return tuple(out)


def direct(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return tuple(out)


def main():
    n = 4
    checked = 0
    for i in range(n):
        for j in range(n):
            a = tuple(int(k == i) for k in range(n))
            b = tuple(int(k == j) for k in range(n))
            got = karatsuba(a, b)
            expected = tuple(int(k == i + j) for k in range(2 * n - 1))
            assert got == expected == direct(a, b), (i, j, got, expected)
            checked += 1

    a = (0, 0, 1, 0)
    b = (0, 0, 1, 0)
    correct = karatsuba(a, b)
    expected = direct(a, b)
    incorrect = wrong_decoder(a, b)
    assert correct == expected
    assert incorrect != expected

    print(json.dumps({
        "status": "PASS",
        "ring": "Z",
        "n": n,
        "bilinear_basis_pairs_checked": checked,
        "negative_control": {
            "inputs": [list(a), list(b)],
            "expected_coefficients": list(expected),
            "wrong_coefficients": list(incorrect),
            "rejected": True,
            "meaning": "omitting -p2 adds the spurious x^2 term"
        }
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
