#!/usr/bin/env python3

import collections
import math
import logging
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


class Pattern:
    def __init__(self, s, reverse=False):
        self.row = s
        self.values = list(map(int, s.split()))
        if reverse:
            self.values.reverse()
        self.steps = []

    def __str__(self):
        s = ' '.join(str(n) for n in self.values)
        return s

    def analyze(self):
        all_zeros = False

        self.steps.append(self.values)

        while not all_zeros:
            previous_step = self.steps[-1]
            deltas = [
                previous_step[i+1] - previous_step[i]
                for i in range(0, len(previous_step)-1)
            ]
            self.steps.append(deltas)
            if not any(deltas):
                # all zeros, break
                break

        print(f'Steps to 0')
        for row in self.steps:
            print(row)

        # get next number.
        self.steps.reverse()
        for i, step in enumerate(self.steps[1:], start=1):
            next_number = self.steps[i-1][-1] + step[-1]
            step.append(next_number)

        print('Next number added.')
        self.steps.reverse()
        for row in self.steps:
            print(row)

        return self.steps[0][-1]

    def analyze_left(self):
        all_zeros = False

        self.steps.append(self.values)

        while not all_zeros:
            previous_step = self.steps[-1]
            deltas = [
                previous_step[i+1] - previous_step[i]
                for i in range(0, len(previous_step)-1)
            ]
            self.steps.append(deltas)
            if not any(deltas):
                # all zeros, break
                break

        print(f'Steps to 0')
        for row in self.steps:
            print(row)

        # get next number.
        self.steps.reverse()
        for i, step in enumerate(self.steps[1:], start=1):
            next_number = self.steps[i-1][-1] + step[-1]
            step.append(next_number)

        print('Next number added.')
        self.steps.reverse()
        for row in self.steps:
            print(row)

        return self.steps[0][-1]

def part_1(data):
    p('== Part 1 ==')

    patterns = [Pattern(row) for row in data]
    answers = [pattern.analyze() for pattern in patterns]
    answer = sum(answers)
    print('Answer', answer)


def part_2(data):
    p('== Part 2 ==')
    patterns = [Pattern(row, reverse=True) for row in data]
    answers = [pattern.analyze() for pattern in patterns]
    answer = sum(answers)
    print('Answer', answer)
    pass


def main(data):
    _data = [
        '0 3 6 9 12 15',
        '1 3 6 10 15 21',
        '10 13 16 21 30 45',
    ]
    #part_1(data)
    part_2(data)


if __name__ == '__main__':
    data = load_data()
    main(data)
