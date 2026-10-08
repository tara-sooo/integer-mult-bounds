#!/usr/bin/env python3
"""FAST exact check for the pinned scalar carrier and width-529 profile row."""
from fractions import Fraction
from itertools import product
import hashlib
import json
import subprocess

BASE = 'aa7701b68540b7863d3b66a414e4319915d6282d'
HASHES = {
    'research/pair-assembly/pair_graph.py':
        '3d47e89d2649c90800a276bdd0480131def50e0bdf92c122a19494b55bf17420',
    'research/rank-pair/screen-certificate.json':
        '4aea9e9a2610f26f28872e2918c94c402bc93aa2203796af77021982e9120d8e',
    'research/rank-pair/frame-compiler.json':
        'e34d155e32b03451d3fd5b39fc39b0aefcf09bc2a8e803ab9cacf21c91ee6ba1',
}


def pinned(path):
    raw = subprocess.check_output(['git', 'show', f'{BASE}:{path}'])
    assert hashlib.sha256(raw).hexdigest() == HASHES[path], f'Pinned source changed: {path}'
    return raw


graph = pinned('research/pair-assembly/pair_graph.py').decode()
assert 'FSa, FSa2 = self.add(F, Sa), self.add(F, Sa2)' in graph
assert 'Y2 = self.add(FSa, Sb2)' in graph

cert = json.loads(pinned('research/rank-pair/screen-certificate.json'))
bit = cert['bit']
assert bit['m'] == 575 and bit['W'] == 137151806
assert bit['child_multiplicities']['529'] == 64211400
assert Fraction(bit['moment']['strict_gap']) > 0
assert Fraction(bit['excluded_above_lower']) > 1

frame = json.loads(pinned('research/rank-pair/frame-compiler.json'))
for h, roles, xors, mass, basis_vectors in (
    ('23', 27918, 149172, 642620, 31460),
    ('25', 36586, 205915, 915250, 41186),
):
    axis = frame['axes'][h]
    compiled = axis['compiled']
    replay = axis['replay']
    assert (compiled['roles'], compiled['elementary_xors'], compiled['rank_mass'],
            compiled['dirty_basis_vectors']) == (roles, xors, mass, basis_vectors)
    assert compiled['all_physical_frame_inclusions']
    assert compiled['complete_dirty_basis_both_orientations']
    assert replay['roles'] == roles and replay['rank_mass'] == mass

for f, sa, sb2, dirty in product((0, 1), repeat=4):
    x = f ^ sa
    y2 = x ^ sb2
    assert (x, y2 ^ x, dirty) == (x, sb2, dirty)
    # A child that silently drops the carried scalar is a bad conversion.
    assert (y2 == (sa ^ sb2)) == (f == 0)

print('PASS: source-derived GF(2) carrier/inverse, dirty spectator, and pinned whole-graph frame records')
print('m=575 W=137151806 n_529=64211400; accepted moment gap > 0; next-grid lower bound > 1')
print('This checks only the local scalar map and recorded certificate, not a typed recursive call.')
