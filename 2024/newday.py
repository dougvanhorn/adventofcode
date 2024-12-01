#!/usr/bin/env python3

import pathlib
import re
import sys

import pyperclip


# Python solution template.
PYTHON_TEMPLATE = '''#!/usr/bin/env python3

import collections
import logging
import math
import pathlib


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
    pass


def part_2(data):
    p('== Part 2 ==')
    pass


def main(data):
    _data = [
    ]
    # part_1(data)
    # part_2(data)


if __name__ == '__main__':
    data = load_data()
    main(data)
'''


def main():
    print('Creating templates for: https://adventofcode.com/2024')

    # Get the day number from the user.
    try:
        day = sys.argv[1]
    except IndexError:
        day = input('Enter the day: ')
        if not re.match(r'\d{1,2}$', day):
            print('Nope.  Try again when you get your shit together.')
            exit(1)

    # Format our filenames.
    day = int(day)
    python_filename = f'day{day:02}.py'
    input_filename = f'day{day:02}-input.txt'

    # Write the template to disk.  Make it executable.  And make it lame.
    with open(python_filename, mode='w') as fp:
        fp.write(PYTHON_TEMPLATE)
    pathlib.Path(python_filename).chmod(0o755)

    # Create a placeholder for the input data.
    pathlib.Path(input_filename).touch()

    print(f'Created {python_filename} and {input_filename}')
    url = f'https://adventofcode.com/2024/day/{day}'
    print(f'    Puzzle:  {url}')
    print(f'    Input:   {url}/input')

    pyperclip.copy(url)
    print('    URL has been copied to the clipboard.')


if __name__ == '__main__':
    main()

