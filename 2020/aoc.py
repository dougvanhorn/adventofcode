#!/usr/bin/env python3
import math
import re
import traceback


def aoc201202():
    with open('aoc201202.txt', mode='r+') as fp:
        text = fp.read()

    rows = text.split('\n')

    class Record:
        def __init__(self, text):
            self.text = text
            rule, password = text.split(': ')
            counts, letter = rule.split(' ')
            min_count, max_count = counts.split('-')
            self.min_count = int(min_count)
            self.max_count = int(max_count)
            self.letter = letter
            self.password = password

        def __str__(self):
            return f'{self.min_count}-{self.max_count} {self.letter}: {self.password}'

        def is_valid_sled(self):
            # min to max count of letter.
            found = re.findall(self.letter, self.password)
            #print(f'found {len(found)} {self.letter} in {self.password}')
            return found and (self.min_count <= len(found) <= self.max_count)

        def is_valid_toboggan(self):
            # exactly one positioned at min, max.
            first = self.password[self.min_count - 1] == self.letter
            second = self.password[self.max_count - 1] == self.letter
            return first != second


    records = []
    for i, rec in enumerate(rows):
        if not rec:
            continue
        try:
            record = Record(rec)
            records.append(record)
        except Exception:
            print(f'Cannot parse {i}: "{rec}"')
            traceback.print_exc()

    print(f'Records: {len(records)}')
    valid_passwords = [rec for rec in records if rec.is_valid_toboggan()]
    print(f'valid password count: {len(valid_passwords)}')


def aoc201203():
    with open('aoc201203.txt', mode='r+') as fp:
        text = fp.read()

    class Map:
        def __init__(self, text):
            self.text = text
            self.rows = self.text.split('\n')
            self.rows = self.rows[:-1]
            self.modulo = len(self.rows[0])

        def traverse(self, right, down):
            x = 0
            tree_count = 0

            for row in self.rows[::down]:
                index = x % self.modulo
                if row[index] == '#':
                    tree_count += 1
                x += right

            return tree_count

    found = []
    map = Map(text)
    tree_count = map.traverse(1, 1)
    found.append(tree_count)
    print(f'Right 1, down 1 tree count: {tree_count}')

    tree_count = map.traverse(3, 1)
    found.append(tree_count)
    print(f'Right 3, down 1 tree count: {tree_count}')

    tree_count = map.traverse(5, 1)
    found.append(tree_count)
    print(f'Right 5, down 1 tree count: {tree_count}')

    tree_count = map.traverse(7, 1)
    found.append(tree_count)
    print(f'Right 7, down 1 tree count: {tree_count}')

    tree_count = map.traverse(1, 2)
    found.append(tree_count)
    print(f'Right 1, down 2 tree count: {tree_count}')

    product = math.prod(found)
    print(f'found: {found}, {product}')


if __name__ == '__main__':
    aoc201203()
