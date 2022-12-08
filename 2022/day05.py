#!/usr/bin/env python3

import collections
import pathlib


# This is a convenient data structure too.
# Very much like a Struct in C++.
Instruction = collections.namedtuple('Instruction', 'quantity origin destination')


class Warehouse:
    """Holds the various stacks of crates in the warehouse.

    Provides different move methods for different crane types.
    """
    def __init__(self, data):
        # Hard coded for 9 stacks.
        self.stacks = [[] for _ in range(9)]
        for row in data:
            # print(f'Processing |{row}|')
            # |[c] [c] [c] ... [c]|
            # | 1   5   9  ...  33   
            columns = [crate for crate in row[1::4]]
            # print(f'Columns: {columns}')
            for stack_i, crate in enumerate(columns):
                # print(f'    {stack_i}: {crate}')
                if crate != ' ':
                    # print(f'Inserting Crate [{crate}]')
                    # print('    ...Inserting.')
                    # Because we're working "top to bottom" given the input data, we need to put each
                    # crate at the "bottom" of the stack.  So we insert it at the 0th position.
                    self.stacks[stack_i].insert(0, crate)

    def move_9000(self, instr):
        # Move one at a time.
        for i in range(instr.quantity):
            # print(f'{instr}')
            self.stacks[instr.destination].append(self.stacks[instr.origin].pop())

    def move_9001(self, instr):
        # Move substack together...
        #print(f'Move {instr.quantity} from {self.stacks[instr.origin]} to {self.stacks[instr.destination]}')
        # Grab the substack
        substack = self.stacks[instr.origin][-1*instr.quantity:]

        #print(f'    substack: {substack}')

        # remove
        del self.stacks[instr.origin][-1*instr.quantity:]

        # add
        # Note the use of `extend` instead of `append`.
        self.stacks[instr.destination].extend(substack)

        #print(f'    origin {self.stacks[instr.origin]}')
        #print(f'    dest {self.stacks[instr.destination]}')
        #print()

    def tops(self):
        return ''.join([stack[-1] for stack in self.stacks])


class Program:
    """A list of crane instructions.

    Parses the input file into instructions.
    """
    def __init__(self, data):
        self.instructions = []
        for text in data:
            parts = text.split(' ')
            self.instructions.append(
                # quantity, origin stack, dest. stack
                Instruction(
                    int(parts[1]),  # quantity
                    int(parts[3])-1,  # origin stack index
                    int(parts[5])-1,  # dest. stack index
                )
            )


def part_1(warehouse, program):
    # Crane 9000, moves one at a time.
    for instr in program.instructions:
        warehouse.move_9000(instr)

    print(f'Part 1: {warehouse.tops()}')


def part_2(warehouse, program):
    # Crane 9001, moves several at a time.
    for instr in program.instructions:
        warehouse.move_9001(instr)

    print(f'Part 2: {warehouse.tops()}')


def main(data):
    warehouse = Warehouse(data[:8])
    program = Program(data[10:])

    part_1(warehouse, program)

    # Need the clean data, not the munged data from part 1.
    warehouse = Warehouse(data[:8])
    part_2(warehouse, program)


if __name__ == '__main__':
    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00input.txt
    with open(f'{stem}input.txt', mode='r+') as fp:
        # DON'T Strip this data!
        data = [line for line in fp.readlines()]

    main(data)

