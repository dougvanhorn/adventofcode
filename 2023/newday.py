#!/usr/bin/env python3

import pathlib
import re
import sys

# Python solution template.
PYTHON_TEMPLATE = '''#!/usr/bin/env python3

import collections
import math
import logging
import pathlib

logging.basicConfig(level=logging.DEBUG, format='%(message)s')


def debug(message):
    log = logging.getLogger('aoc')
    log.debug(message)


def part_1(data):
    debug('== Part 1 ==')
    pass


def part_2(data):
    debug('== Part 2 ==')
    pass


def main(data):
    part_1(data)
    part_2(data)


if __name__ == '__main__':
    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00-input.txt
    with open(f'{stem}-input.txt', mode='r+') as fp:
        data = [line.strip() for line in fp.readlines()]

    main(data)
'''


def main():
    print('Creating templates for: https://adventofcode.com/2023')

    # Get the day number from the user.
    try:
        day = sys.argv[1]
    except IndexError:
        day = input('Enter a two-digit day: ')
        if not re.match('\d\d', day):
            print('Nope.  Try again when you get your shit together.')
            exit(1)

    # Format our filenames.
    python_filename = f'day{day}.py'
    input_filename = f'day{day}-input.txt'

    # Write the template to disk.  Make it executable.  And make it lame.
    with open(python_filename, mode='w') as fp:
        fp.write(PYTHON_TEMPLATE)
    pathlib.Path(python_filename).chmod(0o755)

    # Create a placeholder for the input data.
    pathlib.Path(input_filename).touch()

    print(f'Created {python_filename} and {input_filename}')


if __name__ == '__main__':
    main()
