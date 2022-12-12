#!/usr/bin/env python3

import collections
import heapq as heap
import pathlib


class Cell:
    def __init__(self, row, col, height, grid):
        self.row = row
        self.col = col
        self.height = height
        self.grid = grid

    def __str__(self):
        return f'({self.row},{self.col}) {self.height}'

    @property
    def node(self):
        return (self.row, self.col)


class Grid:
    def __init__(self, data, custom_start=None):
        self.grid = []
        self.start = None
        self.end = None
        self.path = []
        self.path_set = set()
        self.found_paths = []

        for row_i, row in enumerate(data):
            grid_row = []
            for col_j, letter in enumerate(row):
                height = ord(letter) - 96
                if letter == 'S':
                    height = 0
                elif letter == 'E':
                    height = 27

                cell = Cell(row_i, col_j, height, self)

                if letter == 'S':
                    self.start = cell
                elif letter == 'E':
                    self.end = cell
                
                grid_row.append(cell)
            self.grid.append(grid_row)

        if custom_start:
            self.start = self.grid[custom_start[0]][custom_start[1]]

        self.row_count = len(self.grid)
        self.col_count = len(self.grid[0])
        self.shortest_path_length = self.row_count * self.col_count

        self.visited_count = 0

    def __str__(self):
        rows = []
        for row in self.grid:
            rows.append(' '.join(f'{cell.height:02}' for cell in row))

        return '\n'.join(rows)

    def __repr__(self):
        return f'{self.row_count}x{self.col_count} Grid'

    def neighbors(self, node):
        row, col = node
        cell = self.grid[row][col]

        neighbors = []

        up = row - 1
        down = row + 1
        left = col - 1
        right = col + 1

        if 0 <= up <= self.row_count-1:
            neighbor = self.grid[up][col]
            if neighbor.height - cell.height <= 1:
                neighbors.append(neighbor)

        if 0 <= down <= self.row_count-1:
            neighbor = self.grid[down][col]
            if neighbor.height - cell.height <= 1:
                neighbors.append(neighbor)

        if 0 <= left <= self.col_count-1:
            neighbor = self.grid[row][left]
            if neighbor.height - cell.height <= 1:
                neighbors.append(neighbor)

        if 0 <= right <= self.col_count-1:
            neighbor = self.grid[row][right]
            if neighbor.height - cell.height <= 1:
                neighbors.append(neighbor)

        return neighbors

    def print_visited(self, costs):
        for row_i in range(self.row_count):
            c = []
            for col_j in range(self.col_count):
                if (row_i, col_j) in costs:
                    c.append('v')
                else:
                    c.append('.')
            print(''.join(c))

    def lowest(self):
        found = []
        for row in range(self.row_count):
            for col in range(self.col_count):
                cell = self.grid[row][col]
                if cell.height == 1:
                    found.append(cell)
        return found


def dijkstra_search(grid, cell):
    # Dijkstra Algorithm
    # Breadth first search, weighting each node as we visit them.

    # We hold a set of nodes we've visited, so we don't walk backwords.
    visited = set()

    # Parents map will contain:
    # child_node: parent_node
    # So given any node, we can ask this dict for it's parent.
    # That will let us walk back to our Starting Cell, which is *NOT* in this map.
    parents_map = dict()

    # Here we keep track of every node's cost from the Starting Cell.
    node_costs = collections.defaultdict(lambda: 1_000_000)

    # Staring node costs 0.
    node_costs[cell.node] = 0

    # Push this cost onto the heap.
    queue = []
    heap.heappush(queue, (0, cell.node))

    # Every edge costs 1.
    WEIGHT = 1
    while queue:
        _, node = heap.heappop(queue)
        visited.add(node)

        for neighbor in grid.neighbors(node):
            if neighbor.node in visited:
                continue

            new_cost = node_costs[node] + WEIGHT
            if node_costs[neighbor.node] > new_cost:
                parents_map[neighbor.node] = node
                node_costs[neighbor.node] = new_cost
                heap.heappush(queue, (new_cost, neighbor.node))

    return parents_map, node_costs


def part_1(data):
    grid = Grid(data)
    #print(grid)
    parents, costs = dijkstra_search(grid, grid.start)
    print(f'Part 1: from {grid.start.node} to {grid.end.node}: {costs[grid.end.node]}')


def part_2(data):
    grid = Grid(data)
    best = None
    for cell in grid.lowest():
        parents, costs = dijkstra_search(grid, cell)
        cell_cost = costs[grid.end.node]
        if best is None:
            best = (cell, cell_cost)
        elif cell_cost < best[1]:
            best = (cell, cell_cost)

    print(f'Part 2: from {best[0].node} to {grid.end.node}: {best[1]}')



def main(data):
    INPUT = [
        'Sabqponm',
        'abcryxxl',
        'accszExk',
        'acctuvwj',
        'abdefghi',
    ]
    part_1(data)
    part_2(data)


if __name__ == '__main__':
    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00input.txt
    with open(f'{stem}input.txt', mode='r+') as fp:
        data = [line.strip() for line in fp.readlines()]

    main(data)

