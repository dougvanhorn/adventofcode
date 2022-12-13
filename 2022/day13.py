#!/usr/bin/env python3

import collections
import logging
import math
import pathlib
import traceback


logging.basicConfig(level=logging.ERROR, format='%(message)s')
log = logging.getLogger('aoc')


def debug(message):
    log.debug(message)


Pair = collections.namedtuple('Pair', 'left right')

def both_ints(left, right):
    return isinstance(left, int) and isinstance(right, int)

def int_compare(left, right):
        if left < right:
            return -1
        if left > right:
            return 1

        return 0


def normalize(left, right):
    if isinstance(left, int):
        left = [left]

    if isinstance(right, int):
        right = [right]

    return left, right


def cmp_value(result):
    return 1 if result else 0


def compare(left, right, indent=0):
    # Use Case 1: Both integers.
    pad = '  ' * indent
    debug(f'{pad}- Compare {left} vs. {right}')
    if both_ints(left, right):
        result = int_compare(left, right)
        debug(f'{pad}- {left} ? {right} returns {result}')
        return result

    # Use Case 2: int vs. list, normalize
    retry = False
    if isinstance(left, int):
        retry = True
        left = [left]

    if isinstance(right, int):
        retry = True
        right = [right]

    if retry:
        debug(f'{pad}{pad}- Mixed types, normalize to list and retry.')
        return compare(left, right, indent=indent+1)

    # Use Case 3: list vs. list, compare
    for i in range(len(left)):
        # If the right list runs out of items first, the inputs are not in the right order.
        if i >= len(right):
            debug(f'{pad}- Right side smaller, return 1')
            return 1

        result = compare(left[i], right[i], indent=indent+1)
        if result != 0:
            return result

    # If the left list runs out of items first, the inputs are in the right order.
    if len(left) < len(right):
        debug(f'{pad}- Left side smaller, return -1')
        return -1

    # If the lists are the same length and no comparison makes a decision about the order, continue
    # checking the next part of the input.
    return 0


def part_1(data):
    pairs = []
    for i in range(0, len(data), 2):
        debug(f'lines: {len(data)}')
        debug(f'indexes: {i}, {i+1}')
        try:
            pair = Pair(eval(data[i]), eval(data[i+1]))
            pairs.append(pair)
        except:
            traceback.print_exc()
            print(f'data {i}: {data[i]}')
            print(f'data {i+1}: {data[i+1]}')
            raise

    indexes = []
    for i, pair in enumerate(pairs, start=1):
        debug(f'== Pair {i} ==')
        correct_order = compare(pair.left, pair.right)
        if correct_order == -1:
            indexes.append(i)
        else:
            continue

    print(f'Indexes: {indexes}')
    print(f'Part 1: {sum(indexes)}')


def part_2(data):
    eval_data = []
    for i in range(len(data)):
        eval_data.append(eval(data[i]))

    import functools
    eval_data.sort(key=functools.cmp_to_key(compare))
    #for row in eval_data:
    #    print(row)
    indexes = []
    for i, row in enumerate(eval_data, start=1):
        if row == [[2]] or row == [[6]]:
            indexes.append(i)

    print(f'Indexes: {indexes}')
    print(f'Part 2: {math.prod(indexes)}')


def main(data):
    INPUT = [
        '[1,1,3,1,1]',
        '[1,1,5,1,1]',

        '[[1],[2,3,4]]',
        '[[1],4]',

        '[9]',
        '[[8,7,6]]',

        '[[4,4],4,4]',
        '[[4,4],4,4,4]',

        '[7,7,7,7]',
        '[7,7,7]',

        '[]',
        '[3]',

        '[[[]]]',
        '[[]]',

        '[1,[2,[3,[4,[5,6,7]]]],8,9]',
        '[1,[2,[3,[4,[5,6,0]]]],8,9]',
    ]
    data = [row for row in data if row]
    part_1(data)
    data.append('[[2]]')
    data.append('[[6]]')
    part_2(data)


if __name__ == '__main__':
    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00input.txt
    with open(f'{stem}input.txt', mode='r+') as fp:
        data = [line.strip() for line in fp.readlines()]

    main(data)

