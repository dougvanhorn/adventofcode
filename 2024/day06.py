#!/usr/bin/env python3

import collections
import logging
import math
import pathlib


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


def part_1(data):
    p('== Part 1 ==')
    map = Map(data)
    map.part_1()


def part_2(data):
    p('== Part 2 ==')
    map = Map(data)
    map.part_2()


def main(data):
    # part_1(data)
    part_2(data)



EMPTY = '.'
WALL = '#'
GUARD = '^'
# Directions
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x},{self.y})'

    def as_tuple(self):
        return (self.x, self.y)


class Guard:
    def __init__(self, coord, direction):
        self.coord = coord
        self.direction = direction

        self.next_right = {
            UP: RIGHT,
            RIGHT: DOWN,
            DOWN: LEFT,
            LEFT: UP,
        }

    def __str__(self):
        return f'Guard: {self.coord}, {self.direction}'

    def copy(self):
        return Guard(Coord(self.coord.x, self.coord.y), self.direction)

    def get_coord_in_front(self):
        if self.direction == UP:
            return Coord(self.coord.x, self.coord.y - 1)
        elif self.direction == DOWN:
            return Coord(self.coord.x, self.coord.y + 1)
        elif self.direction == LEFT:
            return Coord(self.coord.x - 1, self.coord.y)
        elif self.direction == RIGHT:
            return Coord(self.coord.x + 1, self.coord.y)
        else:
            raise ValueError(f'Invalid direction: {self.direction}')

    def turn_right(self):
        # Always turn right.
        self.direction = self.next_right[self.direction]



class Map:
    class OutOfBounds(Exception):
        pass

    def __init__(self, map_data):
        self.original_map_data = list(map_data)

        self.map = []
        for row_string in map_data:
            self.map.append([s for s in row_string])

        self.guard = None

        for y, row in enumerate(self.map):
            if GUARD in row:
                self.guard = Guard(
                    Coord(row.index(GUARD), y),
                    UP,
                )
                break

    def coord_on_map(self, coord):
        return (
            0 <= coord.y < len(self.map)
            and 0 <= coord.x < len(self.map[0])
        )

    def move(self):
        # Move the guard.
        # Get the cell in front of the guard.
        coord_in_front = self.guard.get_coord_in_front()

        if not self.coord_on_map(coord_in_front):
            raise self.OutOfBounds(f'Next cell is out of bounds: {coord_in_front}')

        cell_in_front = self.map[coord_in_front.y][coord_in_front.x]

        if cell_in_front == EMPTY:
            # Move the guard.
            # Make the current cell empty.
            self.map[self.guard.coord.y][self.guard.coord.x] = EMPTY
            # Update the guard.
            self.guard.coord = coord_in_front
            # Make the new cell the guard.
            self.map[self.guard.coord.y][self.guard.coord.x] = GUARD

        elif cell_in_front == WALL:
            # Turn right.
            self.guard.turn_right()

        else:
            raise ValueError(f'Invalid cell in front: {cell_in_front}')


    def part_1(self):
        print('Part 1')
        print('------')
        print(f'Map Summary:')
        print(f'  Size: {len(self.map[0])}x{len(self.map)}')
        print(f'  Guard: {self.guard}')

        moves = set()
        moves.add(self.guard.coord.as_tuple())

        try:
            while True:
                self.move()
                moves.add(self.guard.coord.as_tuple())

        except self.OutOfBounds as e:
            pass

        print(f'Answer: {len(moves)}')


    def part_2(self):
        # Every time we cross a path that is heading to the right of our current direction,
        # we can put a wall in front of us to cause a loop.

        # this doesn't work as we can add blocks at non-path crossing points as well.

        NEXT_DIRECTION = {
            UP: RIGHT,
            RIGHT: DOWN,
            DOWN: LEFT,
            LEFT: UP,
        }

        # Keep track of the moves with the state of the guard.
        # That will let us know if we cross a path that leads to a loop.
        moves = collections.defaultdict(list)
        moves[self.guard.coord.as_tuple()].append(self.guard.copy())

        loop_count = 0

        try:
            while True:
                # this may not move the guard, might be an issue?
                current_coord = self.guard.coord.as_tuple()

                self.move()
                # If we turn, don't re-check.
                if current_coord == self.guard.coord.as_tuple():
                    continue

                print(self.guard)
                next_direction = NEXT_DIRECTION[self.guard.direction]

                # Check if we crossed a path that leads to a loop.
                crossed_paths = moves[self.guard.coord.as_tuple()]

                for ghost_guard in crossed_paths:
                    print(f'  Checking ghost guard: {ghost_guard} against {next_direction}')
                    if ghost_guard.direction == next_direction:
                        print('    Loop detected!')
                        loop_count += 1

                moves[self.guard.coord.as_tuple()].append(self.guard.copy())

        except self.OutOfBounds as e:
            pass

        print(f'Loop: {loop_count}')
        print(f'Moves: {len(moves)}')



if __name__ == '__main__':
    data = load_data()
    data = [
        '....#.....',
        '.........#',
        '..........',
        '..#.......',
        '.......#..',
        '..........',
        '.#..^.....',
        '........#.',
        '#.........',
        '......#...',
    ]
    main(data)
