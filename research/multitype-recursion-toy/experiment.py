#!/usr/bin/env python3
"""Exact, small two-type moment experiment; standard library only."""

from fractions import Fraction as Q
from math import factorial, isqrt


M = 575
W = 137_151_806
SCALE = 10**24
LOG_TERMS = 32
EXP_TERMS = 8

# Complete pinned child-width histograms. Sources and hashes are in SOURCES.md.
TYPE_A = (
    (1, 1_725_399_142), (2, 83_474_797), (3, 45_979_944),
    (4, 25_771_845), (5, 20_048_226), (6, 18_832_860),
    (7, 17_285_926), (8, 13_320_151), (9, 10_863_958),
    (10, 8_899_436), (11, 8_550_388), (12, 6_150_660),
    (13, 5_359_966), (14, 3_947_398), (15, 3_264_367),
    (16, 2_045_758), (17, 9_608_825), (18, 928_096),
    (19, 299_299), (20, 282_371), (21, 16_346_100),
    (22, 97_405), (23, 72_402_275), (25, 64_793_806),
    (481, 8_146_600), (525, 64_793_806), (529, 64_211_400),
)
TYPE_B = (
    (1, 1_725_448_017), (2, 83_325_366), (3, 45_690_259),
    (4, 25_239_096), (5, 19_651_200), (6, 18_723_242),
    (7, 17_106_549), (8, 13_274_680), (9, 10_943_423),
    (10, 8_919_929), (11, 8_639_950), (12, 6_282_197),
    (13, 5_425_815), (14, 4_016_766), (15, 3_351_146),
    (16, 2_045_758), (17, 9_626_535), (18, 919_241),
    (19, 320_551), (20, 300_081), (21, 16_346_100),
    (22, 97_405), (23, 72_402_275), (25, 64_793_806),
    (481, 8_146_600), (525, 64_793_806), (529, 64_211_400),
)

SAVING_A = Q(39_859, 781_250_000)
SAVING_B = Q(2_551_509, 50_000_000_000)
SOURCE_CHECKS = {
    "A": (999_999_999_998_609_449, 999_999_999_998_609_468),
    "B": (999_999_999_996_323_840, 999_999_999_996_323_860),
}


def log_atanh(z):
    partial = sum(
        (2 * z ** (2 * j + 1) / (2 * j + 1) for j in range(LOG_TERMS)), Q()
    )
    tail = 2 * z ** (2 * LOG_TERMS + 1) / (
        (2 * LOG_TERMS + 1) * (1 - z * z)
    )
    return partial, partial + tail


LOG_2 = log_atanh(Q(1, 3))


def log_ratio_interval(x):
    """Enclose log(x) for 1 <= x <= M via exact range reduction and atanh."""
    k = 0
    reduced = x
    while reduced >= 2:
        reduced /= 2
        k += 1
    z = (reduced - 1) / (reduced + 1)
    low, high = log_atanh(z)
    return k * LOG_2[0] + low, k * LOG_2[1] + high


def exp_partial(x):
    total = term = Q(1)
    for k in range(1, EXP_TERMS + 1):
        term *= x / k
        total += term
    return total


def exp_interval(low_x, high_x):
    """Enclose exp(x); the geometric tail bound is valid for high_x < 1."""
    assert 0 <= low_x <= high_x < 1
    tail = high_x ** (EXP_TERMS + 1) / factorial(EXP_TERMS + 1)
    tail /= 1 - high_x / (EXP_TERMS + 2)
    return exp_partial(low_x), exp_partial(high_x) + tail


def moment_interval(a, hist):
    low = high = Q()
    for t, count in hist:
        log_low, log_high = log_ratio_interval(Q(M, t))
        exp_low, exp_high = exp_interval(a * log_low, a * log_high)
        weight = Q(count * t, M * W)
        low += weight * exp_low
        high += weight * exp_high
    return low, high


def outward_scaled(low, high, scale=SCALE):
    lo = low.numerator * scale // low.denominator
    hi = -((-high.numerator * scale) // high.denominator)
    return lo, hi


def sqrt_scaled_bounds(value, scale=SCALE):
    scaled_num = value.numerator * scale * scale
    denominator = value.denominator
    floor_root = isqrt(scaled_num // denominator)
    exact = floor_root * floor_root * denominator == scaled_num
    return floor_root, floor_root if exact else floor_root + 1


def two_cycle_radius(x, y, fee=Q(0)):
    """Bounds rho([[0,(1+fee)x],[(1+fee)y,0]]) on scaled intervals."""
    factor2 = (1 + fee) ** 2
    low_x, high_x = (Q(v, SCALE) for v in x)
    low_y, high_y = (Q(v, SCALE) for v in y)
    low, _ = sqrt_scaled_bounds(factor2 * low_x * low_y)
    _, high = sqrt_scaled_bounds(factor2 * high_x * high_y)
    return low, high


def show_interval(label, interval):
    print(f"{label}=[{interval[0]},{interval[1]}]/10^24")


def self_check():
    # Exact 2x2 controls: rho([[0,1/4],[1/4,0]])=1/4;
    # a 1/10 conversion fee scales that radius to 11/40.
    assert two_cycle_radius((SCALE // 4, SCALE // 4),
                            (SCALE // 4, SCALE // 4)) == (SCALE // 4, SCALE // 4)
    fee = Q(1, 10)
    expected = 11 * SCALE // 40
    assert two_cycle_radius((SCALE // 4, SCALE // 4),
                            (SCALE // 4, SCALE // 4), fee) == (expected, expected)


def main():
    self_check()
    assert SAVING_A < SAVING_B
    assert len(TYPE_A) == len(TYPE_B) == 27
    assert all(1 <= t <= 529 and n > 0 for hist in (TYPE_A, TYPE_B) for t, n in hist)
    assert sum(t * n for t, n in TYPE_A) == 78_860_441_550
    assert sum(t * n for t, n in TYPE_B) == 78_860_441_550
    assert M * W - 78_860_441_550 == 1_846_900

    own_a = moment_interval(SAVING_A, TYPE_A)
    own_b = moment_interval(SAVING_B, TYPE_B)
    for name, own in (("A", own_a), ("B", own_b)):
        cert_low, cert_high = SOURCE_CHECKS[name]
        assert own[0] >= Q(cert_low, 10**18)
        assert own[1] <= Q(cert_high, 10**18)

    a_interval = outward_scaled(*moment_interval(SAVING_A, TYPE_A))
    b_interval = outward_scaled(*moment_interval(SAVING_A, TYPE_B))
    assert a_interval[0] > b_interval[1]

    zero_fee = two_cycle_radius(a_interval, b_interval)
    tiny_fee = two_cycle_radius(a_interval, b_interval, Q(1, 10**10))
    stress_fee = two_cycle_radius(a_interval, b_interval, Q(1, 1000))
    assert zero_fee[0] > b_interval[1]
    assert tiny_fee[0] > b_interval[1]
    assert tiny_fee[1] < a_interval[0]
    assert stress_fee[0] > SCALE

    print(f"common_a={SAVING_A}")
    show_interval("M_A", a_interval)
    show_interval("M_B", b_interval)
    show_interval("rho_no_switch", a_interval)
    show_interval("rho_alternating_zero_fee", zero_fee)
    show_interval("rho_alternating_fee_1e-10", tiny_fee)
    show_interval("rho_alternating_fee_1e-3", stress_fee)
    print("controls=identical-type PASS; source-cert cross-check PASS; exact self-check PASS")
    print("result=NO_GAIN_IN_TESTED_MODEL")


if __name__ == "__main__":
    main()
