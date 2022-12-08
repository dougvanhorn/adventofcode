#!/usr/bin/env python3

import collections
import math
import re
import traceback

import aoc


class Line:
    def __init__(self, line_number, text):
        self.text = text
        self.line_number = line_number
        parsed = text.split(' ')
        self.instruction = parsed[0]
        self.value = int(parsed[1])

    def __str__(self):
        return f'{self.line_number}: {self.instruction} {self.text[4:]}'


class InfiniteLoop(Exception):
    pass


class Program:
    def __init__(self, file_lines):
        self.file_lines = file_lines
        self.lines = [Line(i, line) for i, line in enumerate(file_lines)]
        self.line_count = len(self.lines)
        self.previous_line = 0
        self.current_line = 0
        self.accumulator = 0
        self.lines_seen = set()

    def run(self):
        # Program state during this run.
        self.previous_line = 0
        self.current_line = 0
        self.accumulator = 0
        self.lines_seen = set()

        while True:
            if self.current_line in self.lines_seen:
                raise InfiniteLoop(f'Inifinite loop detected at line {self.current_line} (from '
                                   f'{self.previous_line}).')

            self.lines_seen.add(self.current_line)

            if self.current_line == self.line_count:
                # Program complete.
                return
            elif self.current_line > self.line_count:
                raise Exception(f'{self.current_line} out of bounds ({self.line_count}).')

            line = self.lines[self.current_line]

            if line.instruction == 'nop':
                self.previous_line = self.current_line
                self.current_line += 1
                continue

            elif line.instruction == 'acc':
                self.accumulator += line.value
                self.previous_line = self.current_line
                self.current_line += 1
                continue

            elif line.instruction == 'jmp':
                self.previous_line = self.current_line
                self.current_line += line.value
                continue

            else:
                raise Exception(f'Unknown Instruction: {line}')


def main():
    lines = aoc.loadfile('08.txt')
    program = Program(lines)
    try:
        program.run()
        print(f'Accumulator: {program.accumulator}')

    except InfiniteLoop as exc:
        print(exc)
        print(f'Accumulator: {program.accumulator}')

    for line in program.lines:
        if line.instruction == 'nop':
            line.instruction = 'jmp'
            try:
                program.run()
                print(f'Changed {line} to jmp')
                print(f'Completes! Accumulator: {program.accumulator}')

            except InfiniteLoop as exc:
                #print(exc)
                #print(f'Accumulator: {program.accumulator}')
                pass

            except Exception as exc:
                #print(exc)
                #print(f'Accumulator: {program.accumulator}')
                pass
            line.instruction = 'nop'

        elif line.instruction == 'jmp':
            #print(f'Changing {line} to nop')
            line.instruction = 'nop'
            try:
                program.run()
                print(f'Changed {line} to nop')
                print(f'Completes! Accumulator: {program.accumulator}')

            except InfiniteLoop as exc:
                #print(exc)
                #print(f'Accumulator: {program.accumulator}')
                pass

            except Exception as exc:
                #print(exc)
                #print(f'Accumulator: {program.accumulator}')
                pass
            line.instruction = 'jmp'


if __name__ == '__main__':
    main()
