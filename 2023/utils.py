#!/usr/bin/env python3

import collections
import math
import re
import unittest


class TestUtils(unittest.TestCase):
    def test_adjacent(self):
        cells = adjacent(140, 140, (0,0), (0,0))
        self.assertEqual(len(cells), 3)
        self.assertEqual(cells, [(0, 1), (1, 0), (1, 1)])

        cells = adjacent(140, 140, (0,139), (0,139))
        self.assertEqual(len(cells), 3)
        self.assertEqual(cells, [(0, 138), (1, 138), (1, 139)])

        cells = adjacent(140, 140, (139,0), (139,0))
        self.assertEqual(len(cells), 3)
        self.assertEqual(cells, [(138, 0), (138,1), (139, 1)])

        cells = adjacent(140, 140, (139,139), (139,139))
        self.assertEqual(len(cells), 3)
        self.assertEqual(cells, [(138, 138), (138,139), (139, 138)])

        cells = adjacent(140, 140, (5, 11), (7, 20))
        self.assertEqual(len(cells), 30)
        self.assertEqual(cells[0], (4, 10))
        self.assertEqual(cells[-1], (8, 21))


def adjacent(row_length, col_length, top_left, bottom_right):
    """Return all adjacent coordinates to the given range.

    Coordinates are (row, col).

    Rows are human, 140 rows means max row 139.
    """
    #print(f'Find Adjacent Cells: top-left: {top_left}, bottom-right: {bottom_right}')
    # Inclusive on both sides.
    MIN_ROW = 0
    MAX_ROW = row_length - 1
    MIN_COL = 0
    MAX_COL = col_length - 1

    top, left = top_left
    bottom, right = bottom_right

    top_bottom_range = list(range(max(0, top), min(MAX_ROW, bottom)+1))
    left_right_range = list(range(max(0, left-1), min(MAX_COL, right+1)+1))

    #print('top_bottom', top_bottom_range)
    #print('left_right', left_right_range)

    cells = []

    # Above
    if top > 0:
        cells.extend(
            [
                (top-1, column)
                for column in left_right_range
            ]
        )
    #print(cells)

    for row in top_bottom_range:
        # Left
        if left > 0:
            cells.append((row, left-1))
        # Right
        if right < (MAX_COL-1):
            cells.append((row, right+1))
        #print(cells)

    # Below
    if bottom < MAX_ROW:
        cells.extend(
            [
                (bottom+1, column)
                for column in left_right_range
            ]
        )

    #print(cells)
    return cells



if __name__ == '__main__':
    unittest.main()