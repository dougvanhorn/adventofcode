#!/usr/bin/env python3

import pathlib


def main(data):
    # Hold all the calorie groups in a list.
    elf_calories = []

    total_calories = 0
    for row in data:
        #row = row.strip()
        if row:
            calories = int(row)
            total_calories += calories

        else:
            # We've hit a new group, append what we have and prep for the next group.
            elf_calories.append(total_calories)
            total_calories = 0

    # Part one, find the maximum calorie elf.
    max_calories = max(elf_calories)
    elf_index = elf_calories.index(max_calories)
    print(f'Elf {elf_index + 1} carries {max_calories}')

    # Part two, find the sum of the top three calories.
    elf_calories.sort()
    top_three_calories = sum(elf_calories[-3:])
    print(f'The top three elves carry {top_three_calories}.')


if __name__ == '__main__':
    stem = pathlib.Path(__file__).stem
    with open(f'{stem}input.txt', mode='r+') as fp:
        data = [line.strip() for line in fp.readlines()]

    main(data)

