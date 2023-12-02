#!/usr/bin/env python3

import collections
import math
import logging
import pathlib

logging.basicConfig(level=logging.DEBUG, format='%(message)s')

class Group:
    def __init__(self, s):
        self.count, self.color = s.split()
        self.count = int(self.count)

    def __str__(self):
        return f'{self.count} {self.color}'


class Round:
    def __init__(self, s):
        self.groups = [Group(cubes) for cubes in s.split(', ')]
        self.max_values = collections.defaultdict(int)
        self.min_values = collections.defaultdict(int)

        # Determine max, min.
        for group in self.groups:
            current_max = self.max_values.get(group.color, group.count)
            self.max_values[group.color] = max(group.count, current_max)

            current_min = self.min_values.get(group.color, group.count)
            self.min_values[group.color] = min(group.count, current_min)

    def __str__(self):
        return ', '.join(str(group) for group in self.groups)


class Game:
    def __init__(self, s):
        game_string, rounds_string = s.split(': ')
        self.game = game_string
        _, self.game_number = game_string.split(' ')
        self.game_number = int(self.game_number)

        self.rounds = [Round(round) for round in rounds_string.split('; ')]

        self.max_values = collections.defaultdict(int)
        self.red = 0
        self.green = 0
        self.blue = 0
        for i, round in enumerate(self.rounds):
            for color, count in round.max_values.items():
                if color == 'red':
                    self.red = max(self.red, count)
                elif color == 'green':
                    self.green = max(self.green, count)
                elif color == 'blue':
                    self.blue = max(self.blue, count)

    def __str__(self):
        s = []
        s.append(self.game)
        for i, round in enumerate(self.rounds):
            s.append(f'    Round {i}: {round}')
        s.append(f'Cube Power: red: {self.red}, green: {self.green}, blue: {self.blue}')
        return '\n'.join(s)

    def cube_power(self):
        return self.red * self.green * self.blue


def debug(message):
    log = logging.getLogger('aoc')
    log.debug(message)


def part_1(data):
    data_ = [
        'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green',
        'Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue',
        'Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red',
        'Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red',
        'Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green',
    ]
    debug('== Part 1 ==')
    games = [Game(row) for row in data]

    max_values = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }
    invalid = set()

    for game in games:
        for round in game.rounds:
            for group in round.groups:
                if group.count > max_values[group.color]:
                    invalid.add(game.game_number)

    total = sum(game.game_number for game in games)
    invalid = sum(invalid)
    print(f'Part 1: {total - invalid}')


def part_2(data):
    debug('== Part 2 ==')
    _data = [
        'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green',
        'Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue',
        'Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red',
        'Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red',
        'Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green',
    ]
    games = [Game(row) for row in data]
    #for game in games:
    #    print(game)
    total = sum(game.cube_power() for game in games)
    print(f'Answer: {total}')


def main(data):
    #part_1(list(data))
    print()
    part_2(list(data))


if __name__ == '__main__':
    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00-input.txt
    with open(f'{stem}-input.txt', mode='r+') as fp:
        data = [line.strip() for line in fp.readlines()]

    main(data)
