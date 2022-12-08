#!/usr/bin/env python3

import collections
import math
import re
import traceback

import aoc


def main():
    lines = [
        28, 33, 18, 42, 31, 14, 46, 20, 48, 47,
        24, 23, 49, 45, 19, 38, 39, 11, 1, 32,
        25, 35, 8, 17, 7, 9, 4, 2, 34, 10,
        3,
    ]
    #lines = aoc.loadfile('10.txt')
    #lines = [int(line) for line in lines]

    lines.append(0)
    lines.append(max(lines) + 3)
    lines.sort()

    metadata = [('required', lines[-1])]
    for i in range(2, len(lines) + 1):
        i *= -1
        previous_num = lines[i+1]
        num = lines[i]
        diff = previous_num - num
        if diff < 3:
            metadata.append(('optional', num))
        elif diff == 3:
            metadata.append('required', num
        print(i, lines[i])

    print(metadata)

    onejolt = 0
    threejolt = 0

    for i in range(1, len(lines)):
        diff = lines[i] - lines[i-1]
        print(f'{i-1}:{i}, {lines[i]} - {lines[i-1]} = {diff}')
        if diff == 1:
            onejolt += 1
        elif diff == 3:
            threejolt += 1
        else:
            print('### Jolt', diff)

    print('1 Jolt', onejolt)
    print('3 Jolt', threejolt)
    print(onejolt * threejolt)

if __name__ == '__main__':
    main()
