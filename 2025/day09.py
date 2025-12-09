#!/usr/bin/env python

import collections
import itertools
import logging
import math
import pathlib

import rich
from rich.progress import track

# Cheating?
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


def part_1(tiles):
    rich.print('[bold red]== Part 1 ==[/bold red]')
    rich.print('Find the largest rectangle.')

    rects = list(Rect(a, b) for a, b in itertools.combinations(tiles, 2))
    rects.sort(key=lambda r: r.area, reverse=True)
    # for rect in rects:
    #     rich.print(rect)

    rich.print(f'Found {len(rects)} rectangles.')
    rich.print(f'Largest rectangle: {rects[0]}')


def part_2(tiles):
    rich.print('[bold red]== Part 2 ==[/bold red]')
    rich.print('Find the largest triangle with green & red tiles.')

    # Build a polygon from our tiles.
    points = [shapely.Point(tile.x, tile.y) for tile in tiles]
    polygon = shapely.Polygon(points + [points[0]])
    print(f'Polygon area: {polygon.area}')

    rects = list(Rect(a, b) for a, b in itertools.combinations(tiles, 2))
    rects.sort(key=lambda r: r.area, reverse=True)

    for rect in rects:
        # .contains allows for edge overlap.
        if polygon.contains(rect.polygon):
            rich.print(f'Found box within polygon with area: {rect.area}')
            # Stop at the first (largest) one.
            break


class Rect:
    def __init__(self, a, b, build_polygon=False):
        self.a = a
        self.b = b
        self.width = abs(a.x - b.x) + 1
        self.height = abs(a.y - b.y) + 1
        self.area = self.width * self.height

        x_min = min(self.a.x, self.b.x)
        x_max = max(self.a.x, self.b.x)
        y_min = min(self.a.y, self.b.y)
        y_max = max(self.a.y, self.b.y)
        self.corners = [
            Tile(f'{x_min},{y_min}'),  # top left
            Tile(f'{x_min},{y_max}'),  # top right
            Tile(f'{x_max},{y_min}'),  # bottom left
            Tile(f'{x_max},{y_max}'),  # bottom right
        ]

        self._polygon = None

    def __repr__(self):
        return f'Rect({self.a}, {self.b}): {self.width} x {self.height} = {self.area}'

    @property
    def polygon(self):
        # This is somewhat expensive, so do it on demand.
        if self._polygon is None:
            min_x = min(self.a.x, self.b.x)
            max_x = max(self.a.x, self.b.x)
            min_y = min(self.a.y, self.b.y)
            max_y = max(self.a.y, self.b.y)
            top_left = shapely.Point(min_x, min_y)
            bottom_left = shapely.Point(max_x, min_y)
            top_right = shapely.Point(min_x, max_y)
            bottom_right = shapely.Point(max_x, max_y)
            self._polygon = shapely.Polygon([top_left, bottom_left, bottom_right, top_right, top_left])
        return self._polygon


class Tile:
    def __init__(self, s, color='red'):
        x, y = map(int, s.split(','))
        self.x = x
        self.y = y
        self.color = color

    def __repr__(self):
        return f'{self.color.title()} Tile({self.x}, {self.y})'


def main(data):
    _data = [
        '7,1',
        '11,1',
        '11,7',
        '9,7',
        '9,5',
        '2,5',
        '2,3',
        '7,3',
    ]

    tiles = [Tile(s) for s in data]
    part_1(tiles)
    part_2(tiles)


if __name__ == '__main__':
    data = load_data()
    main(data)
