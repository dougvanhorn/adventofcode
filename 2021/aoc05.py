#!/usr/bin/env python3

import collections
import math
import pprint
import re
import traceback

import aoc


# https://adventofcode.com/2021/day/5

Point = collections.namedtuple('Point', ['row', 'col'])


def run(lines, include_diagonal=False):
    all_lines = []
    valid_lines = []
    valid_points = collections.defaultdict(int)

    for line in lines:
        # Loop over lines and construct points
        string_1, string_2 = line.split(' -> ')
        row, col = string_1.split(',')
        point_1 = Point(int(row), int(col))
        row, col = string_2.split(',')
        point_2 = Point(int(row), int(col))

        # Consider only horizontal or vertical lines.
        # Horizontal.
        if point_1.row == point_2.row:
            # Sort them for all-points construction.
            points = [point_1, point_2]
            points.sort(key=lambda p: p.col)
            for col in range(points[0].col, points[1].col + 1):
                valid_points[point_1.row, col] += 1
            valid_lines.append(points)
        
        # Vertical.
        elif point_1.col == point_2.col:
            # Sort them for all-points construction.
            points = [point_1, point_2]
            points.sort(key=lambda p: p.row)
            for row in range(points[0].row, points[1].row + 1):
                valid_points[row, point_1.col] += 1
            valid_lines.append(points)

        elif include_diagonal:
            # determine row, col steps
            row_step = -1 if point_1.row > point_2.row else 1
            col_step = -1 if point_1.col > point_2.col else 1
            for dxdy in zip(range(point_1.row, point_2.row + row_step, row_step),
                            range(point_1.col, point_2.col + col_step, col_step)):
                valid_points[dxdy[0], dxdy[1]] += 1

            valid_lines.append([point_1, point_2])

        all_lines.append([point_1, point_2])

    dangerous_points = [point for point, vents in valid_points.items() if vents > 1]
    print(f'Valid Lines: {len(valid_lines)}')
    print(f'Vents >= 2: {len(dangerous_points)}')


def main():
    lines = aoc.loadfile('05.txt')
    run(lines, include_diagonal=True)


if __name__ == '__main__':
    main()
