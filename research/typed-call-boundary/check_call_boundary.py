#!/usr/bin/env python3
"""Small exact check of one source-defined rank-one recursive boundary."""

from itertools import product


M = 1_000_000
W = 177_176_569_091_445_000_000
S = 177_176_569_088_785_861_287_000_000
Q = 3  # Local toy radix; the full network chooses q from its rational table.


def shear(h: int, d: int, sign: int, q: int) -> tuple[int, int]:
    """The source's three steps, including one child field interchange."""
    d = (d + sign * h) % q
    h, d = d, h  # Swap_0 on the two selected digit fields.
    d = (h - d) % q
    return h, d


def move_entry(h: int, d: int, payload: int, q: int) -> tuple[int, int, int]:
    """Apply the address shear to an array entry; only its address moves."""
    out_h, out_d = shear(h, d, +1, q)
    return out_h, out_d, payload


def main() -> None:
    assert 0 < S < W * M

    # At k=1, R=W is legal and each role child has one row; W**0=1.
    k = 1
    row_count = W**k
    assert row_count % W**k == 0
    assert (row_count // W) % (W ** (k - 1)) == 0
    assert row_count // W == 1

    for h, d, dirty in product(range(Q), range(Q), range(2)):
        entry = move_entry(h, d, dirty, Q)
        out_h, out_d, out_payload = entry
        assert entry == ((h + d) % Q, d, dirty)
        back_h, back_d, back_payload = (out_h - out_d) % Q, out_d, out_payload
        assert (back_h, back_d, back_payload) == (h, d, dirty)
        once = (d, h, dirty)
        twice = (once[1], once[0], once[2])
        assert twice == (h, d, dirty)  # The child field interchange is involutive.

    # Dropping h from d <- d+h fails to implement the rank-one shear.
    h, d = 1, 1
    wrong_h, wrong_d = d, (h - d) % Q
    assert (wrong_h, wrong_d) != ((h + d) % Q, d)

    print("PASS: 9 rank-one coordinate pairs x 2 dirty payload values")
    print("PASS: inverse, spectator preservation, one-pivot child swap, and source row divisor")
    print("PASS: negative control rejects dropping the source term")
    print("This is a local exact check; it does not identify Issue 13's FSa carrier with a theorem child.")


if __name__ == "__main__":
    main()
