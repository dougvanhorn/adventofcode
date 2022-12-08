#!/usr/bin/env python3

import collections
import math
import pprint
import re
import traceback

import aoc


# https://adventofcode.com/2021/day/-

#   0:      1:      2:      3:      4:
#  aaaa    ....    aaaa    aaaa    ....
# b    c  .    c  .    c  .    c  b    c
# b    c  .    c  .    c  .    c  b    c
#  ....    ....    dddd    dddd    dddd
# e    f  .    f  e    .  .    f  .    f
# e    f  .    f  e    .  .    f  .    f
#  gggg    ....    gggg    gggg    ....
#
#   5:      6:      7:      8:      9:
#  aaaa    aaaa    aaaa    aaaa    aaaa
# b    .  b    .  .    c  b    c  b    c
# b    .  b    .  .    c  b    c  b    c
#  dddd    dddd    ....    dddd    dddd
# .    f  e    f  .    f  e    f  .    f
# .    f  e    f  .    f  e    f  .    f
#  gggg    gggg    ....    gggg    gggg
#
# number   segments
# ------   --------
#  0        6
#  1        2
#  2        5
#  3        5
#  4        4
#  5        5
#  6        6
#  7        3
#  8        7
#  9        6
#
# segments   numbers
# --------   -------
#  2          1
#  3          7
#  4          4
#  5          2, 3, 5
#  6          0, 6, 9
#  7          8


def part_1(lines):
    count = 0
    for line in lines:
        for number in line.output:
            if len(number) in (2, 3, 4, 7):
                count += 1

    print('1, 4, 7, 8:', count)


import enum


class Length(enum.Enum):
    ONE = 2
    FOUR = 4
    SEVEN = 3
    EIGHT = 7


UNIQUE_LENGTHS = {1, 4, 7, 8}


def analysis(lines):
    for line_number, line in enumerate(lines):
        print('='*79)
        lengths = collections.defaultdict(int)
        for i, segment in enumerate(line.signals):
            lengths[len(segment)] += 1

        print(f'Line {line_number} Segment Lengths')
        print('-'*79)
        print('Length | Count')
        keys = list(lengths.keys())
        keys.sort()
        for key in keys:
            length = key
            count = lengths[key]
            print(f'   {length}   |   {count}')

        uniques = {key for key in keys if key in UNIQUE_LENGTHS}

        if len(uniques) != 4:
            print('!!!!!! LESS THAN 4 UNIQUE NUMBERS IN SIGNALS !!!!!!!')
            exit()
        print('-'*79)
        print()


def part_2(lines):
    total = 0
    for i, line in enumerate(lines):
        number = get_number(line)
        total += number
        print(f'Line {i}: {number}')

    print(f'Total: {total}')


def get_number(line):
    map = {}
    char_map = {}
    # We know we'll always have at least one of each unique.
    for signal in line.signals:
        # Find the one signal
        signal_length = len(signal)

        if signal_length == 2:
            map[1] = {c for c in signal}
            char_map[signal] = '1'

        elif signal_length == 3:
            map[7] = {c for c in signal}
            char_map[signal] = '7'

        elif signal_length == 4:
            map[4] = {c for c in signal}
            char_map[signal] = '4'

        elif signal_length == 7:
            map[8] = {c for c in signal}
            char_map[signal] = '8'

    # Second pass armed with our 4 unique numbers.
    for signal in line.signals:
        signal_length = len(signal)
        current_chars = {c for c in signal}

        # Do not map unique numbers
        if len(current_chars) in {2, 3, 4, 7}:
            continue

        # Overlap patterns are unique, create a tuple and match for this number.
        overlaps = (
            len(map[1].intersection(current_chars)),
            len(map[4].intersection(current_chars)),
            len(map[7].intersection(current_chars)),
            len(map[8].intersection(current_chars)),
        )
        # Unique map lengths.
        # 2  1:1  4:2  7:2  8:5
        # 5  1:1  4:3  7:2  8:5
        # 6  1:1  4:3  7:2  8:6
        # 3  1:2  4:3  7:3  8:5
        # 0  1:2  4:3  7:3  8:6
        # 9  1:2  4:4  7:3  8:6
        if overlaps == (1, 2, 2, 5):
            map[2] = current_chars
            char_map[signal] = '2'

        elif overlaps == (1, 3, 2, 5):
            map[5] = current_chars
            char_map[signal] = '5'

        elif overlaps == (1, 3, 2, 6):
            map[6] = current_chars
            char_map[signal] = '6'

        elif overlaps == (2, 3, 3, 5):
            map[3] = current_chars
            char_map[signal] = '3'

        elif overlaps == (2, 3, 3, 6):
            map[0] = current_chars
            char_map[signal] = '0'

        elif overlaps == (2, 4, 3, 6):
            map[9] = current_chars
            char_map[signal] = '9'

        else:
            raise Exception(f'Unexpected overlap: {overlaps}')

    numbers = []
    for output in line.output:
        chars = {c for c in output}
        for number, signal_chars in map.items():
            if chars == signal_chars:
                numbers.append(str(number))

    number_string = ''.join(numbers)
    return int(number_string)


def main(lines):
    part_2(lines)


if __name__ == '__main__':
    lines = aoc.loadfile('08.txt')
    input_lines = []
    _lines = [
        'be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe',
        'edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc',
        'fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg',
        'fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb',
        'aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea',
        'fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb',
        'dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe',
        'bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef',
        'egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb',
        'gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce',
    ]
    Input = collections.namedtuple('Input', ['signals', 'output'])

    for line in lines:
        signals, output = line.split(' | ')
        signals = signals.split()
        output = output.split()
        input_lines.append((Input(signals, output)))
    main(input_lines)
