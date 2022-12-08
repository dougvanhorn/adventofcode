#!/usr/bin/env python3

import collections
import math
import pathlib
import pprint
import re
import traceback

import aoc


# https://adventofcode.com/2021/day/14


class Chain:
    def __init__(self, lines):
        self.lines = lines
        self.start = lines[0]

        self.chain = [c for c in self.start]

        self.rules = {}
        for line in lines[2:]:
            pair = line[:2]
            insert = line[6]
            self.rules[(pair[0], pair[1])] = insert

        self.counts = collections.defaultdict(int)
        for i in range(len(self.chain) - 1):
            pair = (self.chain[i], self.chain[i+1])
            self.counts[pair] += 1


    def pprint(self):
        print('='*79)
        print(aoc.format('Polymer Chain', 'bold blue'))
        print('-'*79)
        print(f'Start: {self.format_chain()}')
        print(f'Count:   {len(self.chain)}')

        chars = set()
        for c in self.chain:
            chars.add(c)
        for pair, insert in self.rules.items():
            chars.add(pair[0])
            chars.add(pair[1])
            chars.add(insert);

        chars = list(chars)
        chars.sort()
        print('Unique Chars:', chars)
        #print(f'Rules ({len(self.rules)}):')
        #pairs = list(self.rules.keys())
        #pairs.sort()
        #for pair in pairs:
        #    print(f'  {pair} -> {self.rules[pair]}')

        print('Pair Counts:')
        pairs = list(self.counts.keys())
        pairs.sort()
        for pair in pairs:
            print(f'  {pair}:{self.counts[pair]}')

        print('Element Count:')
        counter = collections.Counter()
        for pair in pairs:
            count = self.counts[pair]
            counter[pair[0]] += count
            # Do not count the second value, it'll show up as a first value somewhere else.
            #counter[pair[1]] += count

        # Except for the last letter in the chain, it'll never be counted.
        counter[self.start[-1]] += 1

        for char, count in counter.most_common():
            print(f'{char}: {count}')

        print('-'*79)


    def insert(self):
        new_chain = collections.deque()
        for i in range(len(self.chain) - 1):
            lookup_rule = (self.chain[i], self.chain[i+1])
            #print('Pair:', ''.join(c for c in lookup_rule))
            insert_value = self.rules.get(lookup_rule)
            #print(f'  appending {self.chain[i]}')
            new_chain.append(self.chain[i])
            insert_value = self.rules.get(lookup_rule)
            if insert_value:
                #print(f'  appending {insert_value}')
                new_chain.append(insert_value)
            # Don't insert right half of chain, it will insert on next loop.

        # Except for the last character of the chain.
        new_chain.append(self.chain[-1])
        self.chain = [c for c in new_chain]

    def insert_part_2(self):
        # Freeze the state of things before we expand it.
        pairs_and_counts = [(pair, count) for pair, count in self.counts.items()]
        for pair, count in pairs_and_counts:
            insert = self.rules[pair]
            # Remove the old pairing.
            self.counts[pair] -= count
            # And add in the new pairings.
            self.counts[(pair[0], insert)] += count
            self.counts[(insert, pair[1])] += count


    def format_chain(self):
        s = ''.join(c for c in self.chain)
        return s

    def value(self):
        counter = collections.Counter()
        for pair, number_of_pairs in self.counts.items():
            counter[pair[0]] += number_of_pairs
            #counter[pair[1]] += number_of_pairs

        counter[self.start[-1]] += 1
        # list of 2-tuples, char and count.
        counts = counter.most_common()
        return counts[0][1] - counts[-1][1]


def part_1(input_lines):
    chain = Chain(input_lines)

    print(f'Template:     {chain.format_chain()}')
    print(f'  Length: {len(chain.chain)}')

    for step in range(1, 3):
        chain.insert()
        #print(f'After step {step}: {chain.format_chain()}')
        print(f'Step {step} Length: {len(chain.chain)}')

    print(f'Value after 10 steps: {chain.value()}')


def part_2(input_lines):
    chain = Chain(input_lines)
    chain.pprint()

    for step in range(1, 41):
        chain.insert_part_2()
        #print(f'After step {step}: {chain.format_chain()}')
        print(f'## Step {step}')
        chain.pprint()
        print()

    print(f'Value after steps: {chain.value()}')


def main(input_lines):
    #print('Part 1')
    #print('=' * 79)
    #part_1(input_lines)

    #print()
    #print()
    print('Part 2')
    print('=' * 79)
    part_2(input_lines)


TEST_INPUT = [
    'NNCB',
    '',
    'CH -> B',
    'HH -> N',
    'CB -> H',
    'NH -> C',
    'HB -> C',
    'HC -> B',
    'HN -> C',
    'NN -> C',
    'BH -> H',
    'NC -> B',
    'NB -> B',
    'BN -> B',
    'BB -> N',
    'BC -> B',
    'CC -> N',
    'CN -> C',
]


if __name__ == '__main__':
    path = pathlib.Path(__file__)
    day_number = path.name[3:5]
    filename = f'{day_number}.txt'
    lines = aoc.loadfile(filename)
    _lines = TEST_INPUT
    n = len(lines)
    print(aoc.format(f'Loaded {filename}: {n} lines.', 'blue'))
    main(lines)
