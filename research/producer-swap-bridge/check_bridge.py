#!/usr/bin/env python3
"""Small exact check for the pinned producer use and missing bridge fields."""

from itertools import product
import hashlib
import json
import subprocess


BASE = 'aa7701b68540b7863d3b66a414e4319915d6282d'
HASHES = {
    'research/pair-assembly/pair_graph.py':
        '3d47e89d2649c90800a276bdd0480131def50e0bdf92c122a19494b55bf17420',
    'scripts/experiments/rank_pair_compiler.py':
        '9984aaccf880e4840402322d76678bfddb33ce7e494af78430a43429f51b85fd',
    'research/rank-pair/frame-compiler.json':
        'e34d155e32b03451d3fd5b39fc39b0aefcf09bc2a8e803ab9cacf21c91ee6ba1',
    'research/rank-pair/frame-transitions-23.json':
        'e2715ef2ff15abf43ced9a1e1b37fed8383cca9ff3e2ded3260ec5c21bfb88f3',
}


def pinned(path):
    raw = subprocess.check_output(['git', 'show', f'{BASE}:{path}'])
    assert hashlib.sha256(raw).hexdigest() == HASHES[path], f'Pinned source changed: {path}'
    return raw


graph = pinned('research/pair-assembly/pair_graph.py').decode()
assert 'FSa, FSa2 = self.add(F, Sa), self.add(F, Sa2)' in graph
assert 'Y2 = self.add(FSa, Sb2)' in graph

compiler = pinned('scripts/experiments/rank_pair_compiler.py').decode()
assert "key=(c.core[x],c.union[x])" in compiler
serializer = next(line for line in compiler.splitlines()
                  if line.lstrip().startswith('return dict(') and 'ops=ops' in line)
assert "frames=[b['frame']for b in blocks]" in serializer
assert 'nodes=' not in serializer and 'uses=' not in serializer and 'owners=' not in serializer
assert 'M_head' not in compiler and 'M_tail' not in compiler

frame = json.loads(pinned('research/rank-pair/frame-compiler.json'))
axis = frame['axes']['23']
compiled, replay = axis['compiled'], axis['replay']
assert (compiled['roles'], compiled['elementary_xors'], compiled['rank_mass']) == (27918, 149172, 642620)
assert (compiled['stats']['regions'], compiled['stats']['matched'], compiled['stats']['reclaimed'],
        compiled['stats']['clearing_xors']) == (52473, 37025, 801, 1612)
assert compiled['dirty_basis_vectors'] == 31460
assert compiled['all_physical_frame_inclusions']
assert compiled['complete_dirty_basis_both_orientations']
assert replay['word_length'] == 621482 and replay['status'].endswith('PASS')

transitions = json.loads(pinned('research/rank-pair/frame-transitions-23.json'))
assert (transitions['distinct_transitions'], transitions['singles'], transitions['rank_mass']) == (138003, 15939, 642620)
assert transitions['transition_events_equal_independent_xor_word_reconstruction']

# The local scalar carrier is an involutive GF(2) shear; a dirty spectator is fixed.
for f, sa, sb2, dirty in product((0, 1), repeat=4):
    x = f ^ sa
    y2 = x ^ sb2
    assert (x, y2 ^ x, dirty) == (x, sb2, dirty)

# Dropping the carried FSa term is not a valid conversion at F=1.
f, sa, sb2 = 1, 0, 0
assert (f ^ sa) ^ sb2 != sa ^ sb2

print('PASS: pinned FSa -> Y2 scalar shear, inverse, dirty spectator, and dropped-carrier negative control')
print('PASS: pinned h=23 whole-word checks and aggregate physical costs')
print('CONFIRMED GAP: serializer has no source node/use ID or rational address-frame matrices')
print('No selected A_e, rank_Q(A_e), pivot, Swap child, or per-use physical charge is established.')
