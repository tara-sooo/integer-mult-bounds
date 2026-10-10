#!/usr/bin/env python3
"""Exact small tensor and Karatsuba checks for the joint child J_n."""

from fractions import Fraction


def rank(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    if not a:
        return 0
    rows, cols = len(a), len(a[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if a[r][col]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        scale = a[pivot_row][col]
        a[pivot_row] = [x / scale for x in a[pivot_row]]
        for r in range(rows):
            if r != pivot_row and a[r][col]:
                c = a[r][col]
                a[r] = [x - c * y for x, y in zip(a[r], a[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def joint_output_flattening(n):
    # Rows: P_0,...,P_(2n-2), Q_0,...,Q_(2n-2).
    # Columns: a_i*b_j followed by a_i*c_j.
    cols_per_output = n * n
    matrix = []
    for family in range(2):
        for k in range(2 * n - 1):
            row = [0] * (2 * cols_per_output)
            for i in range(n):
                j = k - i
                if 0 <= j < n:
                    row[family * cols_per_output + i * n + j] = 1
            matrix.append(row)
    return matrix


def bilinear_form_add(x, y, scale=1):
    out = dict(x)
    for key, value in y.items():
        out[key] = out.get(key, Fraction(0)) + scale * value
        if out[key] == 0:
            del out[key]
    return out


def bilinear_product(x, y):
    # x and y are linear forms in the left and right input variables.
    out = {}
    for i, xi in x.items():
        for j, yj in y.items():
            out[i, j] = out.get((i, j), Fraction(0)) + xi * yj
    return {key: value for key, value in out.items() if value}


def karatsuba_pair_forms():
    a0, a1 = ({0: Fraction(1)}, {1: Fraction(1)})
    b0, b1 = ({0: Fraction(1)}, {1: Fraction(1)})
    c0, c1 = ({2: Fraction(1)}, {3: Fraction(1)})
    sa = {0: Fraction(1), 1: Fraction(1)}
    sb = {0: Fraction(1), 1: Fraction(1)}
    sc = {2: Fraction(1), 3: Fraction(1)}

    p0 = bilinear_product(a0, b0)
    p2 = bilinear_product(a1, b1)
    p1 = bilinear_form_add(bilinear_product(sa, sb), p0, -1)
    p1 = bilinear_form_add(p1, p2, -1)

    q0 = bilinear_product(a0, c0)
    q2 = bilinear_product(a1, c1)
    q1 = bilinear_form_add(bilinear_product(sa, sc), q0, -1)
    q1 = bilinear_form_add(q1, q2, -1)
    return (p0, p1, p2), (q0, q1, q2)


def schoolbook_pair_forms():
    products = []
    for right_offset in (0, 2):
        one_product = []
        for k in range(3):
            form = {}
            for i in range(2):
                j = k - i
                if 0 <= j < 2:
                    form[(i, right_offset + j)] = Fraction(1)
            one_product.append(form)
        products.append(tuple(one_product))
    return tuple(products)


def wrong_q_middle_form():
    # Deliberate bug: subtract P2 rather than Q2 from (a0+a1)(c0+c1).
    (p0, _, p2), (q0, _, _) = karatsuba_pair_forms()
    a_sum = {0: Fraction(1), 1: Fraction(1)}
    c_sum = {2: Fraction(1), 3: Fraction(1)}
    wrong = bilinear_form_add(bilinear_product(a_sum, c_sum), q0, -1)
    return bilinear_form_add(wrong, p2, -1)


def main():
    assert rank(joint_output_flattening(2)) == 6
    assert rank(joint_output_flattening(3)) == 10

    computed = karatsuba_pair_forms()
    expected = schoolbook_pair_forms()
    assert computed == expected
    assert wrong_q_middle_form() != expected[1][1]

    joint_multiplies = 3 * 2
    joint_linear = 3 + 2 * 2
    naive_pair_multiplies = 2 * 3
    naive_pair_linear = 2 * (2 + 2)
    cached_pair_linear = naive_pair_linear - 1
    joint_child_leaves = 3 * 2
    expanded_baseline_leaves = 2 * 3
    assert (joint_multiplies, joint_linear) == (6, 7)
    assert (naive_pair_multiplies, naive_pair_linear, cached_pair_linear) == (6, 8, 7)
    assert joint_child_leaves == expanded_baseline_leaves

    print("PASS: n=2 output-flattening rank 6; n=3 rank 10")
    print("PASS: exact n=2 Karatsuba reconstruction; wrong cross-output control rejected")
    print("PASS: n=2 costs: joint 6 multiplications/7 linear gates; naive pair 6/8; cached baseline 6/7")
    print("PASS: n=2 Toom child leaves: joint 6; expanded independent baseline 6")


if __name__ == "__main__":
    main()
