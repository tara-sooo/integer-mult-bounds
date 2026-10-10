#!/usr/bin/env python3
"""Exact checks for the two-source center/side screen in MILESTONE3.md."""

from fractions import Fraction
from itertools import product


def dot(a, b):
    return sum(x * y for x, y in zip(a, b)) % 2


def scale(v, s):
    return tuple((x * s) % 2 for x in v)


def add(a, b):
    return tuple((x + y) % 2 for x, y in zip(a, b))


def dirty_channel(x, y, dirty, u, v):
    """Four-shear channel: y += v(u x), restoring arbitrary dirty state."""
    gathered = (dirty + dot(u, x)) % 2
    precompensated = add(y, scale(v, dirty))  # subtraction equals addition in F_2
    out = add(precompensated, scale(v, gathered))
    restored = (gathered - dot(u, x)) % 2
    return out, restored


def log_lower_ratio(m, r, terms=80):
    """Exact lower bound for ln(m/r), including negative powers of two."""
    x = Fraction(m, r)
    k = 0
    while x >= 2:
        x /= 2
        k += 1
    while x < 1:
        x *= 2
        k -= 1

    def atanh_bounds(z):
        t = (z - 1) / (z + 1)
        partial = 2 * sum(t ** (2 * j + 1) / (2 * j + 1) for j in range(terms))
        if t == 0:
            return partial, partial
        tail = 2 * abs(t) ** (2 * terms + 1) / ((2 * terms + 1) * (1 - t * t))
        return partial, partial + tail

    # For k<0, use an upper bound for ln(2) so multiplication preserves a lower bound.
    ln2_lo, ln2_hi = atanh_bounds(Fraction(2))
    x_lo, _ = atanh_bounds(x)
    return (k * ln2_lo if k >= 0 else k * ln2_hi) + x_lo


def entropy_lower(m, histogram):
    return sum(
        (count * r) * log_lower_ratio(m, r)
        for r, count in histogram.items()
        if r
    )


PROFILES = {
    "complex": {
        "m": 66,
        "W": 12052,
        "rank": 794112,
        "v": 1320,
        "full": {
            1: 87534, 2: 39834, 3: 29769, 4: 12627, 5: 5850,
            6: 4815, 7: 2118, 8: 4593, 9: 1287, 10: 2790,
            11: 1062, 12: 3591, 13: 381, 14: 2226, 15: 5637,
            16: 264, 17: 243, 18: 7959, 19: 501, 20: 66,
        },
        "data": {1: 15840, 2: 6600, 18: 7920},
    },
    "bit": {
        "m": 72,
        "W": 21108,
        "rank": 1517840,
        "v": 1760,
        "full": {
            1: 120168, 2: 64228, 3: 29616, 4: 8970, 5: 7800,
            6: 3660, 7: 3312, 8: 2802, 9: 1812, 10: 2508,
            11: 1158, 12: 4320, 13: 1590, 14: 3234, 15: 1230,
            16: 3216, 17: 1164, 18: 1332, 19: 918, 20: 5280,
            21: 11160, 22: 11952, 60: 2200,
        },
        "data": {1: 18480, 2: 6160, 20: 5280, 21: 2640, 22: 2640},
    },
}


def check_cost_profile(name, profile):
    m, W, rank = profile["m"], profile["W"], profile["rank"]
    full = profile["full"]
    assert sum(n for n in full.values()) > 0
    assert sum(r * n for r, n in full.items()) == rank
    deficit = m * W - rank
    assert deficit == (1320 if name == "complex" else 1936)

    full_c = entropy_lower(m, full)
    data = profile["data"]
    data_c = entropy_lower(m, data)
    free_center_deficit = 2 * profile["v"]
    assert deficit - full_c / 99 < 0
    assert free_center_deficit - data_c / 99 < 0
    return deficit, full_c, free_center_deficit, data_c


def check_two_port_family():
    # Every one-center source/target map v u^T has rank at most one.
    identity = ((1, 0), (0, 1))
    vectors = list(product((0, 1), repeat=2))
    for u in vectors:
        for v in vectors:
            matrix = tuple(tuple((v[i] * u[j]) % 2 for j in range(2)) for i in range(2))
            assert matrix != identity

    # A coupled, non-diagonal center/side pair reaches the lower bound exactly.
    center_u, center_v = (1, 1), (1, 0)
    side_u, side_v = (0, 1), (1, 1)
    assert tuple(
        tuple((center_v[i] * center_u[j] + side_v[i] * side_u[j]) % 2 for j in range(2))
        for i in range(2)
    ) == identity
    assert (center_u[0] * side_u[1] - center_u[1] * side_u[0]) % 2 == 1
    for x in vectors:
        for y in vectors:
            for center_dirty, side_dirty in product((0, 1), repeat=2):
                yc, dc = dirty_channel(x, y, center_dirty, center_u, center_v)
                ys, ds = dirty_channel(x, yc, side_dirty, side_u, side_v)
                assert ys == add(y, x)
                assert dc == center_dirty and ds == side_dirty

    # Adverse independent-source control: a decoder that only reads x_1 aliases x_2.
    x, y, dirty = (0, 1), (0, 0), 1
    wrong, restored = dirty_channel(x, y, dirty, (1, 0), (1, 0))
    assert wrong != add(y, x)
    assert restored == dirty

    # Exact dyadic complex coefficients satisfy the same full source/target identity.
    half = Fraction(1, 2)
    complex_center_u, complex_center_v = (1, 1), (half, half)
    complex_side_u, complex_side_v = (1, -1), (half, -half)
    complex_matrix = tuple(
        tuple(
            complex_center_v[i] * complex_center_u[j]
            + complex_side_v[i] * complex_side_u[j]
            for j in range(2)
        )
        for i in range(2)
    )
    assert complex_matrix == ((1, 0), (0, 1))
    assert complex_center_u[0] * complex_side_u[1] - complex_center_u[1] * complex_side_u[0] == -2


def main():
    check_two_port_family()
    print("two-port F_2/Z[i,1/2]: identities, one-channel exclusion, dirty restoration, adverse control PASS")
    for name, profile in PROFILES.items():
        full_d, full_c, relaxed_d, data_c = check_cost_profile(name, profile)
        print(
            f"{name}: full D={full_d}, C_lower={float(full_c):.9f}, "
            f"D-C_lower/99<={float(Fraction(full_d) - full_c / 99):.9f}; "
            f"free-center D<={relaxed_d}, data C_lower={float(data_c):.9f}, "
            f"D-C_lower/99<={float(Fraction(relaxed_d) - data_c / 99):.9f} PASS"
        )


if __name__ == "__main__":
    main()
