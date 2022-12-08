#!/usr/bin/env python3

import collections
import math
import pprint
import re
import traceback

import aoc


# https://adventofcode.com/2021/day/2


def main():
    # Part 2
    command_lines = aoc.loadfile('02.txt')

    depth = 0
    forward = 0
    aim = 0
    for command_line in command_lines:
        command, value = command_line.split()
        value = int(value)
        if command == 'forward':
            forward += value
            depth += (aim * value)
        elif command == 'down':
            aim += value
        elif command == 'up':
            aim -= value

    print(f'depth:   {depth}')
    print(f'forward: {forward}')
    print(f'aim:     {aim}')
    print(f'output:  {depth * forward}')


def main_part_1():
    command_lines = aoc.loadfile('02.txt')

    depth = 0
    forward = 0
    for command_line in command_lines:
        command, value = command_line.split()
        value = int(value)
        if command == 'forward':
            forward += value
        elif command == 'down':
            depth += value
        elif command == 'up':
            depth -= value

    print(f'depth: {depth}')
    print(f'forward: {forward}')
    print(f'output: {depth * forward}')


if __name__ == '__main__':
    main()
