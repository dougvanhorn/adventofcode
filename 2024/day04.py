#!/usr/bin/env python3

import collections
import logging
import math
import pathlib
import re


logging.basicConfig(level=logging.DEBUG, format='%(message)s')


def load_data():
    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00-input.txt
    with open(f'{stem}-input.txt', mode='r+') as fp:
        data = [line.strip() for line in fp.readlines()]
    return data


def p(message):
    log = logging.getLogger('aoc')
    log.debug(message)


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.letter = ''

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def get(self, direction):
        if direction == 'up':
            return Coord(self.x, self.y - 1)

        elif direction == 'down':
            return Coord(self.x, self.y + 1)

        elif direction == 'left':
            return Coord(self.x - 1, self.y)

        elif direction == 'right':
            return Coord(self.x + 1, self.y)

        elif direction == 'up_right':
            return Coord(self.x + 1, self.y - 1)

        elif direction == 'up_left':
            return Coord(self.x - 1, self.y - 1)

        elif direction == 'down_right':
            return Coord(self.x + 1, self.y + 1)

        elif direction == 'down_left':
            return Coord(self.x - 1, self.y + 1)

        else:
            raise ValueError(f'Invalid direction: {direction}')


class RegexPuzzle:
    def __init__(self, rows):
        size = len(rows)
        self.rows = rows
        self.left_right = list(rows)
        #print(self.left_right)

        self.up_down = []
        for col in range(len(rows[0])):
            self.up_down.append(''.join([row[col] for row in rows]))

        #print(self.up_down)

        def get_diagonals(grid, bltr = True):
            dim = len(grid)
            assert dim == len(grid[0])
            return_grid = [[] for total in range(2 * len(grid) - 1)]
            for row in range(len(grid)):
                for col in range(len(grid[row])):
                    if bltr:
                        return_grid[row + col].append(grid[col][row])
                    else:
                        return_grid[col - row + (dim - 1)].append(grid[row][col])
            return return_grid

        self.bltr = [''.join(row) for row in get_diagonals(rows, bltr=True)]
        #print(self.bltr)
        self.tlbr = [''.join(row) for row in get_diagonals(rows, bltr=False)]
        #print(self.tlbr)

    def search(self):
        count = 0
        for row in self.left_right:
            count += len(re.findall('XMAS', row))
            count += len(re.findall('SAMX', row))
        print(f'left right Count: {count}')

        for row in self.up_down:
            count += len(re.findall('XMAS', row))
            count += len(re.findall('SAMX', row))
        print(f'up down Count: {count}')

        for row in self.bltr:
            count += len(re.findall('XMAS', row))
            count += len(re.findall('SAMX', row))
        print(f'bltr Count: {count}')

        for row in self.tlbr:
            count += len(re.findall('XMAS', row))
            count += len(re.findall('SAMX', row))
        print(f'tlbr Count: {count}')



class Puzzle:
    def __init__(self, rows):
        self.rows = rows
        self.size = len(rows[0])

    def __str__(self):
        return f'Puzzle: {self.size}x{self.size}'

    def get_word(self, coord, direction, length):
        def is_valid(coord):
            # coord must be within the bounds of the puzzle.
            return (
                0 <= coord.x < self.size
                and
                0 <= coord.y < self.size
            )

        if direction not in ('up_right', 'right', 'down_right', 'down'):
            raise ValueError(f'Invalid direction: {direction}')

        coords = [coord]
        while len(coords) < length:
            coords.append(coords[-1].get(direction))

        # print(f'  Direction: {direction}, Coords: {coords}, Length: {length}')

        letters = [
            self.rows[coord.y][coord.x]
            for coord in coords
            if is_valid(coord)
        ]

        return ''.join(letters)


    def search(self, coord):
        # up_left, left, down_left, down strings.
        # We can match against XMAS, SAMX.
        count = 0
        WORDS = ('XMAS', 'SAMX')

        # print(f'Searching {coord}.')
        for direction in ('up_right', 'right', 'down_right', 'down'):
            word = self.get_word(coord, direction, 4)
            # print(f'  {direction}: {word}')
            if word in WORDS:
                count += 1

        return count

    def coords(self):
        for y in range(self.size):
            for x in range(self.size):
                yield Coord(x, y)


def part_1(rows):
    p('== Part 1 ==')
    # Word search, XMAS up down left right diagonally.
    # Puzzle is square.
    puzzle = Puzzle(rows)

    answer = 0
    for coord in puzzle.coords():
        count = puzzle.search(coord)
        answer += count

    print(f'Answer: {answer}')


class Puzzle2:
    def __init__(self, rows):
        self.rows = rows
        self.size = len(rows[0])

    def search(self):
        count = 0
        for coord in self.coords():
            if self.match(coord):
                count += 1

        print(f'Count: {count}')

    def coords(self):
        for y in range(self.size):
            for x in range(self.size):
                yield Coord(x, y)

    def match(self, coord):
        # forward
        try:
            tl = [self.rows[coord.y][coord.x], self.rows[coord.y + 1][coord.x + 1], self.rows[coord.y + 2][coord.x + 2]]
            br = [self.rows[coord.y + 2][coord.x], self.rows[coord.y + 1][coord.x + 1], self.rows[coord.y][coord.x + 2]]
        except IndexError:
            # off the grid
            return False

        tl = ''.join(tl)
        br = ''.join(br)

        if tl in ('SAM', 'MAS') and br in ('SAM', 'MAS'):
            return True

        return False


def part_2(data):
    p('== Part 2 ==')
    puzzle = Puzzle2(data)
    puzzle.search()


def main(data):
    _data = [
    ]
    # puzzle = RegexPuzzle(data)
    # puzzle.search()
    # return
    part_1(data)
    part_2(data)


if __name__ == '__main__':
    data = load_data()
    _data = [
        'MMMSXXMASM',
        'MSAMXMSMSA',
        'AMXSXMAAMM',
        'MSAMASMSMX',
        'XMASAMXAMM',
        'XXAMMXXAMA',
        'SMSMSASXSS',
        'SAXAMASAAA',
        'MAMMMXMMMM',
        'MXMXAXMASX',
    ]
    main(data)
