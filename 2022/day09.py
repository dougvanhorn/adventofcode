#!/usr/bin/env python3

import pathlib

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return str(self)

    @property
    def position(self):
        return (self.x, self.y)

    def move(self, direction):
        if direction == 'R':
            self.x += 1

        elif direction == 'L':
            self.x -= 1

        elif direction == 'U':
            self.y += 1

        elif direction == 'D':
            self.y -= 1

    def follow(self, head):
        # follow a point.

        delta_x = head.x - self.x
        delta_y = head.y - self.y

        # are they touching?
        if (delta_x in (-1, 0, 1)) and (delta_y in (-1, 0, 1)):
            return

        # Horizontal move
        if delta_y == 0:
            if delta_x < -1:
                self.x -= 1
            elif delta_x > 1:
                self.x += 1
            return

        # Vertical move
        if delta_x == 0:
            if delta_y < -1:
                self.y -= 1
            elif delta_y > 1:
                self.y += 1
            return

        # Diagonal move, move both x and y, move both x and y
        # Move X direction when not on same x-axis
        if delta_x <= -1:
            self.x -= 1
        elif delta_x >= 1:
            self.x += 1

        # Move Y direction when not on same y-axis
        if delta_y <= -1:
            self.y -= 1
        elif delta_y >= 1:
            self.y += 1


class Rope:
    def __init__(self, size=2):
        self.head = Point(0,0)
        self.knots = [Point(0, 0) for i in range(size-1)]

        # Keep track of positions the tail has been in.
        self.tail_positions = set()
        self.tail_positions.add(self.knots[-1].position)
    
    def run(self, data):
        for row in data:
            direction, steps = row.split(' ')
            steps = int(steps)

            for i in range(steps):
                self.move(direction)

    def move(self, direction):
        # Move the head
        self.head.move(direction)
        leader = self.head
        for knot in self.knots:
            knot.follow(leader)
            leader = knot

        self.tail_positions.add(self.knots[-1].position)
        #print(f'Head: {self.head}, Tail: {self.knots[-1]}')


def part_1(data):
    rope = Rope()
    rope.run(data)
    print(f'Part 1: {len(rope.tail_positions)}')


def part_2(data):
    rope = Rope(size=10)
    rope.run(data)
    print(f'Part 2: {len(rope.tail_positions)}')


def main(data):
    INPUT = [
        'R 4',
        'U 4',
        'L 3',
        'D 1',
        'R 4',
        'D 1',
        'L 5',
        'R 2',
    ]
    part_1(data)

    INPUT = [
        'R 5',
        'U 8',
        'L 8',
        'D 3',
        'R 17',
        'D 10',
        'L 25',
        'U 20',
    ]
    part_2(data)


if __name__ == '__main__':
    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00input.txt
    with open(f'{stem}input.txt', mode='r+') as fp:
        data = [line.strip() for line in fp.readlines()]

    main(data)

