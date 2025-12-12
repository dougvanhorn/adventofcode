#!/usr/bin/env python

import collections
import logging
import math
import pathlib

import rich
import shapely


logging.basicConfig(level=logging.DEBUG, format='%(message)s')
log = logging.getLogger('aoc')


def load_data():
    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00-input.txt
    with open(f'{stem}-input.txt', mode='r+') as fp:
        data = [line.strip('\n') for line in fp.readlines()]
    return data


def part_1(presents, areas):
    rich.print('[bold red]== Part 1 ==[/bold red]')
    rich.print('Determine if the presents fit.')

    never_fit = []
    might_fit = []
    definitely_fit = []
    for area in areas:
        naive_space = (area.present_count * 9)
        print(f'Naive 3x3 space needed for presents: {area.present_count} * 9: {naive_space}')
        print('  Area size:', area.size)

        # Raw area of presents.
        raw_space = sum(
            presents[present_id].area * quantity
            for present_id, quantity in area.presents.items()
        )
        if raw_space > area.size:
            print(f'    Too many presents: {raw_space} > {area.size}')
            never_fit.append(area)

        elif naive_space > area.size:
            print('    Presents do NOT naive fit!')
            might_fit.append(area)

        elif naive_space <= area.size:
            print('    Presents DO naive fit!')
            definitely_fit.append(area)

    rich.print(f'[bold green]Answer Part 1:[/bold green]')
    rich.print(f'  Definitely fit: {len(definitely_fit)}')
    rich.print(f'  Might fit:      {len(might_fit)}')
    rich.print(f'  Never fit:      {len(never_fit)}')


def part_2(data):
    rich.print('[bold red]== Part 2 ==[/bold red]')
    rich.print('description')
    pass


class Present:
    def __init__(self, id, layout):
        # All presents are 3x3.
        self.id = id
        self.layout = layout

        # define a polygon for this present.
        # All presents are 3x3 cells, so coords are 4x4.
        # we'll draw from the bottom left at origin.

        # Move the pen around the edges of the present.

        pen = [0, 0]

        def _lower_left():
            # Find the lowest, leftmost cell.
            for y, row in enumerate(layout[::-1]):
                for x, cell in enumerate(row):
                    if cell == '#':
                        pen = [x, y]
                        return pen

        lower_left = _lower_left()


        def oob(y, x):
            # print(f'  oob? ({y}, {x})', x<0, x>2, y<0, y>2)
            return x < 0 or x > 2 or y < 0 or y > 2

        edges = set()
        # find the edges of the cell (where they don't touch neighbors)
        for y, row in enumerate(layout):
            for x, cell in enumerate(row):
                to_add = set()
                if cell == '#':
                    # Check each of the 4 directions for neighbors.
                    # up
                    ny, nx = y-1, x
                    if oob(ny, nx) or layout[ny][nx] != '#':
                        to_add.add(((y, x), (y, x+1)))

                    # right
                    ny, nx = y, x+1
                    if oob(ny, nx) or layout[ny][nx] != '#':
                        to_add.add(((y, x+1), (y+1, x+1)))

                    # down
                    ny, nx = y+1, x
                    if oob(ny, nx) or layout[ny][nx] != '#':
                        to_add.add(((y+1, x), (y+1, x+1)))

                    # left
                    ny, nx = y, x-1
                    if oob(ny, nx) or layout[ny][nx] != '#':
                        to_add.add(((y, x), (y+1, x)))

                edges |= to_add

        # With shapely we can now take the edges (LineString) and assemble a polygon.
        line_strings = [
            shapely.geometry.LineString(list(edge))
            for edge in edges
        ]
        gemo_collection = shapely.polygonize(line_strings)
        self.polygon = gemo_collection.geoms[0]

        self.area = int(self.polygon.area)

    def info(self):
        print('Present:')
        print('\n'.join(self.layout))
        print('  Area: ', self.polygon.area)

    def rotate(self):
        self.layout = [''.join(row) for row in zip(*self.layout[::-1])]

    def flip(self):
        self.layout = [row[::-1] for row in self.layout]


class Area:
    def __init__(self, area_definition):
        self.area_definition = area_definition
        dims, present_ids = area_definition.split(':')

        self.width, self.height = [int(x) for x in dims.strip().split('x')]
        self.size = self.width * self.height

        self.presents = {
            present_id: int(quantity)
            for present_id, quantity in enumerate(present_ids.strip().split(' '))
            if quantity != '0'
        }
        self.present_count = sum(self.presents.values())

    def __repr__(self):
        return f'Area({self.width}x{self.height}, presents={self.presents})'


def main(data):
    _data = [
        '0:',
        '###',
        '##.',
        '##.',
        '',
        '1:',
        '###',
        '##.',
        '.##',
        '',
        '2:',
        '.##',
        '###',
        '##.',
        '',
        '3:',
        '##.',
        '###',
        '##.',
        '',
        '4:',
        '###',
        '#..',
        '###',
        '',
        '5:',
        '###',
        '.#.',
        '###',
        '',
        '4x4: 0 0 0 0 2 0',
        '12x5: 1 0 1 0 2 2',
        '12x5: 1 0 1 0 3 2',
    ]

    # We have 6 presents, so we know where to get data.
    presents = []
    for i in range(6):
        row_start = i * 5
        present_id = int(data[row_start].strip(':'))
        layout = data[row_start + 1:row_start + 4]
        present = Present(present_id, layout)
        presents.append(present)

    areas = [
        Area(area_def)
        for area_def in data[30:]
    ]

    part_1(presents, areas)
    # part_2(presents, areas)


if __name__ == '__main__':
    data = load_data()
    main(data)
