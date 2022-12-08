#!/usr/bin/env python3

import pathlib


def part_1(data):
    # 1000 lines.
    subsets = 0

    for row in data:
        section_1, section_2 = row.split(',')

        s1_left, s1_right = section_1.split('-')
        s2_left, s2_right = section_2.split('-')

        section_1 = set(range(int(s1_left), int(s1_right) + 1))  # range is only left inclusive
        section_2 = set(range(int(s2_left), int(s2_right) + 1))

        if section_1.issubset(section_2) or section_2.issubset(section_1):
            subsets += 1

    print(f'Part 1: {subsets}')


def part_2(data):
    # 1000 lines.
    overlap = 0

    for row in data:
        section_1, section_2 = row.split(',')

        s1_left, s1_right = section_1.split('-')
        s2_left, s2_right = section_2.split('-')

        section_1 = set(range(int(s1_left), int(s1_right) + 1))  # range is only left inclusive
        section_2 = set(range(int(s2_left), int(s2_right) + 1))

        if section_1.intersection(section_2):
            overlap += 1

    print(f'Part 2: {overlap}')



def main(data):
    part_1(data)
    part_2(data)

if __name__ == '__main__':
    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00input.txt
    with open(f'{stem}input.txt', mode='r+') as fp:
        data = [line.strip() for line in fp.readlines()]

    main(data)

