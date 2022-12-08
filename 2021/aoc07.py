#!/usr/bin/env python3

import collections
import math
import pprint
import re
import statistics
import time
import traceback

import aoc


# https://adventofcode.com/2021/day/7

Point = collections.namedtuple('Point', ['n', 'cost'])


def main(numbers):
    start_1 = time.perf_counter()
    numbers.sort()
    number_counts = collections.defaultdict(int)
    for n in numbers:
        number_counts[n] += 1

    print('numbers:', numbers)
    print('number count:', len(numbers))
    print('-'*79)

    middle_index = int(len(numbers) / 2) - 1
    middle_position = numbers[middle_index]

    def _sum_part_2(position):
        print('='*79)
        for index, n in enumerate(numbers):
            if n >= position:
                break
        print(f'summing numbers split on index {index}')
        left = numbers[0:index+1]
        right = numbers[index:]
        sum_left = 0
        print('...summing left')
        for n in left:
            delta = position - n
            fuel_cost = sum(range(1, delta+1))
            print(f'{n} is {delta} away from {position}, with a fuel cost of {fuel_cost}.')
            sum_left += fuel_cost
        print(f'left: {sum_left}')

        sum_right = 0
        print('...summing right')
        for n in right:
            delta = n - position
            fuel_cost = sum(range(1, delta+1))
            print(f'{n} is {delta} away from {position}, with a fuel cost of {fuel_cost}.')
            sum_right += fuel_cost
        print(f'right: {sum_right}')
        print('-'*79)

        return (sum_left, sum_right)

    def _sum_part_1(position):
        for index, n in enumerate(numbers):
            if n >= position:
                break
        print('='*79)

        left = numbers[0:index+1]
        right = numbers[index:]
        print(f'Position: {position}, Index: {index}\nSumming {left}, {right}')

        sum_left = 0
        for n in left:
            sum_left += position - n

        sum_right = 0
        for n in right:
            sum_right += n - position

        print(f'left: {sum_left}, right: {sum_right}')
        print('-'*79)
        return (sum_left, sum_right)

    _sum = _sum_part_2

    sum_left, sum_right = _sum(middle_position)

    fuel_cost = sum_left + sum_right
    print('initial fuel_cost', fuel_cost)

    while True:
        if sum_left > sum_right:
            middle_position -= 1

        elif sum_left < sum_right:
            middle_position += 1

        else:
            print('Perfectly Balanced.')
            break

        sum_left, sum_right = _sum(middle_position)
        new_fuel_cost = sum_left + sum_right
        print('position:', middle_position)
        print('sum_left', sum_left)
        print('sum_right', sum_right)
        print('fuel_cost', fuel_cost)
        print('new_fuel_cost', new_fuel_cost)
        print('-'*79)

        if new_fuel_cost > fuel_cost:
            break

        fuel_cost = new_fuel_cost

    end_1 = time.perf_counter()
    print('=== WINNER ===')
    print('position:', middle_position)
    print('sum_left', sum_left)
    print('sum_right', sum_right)
    print('fuel_cost', fuel_cost)
    print('time:', end_1 - start_1)


def brute_force(numbers):
    numbers.sort()

    def simple_fuel(a, b):
        return abs(a - b)

    def complex_fuel(a, b):
        delta = abs(a - b)
        return int((delta * (delta + 1)) / 2)

    part_1_fuel = sum(numbers)
    start_1 = time.perf_counter()
    for position in range(numbers[0], numbers[-1]+1):
        fuel = sum([simple_fuel(n, position) for n in numbers])
        part_1_fuel = min(part_1_fuel, fuel)
    end_1 = time.perf_counter()

    part_2_fuel = None
    start_2 = time.perf_counter()
    for position in range(numbers[0], numbers[-1]+1):
        fuel = sum([complex_fuel(n, position) for n in numbers])
        if not part_2_fuel:
            part_2_fuel = fuel
        part_2_fuel = min(part_2_fuel, fuel)
    end_2 = time.perf_counter()

    print('Part 1:', part_1_fuel)
    print(f'        {end_1 - start_1}')
    print('Part 2:', part_2_fuel)
    print(f'        {end_2 - start_2}')



if __name__ == '__main__':
    lines = ['16,1,2,0,4,2,7,1,2,14']
    numbers = [int(n) for n in lines[0].split(',')]
    brute_force(numbers)

    lines = aoc.loadfile('07.txt')
    numbers = [int(n) for n in lines[0].split(',')]
    brute_force(numbers)
    #main(numbers)
