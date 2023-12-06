#!/usr/bin/env python3

import collections
import math
import logging
import pathlib
import sys

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
    winners = []
    for race in data:
        wins = 0
        print(f'Race: {race}')
        for time_pressed in range(0, race.time + 1):
            distance = time_pressed * (race.time - time_pressed)
            print(f'  Pressed: {time_pressed}: {distance}')
            if distance > race.distance:
                print('  winner.')
                wins += 1
        winners.append(wins)

    print('Winners', winners)
    answer = math.prod(winners)
    print('Answer:', answer)


def part_2(race):
    p('== Part 2 ==')

    def search(span):
        if span[0] == span[1]:
            return span[0]

        if (span[0]+1) == span[1]:
            return span[1]

        if span[0] > span[1]:
            raise Exception('left is right of right.')

        middle = sum(span) // 2
        distance = middle * (race.time - middle)
        print(f'Range: {span}, pressed: {middle}, distance: {distance}')
        if distance > race.distance:
            # search lower half.
            return search((span[0], middle))
        else:
            return search((middle, span[1]))

    print(f'Time: {race.time}')
    print(f'Distance: {race.distance}')
    print(f'Middle time: {race.time // 2}')
    middle_distance = (race.time // 2) * (race.time - (race.time // 2))
    print(f'Middle distance: {middle_distance}')

    lower = search((0, race.time // 2))
    print(f'Lower: {lower}')
    for pressed in range(lower - 1, lower + 2):
        star = ''
        diff = (pressed * (race.time - pressed)) - race.distance
        if pressed == lower:
            star = '* '
        print(f'{star}Pressed {pressed}: {diff}')

    upper = race.time - lower
    print(f'Upper: {upper}')
    for pressed in range(upper- 1, upper + 2):
        star = ''
        diff = (pressed * (race.time - pressed)) - race.distance
        if pressed == upper:
            star = '* '
        print(f'{star}Pressed {pressed}: {diff}')

    answer = upper - lower + 1
    print('Answer', answer)


def main(data):
    Race = collections.namedtuple('Race', 'time,distance')
    data = [
        Race(7, 9),
        Race(15, 40),
        Race(30, 200),
    ]
    data = [
        Race(46, 358),
        Race(68, 1054),
        Race(98, 1807),
        Race(66, 1080),
    ]
    #part_1(data)
    race = Race(71530, 940200)
    race = Race(46689866, 358105418071080)
    part_2(race)


if __name__ == '__main__':
    data = load_data()
    main(data)
