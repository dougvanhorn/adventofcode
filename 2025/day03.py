#!/usr/bin/env python

import collections
import dataclasses
import logging
import math
import pathlib


logging.basicConfig(level=logging.DEBUG, format='%(message)s')

@dataclasses.dataclass
class Battery:
    joltage: int
    index: int


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


def part_1(batteries):
    p('== Part 1 ==')
    # Find the largest number x in 0..n-1.
    # Find the largest number y in x_i..n.

    bank_joltages = []

    for bank in batteries:
        # Process each row twice.
        print('Bank: ', bank)

        max_battery = None
        max_joltage = 0
        max_index = -1
        # find the maximum joltage battery, excluding the last one.
        for battery in bank[:-1]:
            if battery.joltage > max_joltage:
                max_battery = battery
                max_joltage = battery.joltage
                max_index = battery.index

            # Quit early if we found the max possible.
            if max_joltage == 9:
                break

        print(f'  Max joltage: {max_joltage} at index {max_index}')

        # Find the next largest joltage battery after the max.
        next_max_battery = None
        next_max_joltage = 0
        next_max_index = -1
        for battery in bank[max_index + 1:]:
            if battery.joltage > next_max_joltage:
                next_max_battery = battery
                next_max_joltage = battery.joltage
                next_max_index = battery.index

            # Quit early if we found the max possible.
            if next_max_joltage == 9:
                break

        print(f'  Next max joltage: {next_max_joltage} at index {next_max_index}')

        bank_joltage = int(f'{max_joltage}{next_max_joltage}')
        print(f'  Joltage for Bank: {bank_joltage}')
        bank_joltages.append(bank_joltage)

    total_joltage = sum(bank_joltages)
    print(f'Total joltage: {total_joltage}')


def part_2(batteries):
    p('== Part 2 ==')
    def find_max_battery(bank, start_index, length):
        # Find max joltage in bank[start_index:end_index]
        bank_length = len(bank)
        end_index = bank_length - length
        # print(f'Slice: [{start_index}:{end_index}], length {length}')

        max_battery = bank[start_index]
        for battery in bank[start_index + 1:end_index]:
            if battery.joltage > max_battery.joltage:
                max_battery = battery
        return max_battery

    max_joltages = []
    for bank in batteries:
        joltages = []
        # print('Bank: ' + ''.join(str(b.joltage) for b in bank))
        # Decreasing length, e.g., leave 11 after, leave 10 after, ...
        last_index = 0
        for length in range(11, -1, -1):  # right end slice -11..-1
            battery = find_max_battery(bank, last_index, length)
            joltages.append(battery)
            # Move to the next battery.
            last_index = battery.index + 1

        # print('Joltage: ' + ''.join(str(b.joltage) for b in joltages))
        # print()
        max_joltages.append(int(''.join(str(b.joltage) for b in joltages)))

    print('Max joltages per bank: ', max_joltages)
    total = sum(max_joltages)
    print(f'Total joltage: {total}')
    # print('Correct? ' + str(total == 3121910778619))


def main(data):
    _data = [
        '987654321111111',
        '811111111111119',
        '234234234234278',
        '818181911112111',
    ]
    batteries = []
    for row in data:
        bank = [Battery(int(n), i) for i, n in enumerate(row)]
        batteries.append(bank)

    # part_1(batteries)
    part_2(batteries)


if __name__ == '__main__':
    data = load_data()
    main(data)
