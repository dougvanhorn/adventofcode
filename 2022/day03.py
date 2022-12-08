#!/usr/bin/env python3

import pathlib

# Enumerate returns an index of the iteration and the value.
# Strings behave as lists when you ask them to.
PRIORITIES = {
    char: value + 1
    for value, char
    in enumerate('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
}

def part_1(data):
    total_priority = 0

    for row in data:
        size = int(len(row) / 2)
        ruck_1 = row[:size]
        ruck_2 = row[size:]

        in_both = set(ruck_1).intersection(set(ruck_2))
        total_priority += PRIORITIES[in_both.pop()]

    print(f'Total Priority: {total_priority}')


def part_2(data):
    total_priority = 0

    #print(len(data))
    #print(list(range(0, len(data), 3)))

    # Groups of 3.
    for group_index in range(0, len(data), 3):
        rows = data[group_index:group_index + 3]
        ruck_1 = set(rows[0])
        ruck_2 = set(rows[1])
        ruck_3 = set(rows[2])
        in_all = ruck_1.intersection(ruck_2).intersection(ruck_3)
        total_priority += PRIORITIES[in_all.pop()]

    print(f'Part 2 Total Priority: {total_priority}')



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

