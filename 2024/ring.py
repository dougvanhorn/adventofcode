#!/usr/bin/env python

import random


class Ring:
    """Ring class to support rotations.
    """
    def __init__(self, width, height, numbers):
        self.width = width
        self.height = height
        self.original_numbers = numbers
        self.numbers = numbers

        # Corner indexes.
        self.top_left = 0
        self.top_right = self.width - 1
        self.bottom_right = self.top_right + self.height - 1
        self.bottom_left = self.bottom_right + self.width - 1

    def __repr__(self):
        output = []
        output.append(f'Width: {self.width}')
        output.append(f'Height: {self.height}')
        output.append(f'Top Left: {self.top_left}')
        output.append(f'Top Right: {self.top_right}')
        output.append(f'Bottom Right: {self.bottom_right}')
        output.append(f'Bottom Left: {self.bottom_left}')
        expected = self.width + self.width + self.height + self.height - 4
        output.append(f'Numbers: {len(self.numbers)}, (expected: {expected})')

        output.append(' '.join(str(x) for x in self.numbers))
        s = ''
        for i in range(0, len(self.numbers)):
            if i in (self.top_left, self.top_right, self.bottom_right, self.bottom_left):
                # print(f'{i} in {self.top_left}, {self.top_right}, {self.bottom_right}, {self.bottom_left}')
                s += f'* '
            else:
                # print(f'{i} not a corner')
                s += '  '
        output.append(s)
        return '\n'.join(output)

    def __str__(self):
        # top row
        top_row = self.numbers[self.top_left:self.top_right + 1]
        top_row_str = ''.join(str(x) for x in top_row)

        # bottom row
        bottom_row = self.numbers[self.bottom_left:self.bottom_right + 1]
        bottom_row.reverse()
        bottom_row_str = ''.join(str(x) for x in bottom_row)

        # middle rows
        # Get left side,
        left_side = self.numbers[self.bottom_right+1:]
        left_side.reverse()
        print('left side numbers:', left_side)

        # Get right side,
        right_side = self.numbers[self.top_right+1:self.bottom_right]

        middle_rows = []
        for left, right in zip(left_side, right_side):
            middle_rows.append(f'{left}{" " * (self.width - 2)}{right}')

        middle_rows_str = '\n'.join(middle_rows)

        return '\n'.join([
            top_row_str,
            middle_rows_str,
            bottom_row_str,
        ])

    def rotate(self, n):
        # rotate n positions.
        self.numbers = self.numbers[n:] + self.numbers[:n]


def main():
    width = 5
    height = 5
    numbers = range(0, (width + width + height + height - 4))
    ring = Ring(width, height, [f'{(n % 16):x}' for n in numbers])

    print(repr(ring))
    ring.rotate(4)
    print(repr(ring))
    ring.rotate(4)
    print(repr(ring))
    ring.rotate(4)
    print(repr(ring))
    ring.rotate(4)
    print(repr(ring))


if __name__ == '__main__':
    main()