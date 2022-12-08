#!/usr/bin/env python3

import collections
import math
import pprint
import re
import traceback

import aoc

DEMO = '''7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7'''

# https://adventofcode.com/2021/day/4

class Line:
    def __init__(self, numbers, line_type):
        self.line_type = line_type
        self.numbers = numbers
        self.marks = [[n, False] for n in numbers]
        self.marked = 0
        self.contains = {n for n in self.numbers}

    def __repr__(self):
        return str(self)

    def __str__(self):
        display_numbers = []
        for el in self.marks:
            x = 'x' if el[1] else ' '
            display_numbers.append(f'{el[0]:>2}{x}')
        display_numbers = ' '.join(display_numbers)
        return f'{self.line_type}: ' + display_numbers + f', Marked: {self.marked}'

    def __contains__(self, n):
        return n in self.contains

    def mark(self, n):
        for el in self.marks:
            if n == el[0]:
                if el[1] is False:
                    self.marked += 1
                el[1] = True



class Board:
    def __init__(self, name, lines):
        self.name = name
        self.rows = [row.split() for row in lines]
        self.cols = [[] for _ in range(5)]
        for row in self.rows:
            for col, n in enumerate(row):
                self.cols[col].append(n)

        self.lookup = collections.defaultdict(list)
        self.last_number_called = None

        self.lines = []
        for row in self.rows:
            line = Line(row, 'Row')
            self.lines.append(line)
            for n in row:
                self.lookup[n].append(line)

        for col in self.cols:
            line = Line(col, 'Col')
            self.lines.append(line)
            for n in col:
                self.lookup[n].append(line)

        self.winner = None

    def __str__(self):
        s = f'Board: {self.name}\n'
        s += '\n'.join([str(line) for line in self.lines])
        return s

    def mark(self, n):
        if self.winner:
            return
        lines = self.lookup.get(n, [])
        if lines:
            #print(f'{n} found in board {self.name}')
            pass
        for line in lines:
            line.mark(n)
            #print(f'Marked {line}')

        for line in lines:
            if line.marked == 5:
                self.winner = line
                return

    def unmarked(self):
        unmarked = []
        rows = [line for line in self.lines if line.line_type == 'Row']
        for line in rows:
            for n in line.marks:
                if not n[1]:
                    unmarked.append(n[0])
        return unmarked


def loadfile():
    lines = aoc.loadfile('04.txt')
    #lines = DEMO.split('\n')

    numbers = [n for n in lines[0].split(',')]

    boards = []
    name = 0
    #for i in range(2, 32, 6):
    for i in range(2, len(lines) + 1, 6):
        board = Board(name, lines[i:i+5])
        boards.append(board)
        name += 1

    return numbers, boards


def part_1():
    numbers, boards = loadfile()

    called = []
    print(f'Board count: {len(boards)}')
    for n in numbers:
        called.append(n)
        print(f'calling {n}')
        for b in boards:
            b.mark(n)
            if b.winner:
                print('WINNER')
                print(f'Numbers Called: {called}')
                print(f'n: {n}')
                print(f'winner: {b.winner}')
                print(b)
                subtotal = sum(int(n) for n in b.unmarked())
                print(f'Subtotal of unmarked: {subtotal}')
                total = subtotal * int(n)
                print(f'Total: {total}')

                return 0


def main():
    numbers, boards = loadfile()
    print(f'boards: {boards}')
    called = []
    for n in numbers:
        called.append(n)
        next_boards = []
        for b in boards:
            print(f'working board {b.name}')
            b.mark(n)
            if b.winner:
                print(f'Winner Found: {b}')
                b.last_number_called = n
                if len(boards) == 1:
                    print('LAST WINNER')
                    print(f'Numbers Called: {called}')
                    print(f'n: {n}')
                    print(f'winner: {b.winner}')
                    print(b)
                    subtotal = sum(int(n) for n in b.unmarked())
                    print(f'Subtotal of unmarked: {subtotal}')
                    total = subtotal * int(n)
                    print(f'Total: {total}')
                    return 0
            else:
                next_boards.append(b)
        boards = next_boards


if __name__ == '__main__':
    main()


