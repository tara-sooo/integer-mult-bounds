#!/usr/bin/env python3
"""Exact p=5 local algebra and h=10 three-stage handoff checks.

Apache-2.0. Prepared with substantial OpenAI Codex assistance.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations
import hashlib
import json
from pathlib import Path
import sys

H = 10
PAIR_COUNT = 5
HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise AssertionError(message)


def intersection(a, b):
    return len(set(a) & set(b))


def pair_key(port):
    return tuple(sorted(i // 2 for i in port))


def zero(bit):
    return 0 if bit else Q(0)


def add(a, b, bit):
    return (a + b) % 2 if bit else a + b


def sub(a, b, bit):
    return (a - b) % 2 if bit else a - b


def make_ports():
    full = list(combinations(range(H), 3))
    local = [s for s in full if len(set(i // 2 for i in s)) == 3]
    cubes = {}
    for s in local:
        cubes.setdefault(pair_key(s), []).append(s)
    need(len(full) == 120, "full triple type has 120 ports")
    need(len(local) == 80, "p=5 selector block has 80 ports")
    need(len(full) - len(local) == 40, "40 repeated-pair triples are outside the local block")
    need(len(cubes) == 10 and all(len(c) == 8 for c in cubes.values()), "ten complete eight-selector cubes")
    need(len({s for c in cubes.values() for s in c}) == 80, "cube ports are distinct")
    return full, local, cubes


def verify_pair_cube(local, cubes):
    cube_of = {s: k for k, ports in cubes.items() for s in ports}
    b = {}
    bb = {}
    k = {}
    hmat = {}
    nonzero_k = nonzero_h = 0
    for s in local:
        for t in local:
            r = intersection(s, t)
            key = (s, t)
            b[key] = Q(r - 1, 2)
            bb[key] = b[key] if cube_of[s] == cube_of[t] else Q(0)
            k[key] = Q(int(s == t)) - bb[key]
            hmat[key] = bb[key] - b[key]
            need(k[key] + hmat[key] + b[key] == int(s == t), "K+H+B=I on all 80 ports")
            if s != t and k[key] != 0:
                nonzero_k += 1
                need(r % 2 == 0, "nonzero K support is binary-orthogonal")
            if s != t and hmat[key] != 0:
                nonzero_h += 1
                need(r % 2 == 0, "nonzero H support is binary-orthogonal")

    for ports in cubes.values():
        local_k = [[k[(s, t)] for t in ports] for s in ports]
        for i in range(8):
            for j in range(8):
                value = sum(local_k[i][u] * local_k[u][j] for u in range(8))
                need(value == int(i == j), "each complete cube has K^2=I")

    for s in local:
        for t in local:
            r = intersection(s, t)
            star_b = sum((Q(1, 2) if i in s and i in t else Q(0)) for i in range(H))
            star_b -= sum((Q(1, 6) if i in t else Q(0)) for i in range(H))
            need(star_b == b[(s, t)], "coordinate-star centers reproduce B=(|S∩T|-1)/2")

    return {"cubes": len(cubes), "ports": len(local), "K_nonzero_offdiagonal": nonzero_k,
            "H_nonzero_offdiagonal": nonzero_h, "K_plus_H_plus_B": True, "K_squared": True}


def operator_edges(ports, bit):
    edges = []
    n = len(ports)
    central = [[zero(bit) for _ in range(n)] for _ in range(n)]
    for si, s in enumerate(ports):
        for ti, t in enumerate(ports):
            r = intersection(s, t)
            if bit:
                central[si][ti] = r % 2
                if si != ti and r == 1:
                    edges.append((si, ti, 1))
            else:
                central[si][ti] = Q(r - 1, 2)
                if si != ti and r % 2 == 0:
                    edges.append((si, ti, -central[si][ti]))

    for si, s in enumerate(ports):
        for ti, t in enumerate(ports):
            r = intersection(s, t)
            if bit:
                side = int(si != ti and r == 1)
                need((side + central[si][ti]) % 2 == int(si == ti), "F2 side-plus-center identity")
            else:
                side = -central[si][ti] if si != ti and r % 2 == 0 else Q(0)
                need(side + central[si][ti] == int(si == ti), "dyadic side-plus-center identity")

    # Recompute the central path through the source's coordinate-star factors.
    for si, s in enumerate(ports):
        for ti, t in enumerate(ports):
            if bit:
                rg = sum(1 for i in s if i in t) % 2
                need(rg == central[si][ti], "F2 gather/scatter factors")
            else:
                rg = sum((Q(1, 2) if i in s and i in t else Q(0)) for i in range(H))
                rg -= sum((Q(1, 6) if i in t else Q(0)) for i in range(H))
                need(rg == central[si][ti], "dyadic gather/scatter factors")
    return edges


def gather(x, ports, bit, sign=1):
    c = [zero(bit) for _ in range(H + (0 if bit else 1))]
    for ti, t in enumerate(ports):
        for i in t:
            c[i] = add(c[i], sign * x[ti], bit)
        if not bit:
            c[-1] = add(c[-1], sign * x[ti], bit)
    return c


def scatter(c, ports, bit):
    y = [zero(bit) for _ in ports]
    for si, s in enumerate(ports):
        if bit:
            y[si] = sum(c[i] for i in s) % 2
        else:
            y[si] = (sum(c[i] for i in s) - c[-1]) / 2
    return y


def side_apply(a, ports, edges, bit):
    y = [zero(bit) for _ in ports]
    for q, (si, _ti, coeff) in enumerate(edges):
        y[si] = add(y[si], coeff * a[q], bit)
    return y


def apply_one(x, y, a, c, ports, edges, bit, sign=1, stop_before_cleanup=False):
    """Run one complete forward shear or its exact time reverse."""
    x, y, a, c = list(x), list(y), list(a), list(c)
    if sign == 1:
        old_side, old_center = side_apply(a, ports, edges, bit), scatter(c, ports, bit)
        y = [sub(v, old_side[i], bit) for i, v in enumerate(y)]
        y = [sub(v, old_center[i], bit) for i, v in enumerate(y)]
        for q, (_si, ti, _coeff) in enumerate(edges):
            a[q] = add(a[q], x[ti], bit)
        gx = gather(x, ports, bit)
        c = [add(c[i], gx[i], bit) for i in range(len(c))]
        new_center, new_side = scatter(c, ports, bit), side_apply(a, ports, edges, bit)
        y = [add(v, new_center[i], bit) for i, v in enumerate(y)]
        y = [add(v, new_side[i], bit) for i, v in enumerate(y)]
        if not stop_before_cleanup:
            c = [sub(c[i], gx[i], bit) for i in range(len(c))]
            for q, (_si, ti, _coeff) in enumerate(edges):
                a[q] = sub(a[q], x[ti], bit)
    elif sign == -1:
        # Reverse rows 7 through 0 of the pinned eight-row schedule.
        for q, (_si, ti, _coeff) in enumerate(edges):
            a[q] = add(a[q], x[ti], bit)
        gx = gather(x, ports, bit)
        c = [add(c[i], gx[i], bit) for i in range(len(c))]
        new_side, new_center = side_apply(a, ports, edges, bit), scatter(c, ports, bit)
        y = [sub(v, new_side[i], bit) for i, v in enumerate(y)]
        y = [sub(v, new_center[i], bit) for i, v in enumerate(y)]
        c = [sub(c[i], gx[i], bit) for i in range(len(c))]
        for q, (_si, ti, _coeff) in enumerate(edges):
            a[q] = sub(a[q], x[ti], bit)
        old_center, old_side = scatter(c, ports, bit), side_apply(a, ports, edges, bit)
        y = [add(v, old_center[i], bit) for i, v in enumerate(y)]
        y = [add(v, old_side[i], bit) for i, v in enumerate(y)]
    else:
        raise ValueError("sign must be +1 or -1")
    return x, y, a, c


def pattern(n, bit, salt=0):
    if bit:
        return [((i + salt) * 7 + 3) % 2 for i in range(n)]
    return [Q(((i + salt) % 9) - 4, 7) for i in range(n)]


def check_dirty_shears(local, bit):
    edges = operator_edges(local, bit)
    center_n = H + (0 if bit else 1)
    a0 = pattern(len(edges), bit, 3)
    c0 = pattern(center_n, bit, 5)
    y0 = pattern(len(local), bit, 2)
    zero_vec = [zero(bit) for _ in local]
    for sign in (1, -1):
        for q in range(len(local)):
            x = [zero(bit) for _ in local]
            x[q] = 1 if bit else Q(1)
            xx, yy, aa, cc = apply_one(x, y0, a0, c0, local, edges, bit, sign)
            target = [add(y0[i], sign * x[i], bit) for i in range(len(local))]
            need(xx == x and yy == target and aa == a0 and cc == c0,
                 "exact one-shear action and arbitrary-dirty restoration")
        xx, yy, aa, cc = apply_one(zero_vec, y0, a0, c0, local, edges, bit, sign)
        need(yy == y0 and aa == a0 and cc == c0, "dirty-only control")
    return edges


def check_exchange(ports, bit):
    # The exact one-shear matrix is already checked on every ordered port pair.
    # Compose its three data actions on each basis vector of both banks.
    n = len(ports)
    for side in (0, 1):
        for q in range(n):
            x, y = [zero(bit) for _ in ports], [zero(bit) for _ in ports]
            (x if side == 0 else y)[q] = 1 if bit else Q(1)
            y1 = [add(y[i], x[i], bit) for i in range(n)]
            x2 = [sub(x[i], y1[i], bit) for i in range(n)]
            y3 = [add(y1[i], x2[i], bit) for i in range(n)]
            expected_x = y if bit else [-v for v in y]
            expected_y = x
            if bit:
                expected_x = list(y)
            need(x2 == expected_x and y3 == expected_y, "three completed stages give exact signed exchange")
    return True


def check_interstage_controls(local, bit, edges):
    # Stage 1 is deliberately stopped before its cleanup. Stage 2 changes X,
    # so late stage-1 cleanup reads the wrong source and strands dirty state.
    q = 0
    x0 = [zero(bit) for _ in local]
    y0 = [zero(bit) for _ in local]
    x0[q] = 1 if bit else Q(1)
    a0 = [zero(bit) for _ in edges]
    c0 = [zero(bit) for _ in range(H + (0 if bit else 1))]
    _x, y1, a1, c1 = apply_one(x0, y0, a0, c0, local, edges, bit, 1, True)
    x2 = [sub(x0[i], y1[i], bit) for i in range(len(local))]
    gx2 = gather(x2, local, bit)
    c_late = [sub(c1[i], gx2[i], bit) for i in range(len(c1))]
    a_late = list(a1)
    for e, (_si, ti, _coeff) in enumerate(edges):
        a_late[e] = sub(a_late[e], x2[ti], bit)
    need(y1[q] == (1 if bit else Q(1)) and x2[q] == 0, "stage-2 witness reads stage-1 output")
    need(a_late != a0 and c_late != c0, "interleaving stage 2 before stage-1 cleanup breaks dirty restoration")

    # A second control drops stage-1's final inverse copy while keeping the
    # ordinary stage order; one source value remains in its private side bank.
    _x, _y, a_bad, c_bad = apply_one(x0, y0, a0, c0, local, edges, bit, 1, True)
    need(a_bad != a0 or c_bad != c0, "omitted cleanup leaves dirty scratch")

    if not bit:
        # Using + instead of the required inverse - at stage 2 changes the endpoint.
        x = [Q(0) for _ in local]
        y = [Q(0) for _ in local]
        y[q] = Q(1)
        y1 = y
        x_wrong = [x[i] + y1[i] for i in range(len(local))]
        y_wrong = [y1[i] + x_wrong[i] for i in range(len(local))]
        need(y_wrong[q] == 2 and y_wrong != x, "wrong stage-2 sign fails signed endpoint")
    return True


def neighbor_degree(ports, bit):
    degrees = [sum(1 for t in ports if t != s and
                   ((intersection(s, t) == 1) if bit else (intersection(s, t) % 2 == 0)))
               for s in ports]
    need(len(set(degrees)) == 1, "local and full neighbor degrees are regular")
    return degrees[0]


def rank_histogram(v, z, centers):
    """Count every Section 3 bit edge rank using its residual table."""
    n = v ** 3
    per_stage_invocations = v ** 2
    hist = Counter()

    def charge(rank, count):
        if rank:
            hist[rank] += count

    for j in (1, 2, 3):
        a = H ** (j - 1)
        f = H ** (3 - j)
        charge((a - 1) * (H - 1), 2 * n)  # X in->2 and Y 0->1
        charge(H - 1, 2 * n)             # X 2->3 and Y 4->5

        side_roles = per_stage_invocations * v * z
        center_roles = per_stage_invocations * centers
        for rank in (a - 1, (a - 1) * (H - 1) + 1, H - 2, 1,
                     a * H * (f - 1)):
            charge(rank, side_roles)
        for rank in ((a - 1) * H, H, H, H, a * H * (f - 1)):
            charge(rank, center_roles)

    charge(1, n)  # X-source sign: rank(2 P_U)=1 per X data role
    stock = 2 * n + 3 * per_stage_invocations * (v * z + centers)
    loss = 3 * per_stage_invocations * centers * H
    paid = sum(r * count for r, count in hist.items())
    formula = stock * H ** 3 - n + 2 * loss
    need(paid == formula, "all edge ranks reproduce the Section 3/4 paid-rank identity")
    data = Counter({1: n, 9: 6 * n, 81: 2 * n, 891: 2 * n})
    need(all(hist[r] >= count for r, count in data.items()), "data child ranks are a submultiset")
    auxiliary = hist - data
    need(sum(r * count for r, count in auxiliary.items()) + sum(r * count for r, count in data.items()) == paid,
         "data and auxiliary paid ranks partition the ledger")
    return {
        "N": n, "I": 3 * per_stage_invocations, "m": H ** 3,
        "W": stock, "L": loss, "s": paid, "Wm_minus_s": stock * H ** 3 - paid,
        "data_child_histogram": dict(sorted(data.items())),
        "data_rank_mass": sum(r * count for r, count in data.items()),
        "auxiliary_child_histogram": dict(sorted(auxiliary.items())),
        "auxiliary_rank_mass": sum(r * count for r, count in auxiliary.items()),
        "complete_section3_edge_histogram": dict(sorted(hist.items())),
    }


def stage_witness(local):
    s = local[0]
    address = (s, s, s)
    need(all(t in list(combinations(range(H), 3)) for t in address), "witness is in the full T^3 address set")
    x = [0] * 120
    y = [0] * 120
    ports = list(combinations(range(H), 3))
    at = {t: i for i, t in enumerate(ports)}
    x[at[s]] = 1
    y1 = [y[i] + x[i] for i in range(120)]
    x2 = [x[i] - y1[i] for i in range(120)]
    y3 = [y1[i] + x2[i] for i in range(120)]
    need(y1[at[s]] == 1 and x2[at[s]] == 0 and y3[at[s]] == 1,
         "Y from stage 1 is read by stage 2 and later remains stage 3 target")
    return {"address": address, "stage1_Y": 1, "stage2_source_Y": 1,
            "stage2_target_X_after": 0, "stage3_target_Y_before": 1,
            "stage3_Y_after": 1}


def main():
    if sys.flags.optimize:
        raise RuntimeError("run without -O so exact assertions stay enabled")
    full, local, cubes = make_ports()
    cube = verify_pair_cube(local, cubes)
    local_complex = operator_edges(local, False)
    local_bit = operator_edges(local, True)
    full_complex = operator_edges(full, False)
    full_bit = operator_edges(full, True)
    dirty = {
        "local_complex": len(check_dirty_shears(local, False)),
        "local_bit": len(check_dirty_shears(local, True)),
    }
    check_exchange(full, False)
    check_exchange(full, True)
    check_interstage_controls(local, False, local_complex)
    check_interstage_controls(local, True, local_bit)

    local_cost = rank_histogram(80, neighbor_degree(local, True), H)
    full_cost = rank_histogram(120, neighbor_degree(full, True), H)
    need(local_cost["Wm_minus_s"] < 0 and full_cost["Wm_minus_s"] < 0,
         "h=10 is not a Section 4 rank-saving supplier in either scope")
    result = {
        "status": "LEGAL_HANDOFF_BUT_NO_DATA_GAIN",
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "pins": {
            "manuscript_commit": "https://redirect.github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a",
            "issue23_commit": "https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/267c24dfa448fbf43fa68b7d2cfdd5f9580be458",
            "issue25_commit": "https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/520203231ff0de8d9c3121c924ed4fce398c8f69",
            "issue30_commit": "https://redirect.github.com/tara-sooo/integer-mult-bounds/commit/78f4a20fa1be5fb7366ae93c808a93d191491472",
            "pr193_head": "https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/187e1010ac8b259af8e9b5166f68b64bc27b4b47",
            "pr203_head": "https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/d2873e20750d0949d2ad75cbc4cd82b5b1a74e84",
            "pr207_head": "https://redirect.github.com/CrocSwap/integer-mult-bounds/commit/cd14825023b75af4f5919a30e5e6d548b6ade5bc",
        },
        "geometry": {"h": H, "p": PAIR_COUNT, "full_triples": len(full),
                      "local_selector_ports": len(local), "omitted_full_triples": len(full) - len(local),
                      "local_cubes": cube},
        "local_operator_checks": {"complex_side_center": True, "bit_side_center": True,
                                  "dirty_shears": dirty, "full120_complex_side_center": True,
                                  "full120_bit_side_center": True,
                                  "full120_signed_exchange": True},
        "actual_T3_handoff_witness": stage_witness(local),
        "local80_bit_paid_profile": local_cost,
        "full120_bit_paid_profile": full_cost,
        "conclusion": "All original data-child transitions survive unchanged; no data rank transition is removed or reduced.",
    }
    text = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if "--write-receipt" in sys.argv:
        (HERE / "receipt.json").write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
