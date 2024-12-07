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
VISITED = ':'
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

    @property
    def next_direction(self):
        return self.next_right[self.direction]


class Map:
    class OutOfBounds(Exception):
        pass

    def __init__(self, map_data):
        self.original_map_data = list(map_data)

        self.display_map = []
        self.map = []
        for row_string in map_data:
            self.map.append([s for s in row_string])
            self.display_map.append([s for s in row_string])

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

        if cell_in_front in (EMPTY, VISITED):
            # Move the guard.
            # Make the current cell empty.
            self.map[self.guard.coord.y][self.guard.coord.x] = VISITED
            # Update the guard.
            self.guard.coord = coord_in_front
            # Make the new cell the guard.
            guard_on_map = {
                UP: '^',
                DOWN: 'v',
                LEFT: '<',
                RIGHT: '>',
            }
            self.map[self.guard.coord.y][self.guard.coord.x] = guard_on_map[self.guard.direction]

        elif cell_in_front == WALL:
            # Turn right.
            self.guard.turn_right()

        else:
            raise ValueError(f'Invalid cell in front: {cell_in_front}')

    def cell_in_front(self):
        coord_in_front = self.guard.get_coord_in_front()
        if self.coord_on_map(coord_in_front):
            cell_in_front = self.map[coord_in_front.y][coord_in_front.x]
            return cell_in_front

    def next_cell_out_of_bounds(self):
        coord_in_front = self.guard.get_coord_in_front()
        return not self.coord_on_map(coord_in_front)

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
        # just put a letter into a set to indicate a direction the cell has seen.

        loop_count = 0

        def look_right(guard):
            direction = guard.next_direction
            coord = guard.coord

            if direction == UP:
                cells = reversed(range(0, coord.y+1))
                for y in cells:
                    cell_coord = (coord.x, y)
                    map_cell = self.map[cell_coord[1]][cell_coord[0]]
                    for ghost_guard in moves[cell_coord]:
                        if ghost_guard.direction == UP:
                            distance = abs(coord.y - y)
                            print(f'  Looking {direction} from {coord}')
                            print(f'    Loop {distance} cells away: {cell_coord}.')
                            return True

            elif direction == DOWN:
                cells = range(coord.y, len(self.map))
                for y in cells:
                    cell_coord = (coord.x, y)
                    for ghost_guard in moves[cell_coord]:
                        if ghost_guard.direction == DOWN:
                            distance = abs(coord.y - y)
                            print(f'  Looking {direction} from {coord}')
                            print(f'    Loop {distance} cells away: {cell_coord}.')
                            return True

            elif direction == LEFT:
                pass
                cells = reversed(range(0, coord.x+1))
                for x in cells:
                    cell_coord = (x, coord.y)
                    for ghost_guard in moves[cell_coord]:
                        if ghost_guard.direction == LEFT:
                            distance = abs(coord.x - x)
                            print(f'  Looking {direction} from {coord}')
                            print(f'    Loop {distance} cells away: {cell_coord}.')
                            return True

            elif direction == RIGHT:
                cells = range(coord.x, len(self.map))
                for x in cells:
                    cell_coord = (x, coord.y)
                    for ghost_guard in moves[cell_coord]:
                        if ghost_guard.direction == RIGHT:
                            distance = abs(coord.x - x)
                            print(f'  Looking {direction} from {coord}')
                            print(f'    Loop {distance} cells away: {cell_coord}.')
                            return True

            else:
                raise ValueError(f'Invalid direction: {direction}')

            return False

        try:
            while True:
                # this may not move the guard, might be an issue?
                current_coord = self.guard.coord.as_tuple()

                self.move()
                # If we turn, don't re-check.
                if current_coord == self.guard.coord.as_tuple():
                    print('WALL!')
                    self.print_area()
                    continue

                if self.next_cell_out_of_bounds():
                    raise self.OutOfBounds(f'About to walk off map: {self.guard.get_coord_in_front()}')

                print(self.guard)

                # # Check if we crossed a path that leads to a loop.
                # ghost_guards = moves[self.guard.coord.as_tuple()]

                # if ghost_guards:
                #     print(f'  Crossed a path, been here {len(ghost_guards)} times.')

                # for ghost_guard in ghost_guards:
                #     if ghost_guard.direction == next_direction:
                #         print('    Loop detected!')
                #         loop_count += 1

                # Look to the right, see if there are any ghost guards that are facing
                # in the same direction, that will lead to a loop.
                if look_right(self.guard):
                    loop_count += 1

                moves[self.guard.coord.as_tuple()].append(self.guard.copy())

        except self.OutOfBounds as e:
            print(e)

        print(f'Loop: {loop_count}')
        print(f'Moves: {len(moves)}')

    def print_area(self):
        # print a 10x10 area around the guard.
        max_xy = len(self.map) - 1
        distance = 30

        x = self.guard.coord.x
        y = self.guard.coord.y
        left = max(0, x - distance)
        right = min(max_xy, x + distance)
        if left == 0:
            right = distance * 2
        if right == max_xy:
            left = max_xy - (distance * 2)

        top = max(0, y - distance)
        bottom = min(max_xy, y + distance)
        if top == 0:
            bottom = (distance * 2)
        if bottom == max_xy:
            top = max_xy - (distance * 2)

        print('Map:')
        for y in range(top, bottom+1):
            row = self.map[y][left:right+1]
            print(''.join(row))


if __name__ == '__main__':
    data = load_data()
    _data = [
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
