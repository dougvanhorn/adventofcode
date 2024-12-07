#!/usr/bin/env python3

import collections
import itertools
import logging
import math
import operator
import pathlib


logging.basicConfig(level=logging.DEBUG, format='%(message)s')


ADD = operator.add
MUL = operator.mul
CONCAT = lambda x, y: int(f'{x}{y}')


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
    answer = 0
    for test in data:
        print(test)
        if test.part_1():
            answer += test.value

    print(f'Answer: {answer}')


def part_2(data):
    p('== Part 2 ==')
    answer = 0
    print('Testing {len(data)} rows.')
    for i, test in enumerate(data):
        print(f'{i:>3} {test}')
        if test.part_2():
            answer += test.value

    print(f'Answer: {answer}')


class Test:
    def __init__(self, row):
        value, numbers = row.split(':')
        self.value = int(value)
        self.numbers = [int(x) for x in numbers.split()]
        self.positions = list(range(len(self.numbers) - 1))


    def __str__(self):
        return f'Test: {self.value}:{self.numbers}, Positions: {self.positions}'


    def part_1(self):
        operations = list(itertools.product([ADD, MUL], repeat=len(self.positions)))

        for operator_list in operations:
            # print(f'  Tessting {operator_list}')
            result = self.numbers[0]
            steps = list(zip(self.numbers[1:], operator_list))
            for number, op in steps:
                result = op(result, number)
            if result == self.value:
                return True

    def part_2(self):
        operators = [ADD, MUL, CONCAT]
        operations = list(itertools.product(operators, repeat=len(self.positions)))

        for operator_list in operations:
            # print(f'  Testing {operator_list}')
            result = self.numbers[0]
            steps = list(zip(self.numbers[1:], operator_list))
            for number, op in steps:
                result = op(result, number)
                if result > self.value:
                    # Once we exceed our value, we can stop looking at this set of operators
                    break

            if result == self.value:
                # print('    FOUND')
                return True



def main(data):
    test_data = [
        Test(row)
        for row in data
    ]

    # part_1(test_data)
    part_2(test_data)


if __name__ == '__main__':
    data = load_data()
    _data = [
        '190: 10 19',
        '3267: 81 40 27',
        '83: 17 5',
        '156: 15 6',
        '7290: 6 8 6 15',
        '161011: 16 10 13',
        '192: 17 8 14',
        '21037: 9 7 18 13',
        '292: 11 6 16 20',
    ]
    main(data)
