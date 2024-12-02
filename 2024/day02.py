#!/usr/bin/env python3

import collections
import itertools
import logging
import math
import operator
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


def part_1(data):
    p('== Part 1 ==')
    # find safe levels
    # either increasing or decreasing
    # steps of 1 to 3.
    reports = data

    safe_report_count = 0
    for report in reports:
        # Make two-tuples
        tuples = zip(report, report[1:])
        deltas = list(itertools.starmap(operator.sub, tuples))
        # p(f'Report: {report}')
        # p(f'Deltas: {deltas}')

        is_positive = bool(deltas[0] > 0)
        is_safe = True
        if is_positive:
            for delta in deltas:
                if delta not in (1, 2, 3):
                    # p(f'Not safe: {delta}')
                    is_safe = False

        else:
            for delta in deltas:
                if delta not in (-1, -2, -3):
                    # p(f'Not safe: {delta}')
                    is_safe = False

        if is_safe:
            safe_report_count += 1

    p(f'Safe reports: {safe_report_count}')

def part_2(data):
    p('== Part 2 ==')
    reports = data

    safe_report_count = 0
    for report in reports:

        # Make two-tuples
        tuples = zip(report, report[1:])
        deltas = list(itertools.starmap(operator.sub, tuples))
        p(f'Report: {report}')
        p(f'Deltas: {deltas}')

        # Allow for 1 unsafe level.
        SAFE_LEVEL = len(deltas) - 1
        p(f'Safe level: {SAFE_LEVEL}')

        is_positive = bool(deltas[0] > 0)
        if is_positive:
            safe_count = 0
            for delta in deltas:
                if delta in (1, 2, 3):
                    safe_count += 1

            p(f'Safe count: {safe_count}')
            if safe_count >= SAFE_LEVEL:
                safe_report_count += 1

        else:
            safe_count = 0
            for delta in deltas:
                if delta in (-1, -2, -3):
                    safe_count += 1

            p(f'Safe count: {safe_count}')
            if safe_count >= SAFE_LEVEL:
                safe_report_count += 1

    p(f'Safe reports: {safe_report_count}')


def main(_data):
    reports = []
    for report in _data:
        levels = [int(x) for x in report.split()]
        reports.append(levels)

    # part_1(reports)
    part_2(reports)


if __name__ == '__main__':
    data = load_data()
    data = [
        '7 6 4 2 1',
        '1 2 7 8 9',
        '9 7 6 2 1',
        '1 3 2 4 5',
        '8 6 4 4 1',
        '1 3 6 7 9',
    ]
    main(data)
