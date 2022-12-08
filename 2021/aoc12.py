#!/usr/bin/env python3

import collections
import math
import pathlib
import pprint
import re
import traceback

import aoc


# https://adventofcode.com/2021/day/12

class Node:
    def __init__(self, name):
        self.name = name
        self.lowercase = name.islower()
        self.edges = []
        self.start = name == 'start'
        self.end = name == 'end'

    def __str__(self):
        edge_list = ', '.join([node.name for node in self.edges])
        return f'Node({self.name}) | Edges({edge_list})'

    def __repr__(self):
        return self.__str__()


class Edge:
    def __init__(self, left_node, right_node):
        self.left_node = left_node
        self.right_node = right_node


class Graph:
    def __init__(self):
        self.start = None
        self.end = None
        self.nodes = {}

    def __str__(self):
        strings = []
        for i, (name, node) in enumerate(self.nodes.items()):
            strings.append(f'{i:>2}: {node}')
        return '\n'.join(strings)

    @classmethod
    def from_input(cls, input_lines):
        graph = cls()

        # input is an edge nodename-nodename
        for line in input_lines:
            left, right = line.split('-')

            left_node = graph.nodes.setdefault(left, Node(left))
            right_node = graph.nodes.setdefault(right, Node(right))

            left_node.edges.append(right_node)
            right_node.edges.append(left_node)

            graph.nodes[left_node.name] = left_node

        graph.start = graph.nodes['start']
        graph.end = graph.nodes['end']

        for node in graph.nodes.values():
            node.edges.sort(key=lambda n: n.name)

        return graph

    def find_paths(self, allow_two_visits=False):
        paths = []

        def depth_first(node, current_path, visited, depth=0):
            # We're here, add us to the path.
            current_path.append(node)

            # Base Case 1: the end.
            if node.end:
                # Copy the current path out to our global.
                paths.append(list(current_path))
                current_path.pop()
                return

            if node.lowercase:
                # Keep a set of lowercase nodes that we've visted.
                visited[node.name] += 1

            for edge in node.edges:
                if edge.start:
                    continue

                # We've visited the edge...
                elif visited[edge.name] > 0:
                    # If we've visited any node twice already, skip this node.
                    twos = [count for count in visited.values() if count >= 2]
                    if any(twos):
                        continue

                # Forge ahead.
                depth_first(edge, current_path, visited, depth=depth+1)

            # Unwind.
            current_path.pop()
            if node.lowercase and not node.start:
                visited[node.name] -= 1

        current_path = collections.deque()
        visited = collections.defaultdict(int)
        depth_first(self.start, current_path, visited)

        for i, row in enumerate(paths, 1):
            path_string = ','.join(node.name for node in row)
            print(f'{i:>3}: {path_string}')


def part_1(input_lines):
    graph = Graph.from_input(lines)
    print('## Graph')
    print('-' * 79)
    print(str(graph))
    print('-' * 79)
    print('## Paths')
    graph.find_paths()
    print('-' * 79)


def part_2(input_lines):
    graph = Graph.from_input(lines)
    print('## Graph')
    print('-' * 79)
    print(str(graph))
    print('-' * 79)
    print('## Paths')
    graph.find_paths()
    print('-' * 79)


def main(input_lines):
    #print('Part 1')
    #print('=' * 79)
    #part_1(input_lines)

    print()
    print()
    print('Part 2')
    print('=' * 79)
    part_2(input_lines)


# 10
#     start
#     /   \
# c--A-----b--d
#     \   /
#      end
INPUT_1 = [
    'start-A',
    'start-b',
    'A-c',
    'A-b',
    'b-d',
    'A-end',
    'b-end',
]

# 19
INPUT_2 = [
    'dc-end',
    'HN-start',
    'start-kj',
    'dc-start',
    'dc-HN',
    'LN-dc',
    'HN-end',
    'kj-sa',
    'kj-HN',
    'kj-dc',
]

# 226
INPUT_3 = [
    'fs-end',
    'he-DX',
    'fs-he',
    'start-DX',
    'pj-DX',
    'end-zg',
    'zg-sl',
    'zg-pj',
    'pj-he',
    'RW-he',
    'fs-DX',
    'pj-RW',
    'zg-RW',
    'start-pj',
    'he-WI',
    'zg-he',
    'pj-fs',
    'start-RW',
]

if __name__ == '__main__':
    path = pathlib.Path(__file__)
    day_number = path.name[3:5]
    filename = f'{day_number}.txt'
    lines = aoc.loadfile(filename)
    _lines = INPUT_3
    n = len(lines)
    print(aoc.format(f'Loaded {filename}: {n} lines.', 'blue'))
    main(lines)
