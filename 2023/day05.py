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
        inputs, *sections = fp.read().split('\n\n')

    # seeds: 79 14 55 13
    inputs = list(map(int, inputs.split(':')[1].split()))
    # numbers (start, range) tuples.
    # [79, 14, 55, 13]
    seeds = []
    # Pair up the left and size to get full range.
    for index in range(0, len(inputs), 2):
        # Create the ranges, (left, right).
        left = inputs[index]
        size = inputs[index+1]
        right = left + size
        seeds.append((left, right))
    # (79, 93), (55, 68)

    print(f'{len(seeds)} Seed ranges need transforming.')
    for seed in seeds:
        print(f'  {seed}')
    # Blocks are all the sections of mappings.
    for section in sections:
        section_rules = []
        # each block is a set of map rules from the file.
        #   seed-to-soil-map:
        #   50 98 2
        # drop the first line (section name), then map each line to a list of ints.
        lines = section.splitlines()
        print('='*79)
        print(f'= SECTION {lines[0]}')
        print('-'*79)
        for line in lines[1:]:
            section_rules.append(list(map(int, line.split())))
        # [[50, 98, 2], [52, 50, 48]]

        # "seeds" is the source ranges we need to transform.
        # build a new range list from that source.
        transformed_ranges = []
        while seeds:
            # we will pop one range every loop.
            # we will add to seeds as we run through the blocks.
            start, end = seeds.pop()
            print(f'=== SEED {start} {end}')

            for dest, source, size in section_rules:
                # The position tranform the mapping defines.
                # E.g., 52 50 means +2, 50 98 means -48
                transform = dest - source
                print(f'Section Rule: ({source}, {source+size}) {transform} / {dest} {source} {size}')

                # Given a seed range, and a mapping rule,
                # Determine if there is an overlap.
                # E.g.,
                #                [55 56 57 58 59 60 61 62 63 64 65 66 67 68]  seed range
                # [50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 ... 98]  52 50 48 transform
                #
                # Given the overlap, we need to generate a new transformed range in the soil values.
                # [55+transform ... 68+transform]
                # [57 58 59 60 61 62 63 64 65 66 67 68 69 70]
                # 
                # if we had seed range that wasn't mapped (left of overlap start or right of overlap end)
                # we would add them back to seeds in case they get transformed by a subsequent mapping rule.

                overlap_start = max(start, source)
                overlap_end = min(end, source + size)
                if overlap_start < overlap_end:
                    print(f'  Seed / Rule Overlap: {overlap_start} {overlap_end}')
                    # Place the overlap range into new_ranges.
                    #new_ranges.append((overlap_start + transform, overlap_end + transform))
                    transformed_range = (overlap_start + transform, overlap_end + transform)
                    print(f'  Transformed Seed Range: {transformed_range}')
                    transformed_ranges.append(transformed_range)
                    # any seed range not transformed goes back into seeds list, as later transforms
                    # may apply to them.
                    if overlap_start > start:
                        print(f'  Adding untransformed ({start}, {overlap_start}) back to seeds list.')
                        seeds.append((start, overlap_start))
                    if end > overlap_end:
                        print(f'  Adding untransformed ({overlap_end}, {end}) back to seeds list.')
                        seeds.append((overlap_end, end))

                    # Done transforming ranges and adding back un-transformed.
                    # Back to the top of the loop.
                    print('  Seed range transformed, move to next seed.')
                    print('.'*79)
                    break

                else:
                    print('...no overlap, skipping.')

            else:
                # probably don't need this as "else".
                print(f'No rules apply, adding ({start}, {end}) to transformed ranges.')
                transformed_ranges.append((start, end))

        seeds = transformed_ranges
        print(f'= SECTION {lines[0]} complete.')
        print('Seed values are now:')
        for r in sorted(seeds):
            print(f'  {r}')
        print('-'*79)


    seeds.sort()
    #print(seeds)
    answer = min(seeds)[0]
    print('Answer', answer)
    if answer != 52210644:
        print('WRONG!')







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
