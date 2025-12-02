#!/usr/bin/env python

import collections
import logging
import math
import pathlib


logging.basicConfig(level=logging.DEBUG, format='%(message)s')

class Range:
    def __init__(self, range_string):
        self.start, self.end = map(int, range_string.split('-'))

    def is_repeat_part2(self, n):
        s = str(n)
        length = len(s)

        # Repeats can be any length, so find all factors, not including n.
        group_sizes = []
        for size in range(1, (length // 2) + 1):
            if length % size == 0:
                group_sizes.append(size)

        # print(f'{s}: sizes: {group_sizes}')

        for size in group_sizes:
            groups = [s[i:i+size] for i in range(0, length, size)]
            # print(f'  Groups of size {size}: {groups}')

            # Check all groups, fast fail on first non-match.
            all_match = True
            for group in groups[1:]:
                # print(f'    Comparing group: {group} to {groups[0]}')
                if groups[0] != group:
                    # print('      No match.')
                    all_match = False
                    break

            if all_match:
                # print(f'  Found repeat with group size {size}: {groups[0]}')
                # We don't care if there are multiple, just return True.
                return True

    def is_repeat(self, n):
        s = str(n)
        length = len(s)

        # If odd length, we can't repeat.
        if length % 2 != 0:
            return None

        half = length // 2

        first_half = s[:half]
        second_half = s[-half:]
        # second_half_reversed = second_half[::-1]

        is_repeat = (first_half == second_half)
        # print(f'{s}: {first_half} == {second_half}? {is_repeat}')

        if is_repeat:
            return n
        else:
            return None

    def repeats(self):
        found = []
        for n in range(self.start, self.end + 1):
            if self.is_repeat_part2(n):
                found.append(n)

        return found


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


def part_1(ranges):
    p('== Part 1 ==')
    all_repeats = []
    for range in ranges:
        found = range.repeats()
        all_repeats.extend(found)

    print('Repeats: ', all_repeats)
    print('Sum: ', sum(all_repeats))


def part_2(ranges):
    p('== Part 2 ==')
    all_repeats = []
    for range in ranges:
        found = range.repeats()
        all_repeats.extend(found)

    print('Repeats: ', all_repeats)
    print('Sum: ', sum(all_repeats))


def main(data):
    data = data[0]
    _data = (
        '11-22,95-115,998-1012,1188511880-1188511890,'
        '222220-222224,1698522-1698528,446443-446449,'
        '38593856-38593862,565653-565659,'
        '824824821-824824827,2121212118-2121212124'
    )
    ranges = [Range(r) for r in data.split(',')]
    # part_1(ranges)
    part_2(ranges)


if __name__ == '__main__':
    data = load_data()
    main(data)
