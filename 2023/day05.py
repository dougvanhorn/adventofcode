#!/usr/bin/env python3

import collections
import math
import logging
import pathlib

logging.basicConfig(level=logging.DEBUG, format='%(message)s')

class Map:
    def __init__(self, maps):
        # list of maps from almanac.
        # 50 98 2 means
        #  50 -> 98
        #  51 -> 99
        self._data = maps

        # Convert everything to ints.
        self.ranges = []
        for row in maps:
            self.ranges.append([int(n) for n in row])

    def lookup(self, n):
        # if n is in any of the defined ranges
        # do the map.
        for row in self.ranges:
            dest_start, source_start, width = row
            # Make these inclusive.
            dest_end = dest_start + width - 1
            source_end = source_start + width - 1

            if source_start <= n <= source_end:
                return dest_start + (n - source_start)

        return n


class Almanac:
    def __init__(self, data, part2=True):
        # Split by blank line.
        sections = []
        section = []
        sections.append(section)
        for row in data:
            if row:
                section.append(row)
            else:
                section = []
                sections.append(section)

        for section in sections:
            print(section)
            print()

        seeds_section = sections[0]
        self.seeds = [int(seed) for seed in seeds_section[0][7:].split()]

        soil_fert_section = sections[1]
        self.seed_soil_map = [s.split() for s in sections[1][1:]]
        self.seed_soil_map = Map(self.seed_soil_map)

        self.soil_fert_map = [s.split() for s in sections[2][1:]]
        self.soil_fert_map = Map(self.soil_fert_map)

        self.fert_water_map = [s.split() for s in sections[3][1:]]
        self.fert_water_map = Map(self.fert_water_map)

        self.water_light_map = [s.split() for s in sections[4][1:]]
        self.water_light_map = Map(self.water_light_map)

        self.light_temp_map = [s.split() for s in sections[5][1:]]
        self.light_temp_map = Map(self.light_temp_map)

        self.temp_hum_map = [s.split() for s in sections[6][1:]]
        self.temp_hum_map = Map(self.temp_hum_map)

        self.hum_loc_map = [s.split() for s in sections[7][1:]]
        self.hum_loc_map = Map(self.hum_loc_map)

    def part1(self):
        locations = []
        for seed in self.seeds:
            soil = self.seed_soil_map.lookup(seed)
            fert = self.soil_fert_map.lookup(soil)
            water = self.fert_water_map.lookup(fert)
            light = self.water_light_map.lookup(water)
            temp = self.light_temp_map.lookup(light)
            hum = self.temp_hum_map.lookup(temp)
            loc = self.hum_loc_map.lookup(hum)
            locations.append(loc)
            print(f'seed:{seed} => location:{loc}')

        return min(locations)


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
    book = Almanac(data)
    location = book.part1()
    print('Answer:', location)


def part_2(data):
    p('== Part 2 ==')
    # https://www.youtube.com/watch?v=NmxHw_bHhGM

    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00-input.txt
    with open(f'{stem}-input.txt', mode='r+') as fp:
        inputs, *blocks = fp.read().split('\n\n')

    # seeds: 123 456 789 1234
    inputs = list(map(int, inputs.split(':')[1].split()))

    seeds = []
    # numbers (start, range) tuples.
    for index in range(0, len(inputs), 2):
        # Create the ranges, (left, right).
        left = inputs[index]
        size = inputs[index+1]
        right = left + size
        seeds.append((left, right))

    for block in blocks:
        ranges = []
        # each block is a set of map rules from the file.
        #   seed-to-soil-map:
        #   50 98 2
        for line in block.splitlines()[1:]:
            ranges.append(list(map(int, line.split())))

        # use seeds as a soure of ranges,
        # build a new range list from that source.
        new_ranges = []
        while seeds:
            start, end = seeds.pop()

            for dest, source, size in ranges:
                # The position tranform the mapping defines.
                # E.g., 60 55 means +5, 50 55 means -5.
                transform = dest - source
                overlap_start = max(start, source)
                overlap_end = min(end, source + size)
                if overlap_start < overlap_end:
                    # Place the overlap range into new_ranges.
                    #new_ranges.append((overlap_start + transform, overlap_end + transform))
                    new_ranges.append((overlap_start - source + dest, overlap_end - source + dest))
                    # account for outlying ranges.
                    # place them back into seeds for reconsideration.
                    if overlap_start > start:
                        seeds.append((start, overlap_start))
                    if end > overlap_end:
                        seeds.append((overlap_end, end))

                    # Overlap added to new ranges, go to top of while loop.
                    break

            else:
                # probably don't need this as "else".
                new_ranges.append((start, end))

        seeds = new_ranges

    seeds.sort()
    print(min(seeds))
    print(seeds)







def main(data):
    data = [
        'seeds: 79 14 55 13',
        '',
        'seed-to-soil map:',
        '50 98 2',
        '52 50 48',
        '',
        'soil-to-fertilizer map:',
        '0 15 37',
        '37 52 2',
        '39 0 15',
        '',
        'fertilizer-to-water map:',
        '49 53 8',
        '0 11 42',
        '42 0 7',
        '57 7 4',
        '',
        'water-to-light map:',
        '88 18 7',
        '18 25 70',
        '',
        'light-to-temperature map:',
        '45 77 23',
        '81 45 19',
        '68 64 13',
        '',
        'temperature-to-humidity map:',
        '0 69 1',
        '1 0 69',
        '',
        'humidity-to-location map:',
        '60 56 37',
        '56 93 4',
    ]
    #part_1(data)
    part_2(data)


if __name__ == '__main__':
    data = load_data()
    main(data)
