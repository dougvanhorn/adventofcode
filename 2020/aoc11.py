#!/usr/bin/env python3

import collections
import math
import pprint
import re
import traceback

import aoc

TEST = [
    'L.LL.LL.LL',
    'LLLLLLL.LL',
    'L.L.L..L..',
    'LLLL.LL.LL',
    'L.LL.LL.LL',
    'L.LLLLL.LL',
    '..L.L.....',
    'LLLLLLLLLL',
    'L.LLLLLL.L',
    'L.LLLLL.LL',
]


class Seat:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state

    def __str__(self):
        return self.state

    def __repr__(self):
        return f'({self.x}, {self.y}): {self.state}'


class Seating:
    def __init__(self, data):
        self.rows = []
        for y, line in enumerate(data):
            row = []
            self.rows.append(row)
            for x, state in enumerate(line):
                seat = Seat(x, y, state)
                row.append(seat)

    def __str__(self):
        output = []
        for i, row in enumerate(self.rows):
            s = f'{i:0>3}: '
            for seat in row:
                s += str(seat)
            output.append(s)
        return '\n'.join(output)

    def get_next_seat(self, seat):
        # Return 2-tuple, Seat, boolean indicating changed.
        occupied = 0
        for y in range(seat.y - 1, seat.y + 2):
            for x in range(seat.x - 1, seat.x + 2):
                if x < 0 or y < 0:
                    continue
                try:
                    if self.rows[y][x].state == '#':
                        occupied += 1
                except Exception:
                    pass

        if seat.state == 'L' and occupied == 0:
            return Seat(seat.x, seat.y, '#'), True

        elif seat.state == '#' and occupied >= 4:
            return Seat(seat.x, seat.y, 'L'), True

        else:
            return seat, False
        
    def run(self):
        changed = False

        new_rows = []
        for y, line in enumerate(self.rows):
            row = []
            new_rows.append(row)
            for x, seat in enumerate(line):
                new_seat, seat_changed = self.get_next_seat(seat)
                changed |= seat_changed
                row.append(new_seat)

        self.rows = new_rows

        return changed


def main():
    data = aoc.loadfile('11.txt')
    seats = [list(line) for line in data]
    #seats = [list(line) for line in TEST]
    ROWS = len(seats)
    COLS = len(seats[0])

    for i, row in enumerate(seats):
        print(f'{i:0>3}: ' + ''.join(row))

    neighbors = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    next_seats = [['.' for col in row] for row in seats]

    round = 1
    while True:
        changed = False
        for row in range(ROWS):
            for col in range(COLS):
                for dy, dx in neighbors:
                    occupied = [
                        seats[row + dy][col + dx] == '#'
                        for dy, dx in neighbors
                        if (0 <= row + dy < ROWS) and (0 <= col + dx < COLS)
                    ]
                    num_occupied = sum(occupied)
                    if seats[row][col] == 'L' and num_occupied == 0:
                        next_seats[row][col] = '#'
                        changed = True
                    elif seats[row][col] == '#' and num_occupied >= 4:
                        next_seats[row][col] = 'L'
                        changed = True
                    else:
                        next_seats[row][col] = seats[row][col]

        if not changed:
            break

        print(f'=== ROUND {round} ===')
        for i, row in enumerate(next_seats):
            print(f'{i:0>3}: ' + ''.join(row))
        print()
        round += 1

        seats = [list(row) for row in next_seats]

    occupied = 0
    for row in seats:
        for seat in row:
            if seat == '#':
                occupied += 1

    #occupied = sum([sum([seat == '#' for seat in row]) for row in seats])

    print(f'Part 1: {occupied}')


if __name__ == '__main__':
    main()
