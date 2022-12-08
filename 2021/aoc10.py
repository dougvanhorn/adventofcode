#!/usr/bin/env python3

import collections
import math
import pathlib
import pprint
import re
import traceback

import aoc


# https://adventofcode.com/2021/day/10

OPEN = '([{<'

CLOSE = ')]}>'

MAP = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

# Syntax errors involve wrong closing char.
SYNTAX_POINTS = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

# Autocomplete involves opening chars.
AUTOCOMPLETE_POINTS = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4,
}


class Line:
    def __init__(self):
        self.line = None
        self.stack = None
        self.syntax_error = False
        self.error_at = None
        self.points = 0


def parse_line(line):
    # Returns a Line instance.
    stack = collections.deque()
    parsed_line = Line()
    parsed_line.line = line
    parsed_line.stack = stack
    for i, current_char in enumerate(line):
        if current_char in OPEN:
            stack.append(current_char)
        else:
            last_char = stack.pop()
            if MAP[last_char] != current_char:
                parsed_line.syntax_error = True
                parsed_line.error_at = i
                parsed_line.points = SYNTAX_POINTS[current_char]
                return parsed_line

    # print('Line:', line)
    # print('stack:', stack)
    return parsed_line


def part_1(input_lines):
    # Score the closing violations.
    score = 0
    for string_line in input_lines:
        line = parse_line(string_line)
        if line.syntax_error:
            score += line.points

    print(f'Part 1 Total Score: {score}')


def part_2(input_lines):
    scores = []
    for string_line in input_lines:
        score = 0
        line = parse_line(string_line)
        if line.syntax_error:
            # Don't score syntax error lines.
            continue

        # Close the stack and score along the way.
        while line.stack:
            last_char = line.stack.pop()
            score *= 5
            score += AUTOCOMPLETE_POINTS[last_char]

        scores.append(score)

    # Get the middle score, invarian: odd-length list.
    scores.sort()
    middle_score = scores[len(scores) // 2]
    print(f'Part 2 Score: {middle_score}')


def main(input_lines):
    part_1(input_lines)
    part_2(input_lines)


TEST_INPUT = [
    '[({(<(())[]>[[{[]{<()<>>',
    '[(()[<>])]({[<{<<[]>>(',
    '{([(<{}[<>[]}>{[]{[(<()>',
    '(((({<>}<{<{<>}{[]{[]{}',
    '[[<[([]))<([[{}[[()]]]',
    '[{[{({}]{}}([{[{{{}}([]',
    '{<[[]]>}<{[{[{[]{()[[[]',
    '[<(<(<(<{}))><([]([]()',
    '<{([([[(<>()){}]>(<<{{',
    '<{([{{}}[<[[[<>{}]]]>[]]',
]

if __name__ == '__main__':
    path = pathlib.Path(__file__)
    day_number = path.name[3:5]
    filename = f'{day_number}.txt'
    lines = aoc.loadfile(filename)
    _lines = TEST_INPUT
    n = len(lines)
    aoc.info(f'Loaded {filename}: {n} lines.')
    main(lines)
