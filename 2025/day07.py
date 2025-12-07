#!/usr/bin/env python

import collections
import dataclasses
import logging
import math
import pathlib

import rich
from rich.progress import track


logging.basicConfig(level=logging.DEBUG, format='%(message)s')
log = logging.getLogger('aoc')


def load_data():
    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00-input.txt
    with open(f'{stem}-input.txt', mode='r+') as fp:
        data = [line.strip('\n') for line in fp.readlines()]
    return data


def part_1(tree):
    rich.print('[bold red]== Part 1 ==[/bold red]')
    rich.print('Follow the beams to find the way out of the tree')

    beam_columns = set([tree.start.col])
    split_count = 0

    for i, row in enumerate(tree.rows[2:], start=2):
        splitter_cols = [i for i, c in enumerate(row) if c == '^']

        #print(f'{i:<3} {tree.rows[i]}')
        #print(f'  Splitters: {splitters}')

        # Loop over splitters, split beams as needed.
        for splitter_col in splitter_cols:
            if splitter_col in beam_columns:
                split_count += 1
                beam_columns.remove(splitter_col)
                if splitter_col - 1 >= 0:
                    beam_columns.add(splitter_col - 1)
                if splitter_col + 1 < tree.width:
                    beam_columns.add(splitter_col + 1)

        #print(f'    Beams: {sorted(beam_columns)}')
        #print(f'    Splits: {split_count}')

    rich.print(f'[bold green]Total Splits: {split_count}[/bold green]')


def part_2(tree):
    rich.print('[bold red]== Part 2 ==[/bold red]')
    rich.print('Single particle traverse the tree, find all ways out.')

    # {col: count}
    particle_cols = collections.defaultdict(int)
    particle_cols[tree.start.col] = 1

    for i, row in enumerate(tree.rows[2:], start=2):
        splitter_cols = [i for i, c in enumerate(row) if c == '^']

        #print(f'{i:<3} {tree.rows[i]}')
        #print(f'  Splitters: {splitters}')

        # Loop over splitters, split beams as needed.
        for splitter_col in splitter_cols:
            if splitter_col in particle_cols:
                # Split the particle, carry the count forward.
                count = particle_cols.pop(splitter_col)
                particle_cols[splitter_col - 1] += count
                particle_cols[splitter_col + 1] += count

        # chars = []
        # for i, c in enumerate(row):
        #     chars.append(str(particle_cols.get(i, c)))
        # print(''.join(chars))


    positions = sum(particle_cols.values())
    rich.print(f'[bold green]Final Multiverses: {positions}[/bold green]')


def part_2_traverse(tree):
    rich.print('[bold red]== Part 2 ==[/bold red]')
    rich.print('Single particle traverse the tree, find all ways out.')

    def traverse(row_idx, particle_col):
        # Recursesively traverse the tree.
        # Bottom out, counts as one path.
        if row_idx >= tree.height:
            return 1  # Reached the bottom, found a path.

        row = tree.rows[row_idx]
        splitter_cols = [i for i, c in enumerate(row) if c == '^']
        print(f'Row: {row}')
        print(f'Splitters: {splitter_cols}')
        print(f'Particle Col: {particle_col}')
        # input('Press Enter to continue...')

        total_paths = 0
        if particle_col in splitter_cols:
            # Splitter hit, choose left and right paths.
            # Traverse left.
            left_paths = traverse(row_idx + 1, particle_col - 1)
            # Traverse right.
            right_paths = traverse(row_idx + 1, particle_col + 1)
            total_paths += left_paths + right_paths

        else:
            # No splitter, continue straight down.
            total_paths += traverse(row_idx + 1, particle_col)

        return total_paths

    total_paths = traverse(2, tree.start.col)
    rich.print(f'[bold green]Total Paths: {total_paths}[/bold green]')


@dataclasses.dataclass
class Coord:
    row: int
    col: int


class Tree:
    def __init__(self, rows):
        self.rows = rows
        self.width = len(rows[0])
        self.height = len(rows)

        self.start = Coord(0, self.rows[0].index('S'))


def main(data):
    _data = [
        '.......S.......',
        '...............',
        '.......^.......',
        '...............',
        '......^.^......',
        '...............',
        '.....^.^.^.....',
        '...............',
        '....^.^...^....',
        '...............',
        '...^.^...^.^...',
        '...............',
        '..^...^.....^..',
        '...............',
        '.^.^.^.^.^...^.',
        '...............',
    ]
    tree = Tree(data)
    part_1(tree)
    part_2(tree)


if __name__ == '__main__':
    data = load_data()
    main(data)
