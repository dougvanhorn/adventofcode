#!/usr/bin/env python3

import collections
import logging
import math
import pathlib
import re
import string

logging.basicConfig(level=logging.DEBUG, format='%(message)s')


def debug(message):
    log = logging.getLogger('aoc')
    log.debug(message)


def part_1(data):
    debug('== Part 1 ==')
    numbers = []
    for line in data:
        digits = [c for c in line if c in string.digits]
        number = int(f'{digits[0]}{digits[-1]}')
        numbers.append(number)

    print('Answer: ', sum(numbers))


def part_2(data):
    fp = open('output.txt', mode='w')

    word_map = {
        'oneight': '1 8    ',
        'twone': '2 1  ',
        'threeight': '3   8    ',
        'fiveight': '5  8    ',
        'sevenine': '7   9   ',
        'eightwo': '8   2  ',
        'eighthree': '8   3    ',
        'nineight': '9  8    ',
        'one': '1  ',
        'two': '2  ',
        'three': '3    ',
        'four': '4   ',
        'five': '5   ',
        'six': '6  ',
        'seven': '7    ',
        'eight': '8    ',
        'nine': '9   ',
    }
    pattern = re.compile('|'.join(word_map.keys()))

    debug('== Part 2 ==')
    numbers = []

    danger = [
        'oneight',
        'twone',
        'threeight',
        'fiveight',
        'sevenine',
        'eightwo',
        'eighthree',
        'nineight',
    ]
    danger = re.compile('|'.join(danger))

    for line in data:
        original_line = line
        show = bool(danger.search(line))
        if show:
            print('before translate: ', line)

        while match := pattern.search(line):
            word = match.group()
            digit = word_map[word]
            # if show: print(f'  {word} -> {digit}')
            if show:
                print(' '*19 + ' '*match.start() + '^'*(match.end() - match.start()))
            line = line[:match.start()] + digit + line[match.end():]
            if show:
                print(f'                   {line}')

        digits = [c for c in line if c in string.digits]
        if show:
            print('          digits: ', digits)

        number = int(f'{digits[0]}{digits[-1]}')

        if show:
            print(f'          number:  {number}')
        numbers.append(number)
        fp.write(f'{original_line}\n{line} => {number}\n\n')

    print('Answer: ', sum(numbers))


def main(data):
    #part_1(data)
    print()
    sample = [
        'two1nine',
        'eightwothree',
        'abcone2threexyz',
        'xtwone3four',
        '4nineeightseven2',
        'zoneight234',
        '7pqrstsixteen',
        # Added this to example data to make the use case clear and accurate.
        # Without this, the "correct" approach is ambiguous with the given example data.
        'zzoneightzz'
    ]
    # part_2(sample)
    part_2(data)


if __name__ == '__main__':
    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00-input.txt
    with open(f'{stem}-input.txt', mode='r+') as fp:
        data = [line.strip() for line in fp.readlines()]

    main(data)
