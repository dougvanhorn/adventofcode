#!/usr/bin/env python3

import collections
import math
import pathlib

class Forest:
    def __init__(self, data):
        self.grid = []
        for row in data:
            self.grid.append([int(c) for c in row])
        self.row_count = len(self.grid)
        self.col_count = len(self.grid[0])

    def __str__(self):
        output = ''
        for row in self.grid:
            output += ''.join(str(x) for x in row) + '\n'

        return output

    def part_1(self):
        # Skip top row, bottom row.
        visible_trees = set()

        # Rows
        for row_i, row in enumerate(self.grid[1:-1], start=1):
            print(f'Row {row_i}')
            # Left and right tree are always visible.
            visible_trees.add((row_i, 0))
            visible_trees.add((row_i, self.row_count - 1))

            # view from left
            print(f'- From Left, Starting Height: {row[0]}')
            current_height = row[0]
            for col, tree in enumerate(row[1:-1], start=1):
                visible = bool(tree > current_height)
                print(f'  - Tree {col}: {tree}, current-height: {current_height}, Visible: {visible}')
                if visible:
                    current_height = tree
                    visible_trees.add((row_i, col))

                if current_height == 9:
                    # Max height reached, no need to continue looking.
                    break


            print()

            # view from right
            # descending index, 3, 2, 1, exclude edges
            current_height = row[-1]
            print(f'- From Right, Starting Height: {current_height}')
            for col in range(self.row_count - 2, 0, -1):
                tree = row[col]
                visible = bool(tree > current_height)
                print(f'  - Tree {col}: {tree}, current-height: {current_height}, Visible: {visible}')
                if visible:
                    current_height = tree
                    visible_trees.add((row_i, col))

                if current_height == 9:
                    # Max height reached, no need to continue looking.
                    break

            print()

        # Columns, 1 to self.row_count - 1, exclude outer columns
        for col in range(1, self.col_count-1):
            print(f'Col {col}')
            # Top and bottom tree are always visible.
            visible_trees.add((0, col))
            visible_trees.add((self.row_count-1, col))

            # view from top
            # ascending index, 1, 2, 3, exclude edges
            current_height = self.grid[0][col]
            print(f'- From Top, Starting Height: {current_height}')
            for row in range(1, self.row_count - 1):
                tree = self.grid[row][col]
                visible = bool(tree > current_height)
                print(f'  - Tree {row}: {tree}, current-height: {current_height}, Visible: {visible}')
                if visible:
                    current_height = tree
                    visible_trees.add((row, col))

                if current_height == 9:
                    # Max height reached, no need to continue looking.
                    break

            print()

            # view from bottom
            # descending index, 3, 2, 1, exclude edges
            current_height = self.grid[-1][col]
            print(f'- From Bottom, Starting Height: {current_height}')
            for row in range(self.row_count - 2, 0, -1):
                tree = self.grid[row][col]
                visible = bool(tree > current_height)
                print(f'  - Tree {row}: {tree}, current-height: {current_height}, Visible: {visible}')
                if visible:
                    current_height = tree
                    visible_trees.add((row, col))

                if current_height == 9:
                    # Max height reached, no need to continue looking.
                    break


        total_visible = len(visible_trees)
        # Corners
        total_visible += 4

        print()
        print(f'Total Visible: {total_visible}')

    def part_2(self):
        scores = []
        print('Part 2')
        Score = collections.namedtuple('Score', 'row col score')
        # scenic score, traverse every tree and score it.
        for row in range(0, self.row_count):
            for col in range(0, self.col_count):
                score = self.calculate_scenic_score(row, col)
                scores.append(Score(row, col, score))

        scores.sort(key=lambda score: score.score)
        print(f'Highest Score: {scores[-1].score}')

    def calculate_scenic_score(self, row, col):
        tree = self.grid[row][col]
        # build 4 index lists
        up = range(row-1, -1, -1)
        down = range(row+1, self.row_count)
        left = range(col-1, -1, -1)
        right = range(col+1, self.col_count)

        scores = []

        visible = 0
        for row_i in up:
            up_tree = self.grid[row_i][col]
            visible += 1
            # Stop looking at same height or taller than scored tree.
            if up_tree >= tree:
                break
        scores.append(visible)

        visible = 0
        for row_i in down:
            down_tree = self.grid[row_i][col]
            visible += 1
            # Stop looking at same height or taller than scored tree.
            if down_tree >= tree:
                break
        scores.append(visible)

        visible = 0
        for col_i in left:
            left_tree = self.grid[row][col_i]
            visible += 1
            # Stop looking at same height or taller than scored tree.
            if left_tree >= tree:
                break
        scores.append(visible)

        visible = 0
        for col_i in right:
            right_tree = self.grid[row][col_i]
            visible += 1
            # Stop looking at same height or taller than scored tree.
            if right_tree >= tree:
                break
        scores.append(visible)

        scenic_score = math.prod(scores)
        print(f'Scoring ({row}, {col}) Height: {tree} Score: {scenic_score}')

        return scenic_score


def part_1(data):
    forest = Forest(data)
    print(forest)
    forest.part_1()


def part_2(data):
    forest = Forest(data)
    print(forest)
    forest.part_2()


def main(data):
    EXAMPLE_INPUT = [
        '30373',
        '25512',
        '65332',
        '33549',
        '35390',
    ]
    #part_1(EXAMPLE_INPUT)
    #part_1(data)
    #part_2(EXAMPLE_INPUT)
    part_2(data)


if __name__ == '__main__':
    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00input.txt
    with open(f'{stem}input.txt', mode='r+') as fp:
        data = [line.strip() for line in fp.readlines()]

    main(data)

