#!/usr/bin/env python3

import collections
import math
import pathlib
import pprint
import re
import traceback

import aoc


# https://adventofcode.com/2021/day/9

class Point:
    def __init__(self, row, col, height):
        self.row = row
        self.col = col
        self.coords = (self.row, self.col)
        self.height = height

    def __str__(self):
        return f'({self.row}, {self.col}): {self.height}'

    def __repr__(self):
        return self.__str__()

    def adjacent_coords(self):
        coords = [
            (self.row - 1, self.col),
            (self.row + 1, self.col),
            (self.row, self.col - 1),
            (self.row, self.col + 1),
        ]
        return coords


class Basin:
    def __init__(self, point):
        self.point = point
        self.neighbors = []

    def __str__(self):
        return f'{self.point}: {self.size}'

    def __repr__(self):
        return self.__str__()

    @property
    def size(self):
        return len(self.neighbors)


class Map:
    def __init__(self, lines):
        self.lines = lines
        self.floor = []
        self.point_dict = {}
        for row, line in enumerate(lines):
            row = [Point(row, col, int(height)) for col, height in enumerate(line)]
            for point in row:
                self.point_dict[point.coords] = point
            self.floor.append(row)

        self.MAX_ROW = len(self.floor) - 1
        self.MAX_COL = len(self.floor[0]) - 1

    def all_points(self):
        """Convenience generator to loop over all points.
        """
        for row in self.floor:
            for point in row:
                yield point

    def low_points(self):
        """Loop over all points, see if it's the low point.
        """
        low_points = []
        for local_point in self.all_points():
            neighbors = self.get_neighbors(local_point)
            lower_neighbors = [
                adjacent_point for adjacent_point in neighbors
                if adjacent_point.height <= local_point.height
            ]
            # Local minimum if no lower neighbors
            if not lower_neighbors:
                low_points.append(local_point)
        return low_points

    def get_neighbors(self, local_point):
        """Return valid adjacent coords.
        """
        neighbors = []
        coords = local_point.adjacent_coords()
        for row, col in coords:
            if row < 0 or self.MAX_ROW < row:
                continue
            if col < 0 or self.MAX_COL < col:
                continue
            neighbors.append(self.point_dict[(row, col)])
        return neighbors

    def get_basin(self, low_point):
        basin = Basin(low_point)
        visited = {}

        def search(point):
            # Mark current point as visited.
            visited[point.coords] = point

            # everything adjacent point that's hi
            adjacent_points = self.get_neighbors(point)

            all_points = [point]
            for adjacent_point in adjacent_points:
                # skip if we've visited this point
                if adjacent_point.coords in visited:
                    continue

                # skip if we've hit a peak
                if adjacent_point.height == 9:
                    continue

                additional_points = search(adjacent_point)

                # the point is within the basin, keep searching.
                all_points.extend(additional_points)

            return all_points

        basin.neighbors = search(low_point)
        return basin


def part_1(input_lines):
    seafloor = Map(input_lines)
    low_points = seafloor.low_points()
    risk_level = 0
    for point in low_points:
        print(point)
        risk_level += (point.height + 1)
    print(f'Risk Level: {risk_level}')


def part_2(input_lines):
    seafloor = Map(input_lines)
    low_points = seafloor.low_points()

    print(f'Finding {len(low_points)} basins.')
    basins = []
    for low_point in low_points:
        basin = seafloor.get_basin(low_point)
        basins.append(basin)

    print(f'basins: {basins}')
    basins.sort(key=lambda b: b.size)

    size = basins[-3].size * basins[-2].size * basins[-1].size
    print(f'Size: {size}')

    basin_points = {}
    basin_colors = [
        aoc.Colors.OKBLUE,
        aoc.Colors.OKCYAN,
        aoc.Colors.OKGREEN,
        aoc.Colors.WARNING,
        aoc.Colors.FAIL,
    ]
    for i, basin in enumerate(basins):
        color = basin_colors[i % 5]
        for point in basin.neighbors:
            basin_points[point.coords] = color

    for row in seafloor.floor:
        row_output = ''
        for point in row:
            if point.coords in basin_points:
                color = basin_points[point.coords]
                row_output += f'{aoc.Colors.BOLD}{color}{point.height}{aoc.Colors.ENDC}'
            else:
                row_output += f'{point.height}'
        print(row_output)
    print()



def main(input_lines):
    part_1(input_lines)
    print()
    print()
    part_2(input_lines)


TEST_INPUT = [
    '2199943210',
    '3987894921',
    '9856789892',
    '8767896789',
    '9899965678',
]

if __name__ == '__main__':
    path = pathlib.Path(__file__)
    day_number = path.name[3:5]
    filename = f'{day_number}.txt'
    lines = aoc.loadfile(filename)
    _lines = TEST_INPUT
    n = len(lines)
    aoc.info(f'Loaded {filename}: {n} lines.')
    main(lines)
