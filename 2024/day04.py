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
        lines = []
        lines.append('   0 1 2 3 4 5 6 7 8 9')
        for i, row in enumerate(self.rows):
            lines.append(f'{i}  ' + ' '.join(row))
            lines.append('')
        return '\n'.join(lines)

    def search(self, coord, direction, word):
        # If no word, return empty list, we found it.
        if word == '':
            return []

        try:
            letter = self.rows[coord.y][coord.x]
        except IndexError:
            # Return False when we go off the edge.
            return False

        if letter != word[0]:
            # Return False when we don't match.
            return False

        # At this point, the letter matches what we're looking for.
        # save it to the coord.
        coord.letter = letter

        # Get the next coord and continue searching.
        next_coord = coord.get(direction)
        result = self.search(next_coord, direction, word[1:])

        if result is False:
            # When search returns False, search failed, return False.
            return False
        else:
            # When search returns a list, search succeeded, return list with coord at end.
            return [coord] + result


def part_1(rows):
    p('== Part 1 ==')
    # Word search, XMAS up down left right diagonally.
    # Puzzle is square.
    size = len(rows)

    puzzle = Puzzle(rows)
    # print(puzzle)

    def coords(size):
        for y in range(size):
            for x in range(size):
                yield Coord(x, y)


    counter = collections.Counter()

    def fmt(tuples, word):
        # format a string of the 4 coordinates.
        # reverse the coords if the word is reversed.
        # this lets us find accidental match overlap.
        xys = [(coord.x, coord.y) for coord in tuples]
        if word == 'SAMX':
            xys.reverse()
        s = ':'.join([f'{x},{y}' for x, y in xys])
        letters = ''.join([coord.letter for coord in tuples])
        # print(s)
        # print(letters)
        if letters not in ('SAMX', 'XMAS'):
            raise ValueError(f'Invalid word: {letters}')

        return [s]

    count = 0
    for coord in coords(size):
        for direction in ('up_right', 'right', 'down_right', 'down'):
            for word in ('XMAS', 'SAMX'):
                found = puzzle.search(coord, direction, word)
                if found:
                    # print(f'Found {word} {direction}:', found)
                    counter.update(fmt(found, word))
                    count += 1

    # print(f'Counter: {counter}')
    keys = list(counter.keys())
    keys.sort()
    for key in keys:
        value = counter[key]
        print(f'{key}: {counter[key]}')

    print(f'Count: {count}')

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
    # part_1(data)
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
