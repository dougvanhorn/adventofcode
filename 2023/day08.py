#!/usr/bin/env python3

import collections
import math
import logging
import pathlib

logging.basicConfig(level=logging.DEBUG, format='%(message)s')


L = 'L'
R = 'R'


class Node:
    def __init__(self, s):
        self.name, edges = s.split(' = ')
        self.left, self.right = edges.replace('(', '').replace(')', '').split(', ')


    def __repr__(self):
        s = f'{self.name} = ({self.left}, {self.right})'
        return s

    def follow(self, rule):
        if rule == 'L':
            return self.left
        elif rule == 'R':
            return self.right
        raise ValueError(f'Invalid rule {rule} for node {self}.')

    @property
    def is_a_node(self):
        return self.name.endswith('A')

    @property
    def is_z_node(self):
        return self.name.endswith('Z')


class Instructions:
    def __init__(self, instructions):
        self.instructions = instructions

    def __iter__(self):
        while True:
            for rule in self.instructions:
                yield rule


class Map:
    def __init__(self, data):
        self.instructions = data[0]

        # Nodes keyed on name.
        self.nodes = {}
        for row in data[2:]:
            node = Node(row)
            self.nodes[node.name] = node

    def part1(self):
        """Follow the instructions, navigate the tree, until we arrive.
        """
        steps = 0
        next_node = self.nodes['AAA']

        followed = []
        followed.append(next_node)

        print(f'Starting at {next_node.name}.')

        rules = Instructions(self.instructions)
        for rule in rules:
            print(f'Current Node: {next_node}, Rule: {rule}')
            next_node_name = next_node.follow(rule)
            next_node = self.nodes[next_node_name]
            print(f'Moving to node {next_node.name}')
            followed.append(next_node)
            steps += 1
            if next_node.name == 'ZZZ':
                print(f'Arrived at {next_node.name} in round {steps}.')
                return steps

    def part2(self):
        steps = 0
        current_nodes = [
            node for node in self.nodes.values()
            if node.is_a_node
        ]

        print('=== Starting Nodes ===')
        for node in current_nodes:
            print(f'{node}')
        print('-'*79)

        found = []


        rules = Instructions(self.instructions)
        for rule in rules:
            steps += 1
            #print(f'  Step {steps}: {len(current_nodes)} current nodes.')
            next_nodes = [
                self.nodes[node.follow(rule)]  # follow gets me the next name, dict gets me the next node
                for node in current_nodes
            ]
            next_round = []
            for node in next_nodes:
                if node.is_z_node:
                    found.append((node, steps))
                else:
                    next_round.append(node)

            #print(f'  Arrived at {len(found)} nodes.')
            if not next_round:
                print('Arrived!')
                for answer in found:
                    print(f'{answer[0]}, Steps: {answer[1]}')

                lcm = math.lcm(*[answer[1] for answer in found])
                print(f'Least Common Multiple: {lcm}')
                return lcm
            current_nodes = next_round


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
    map = Map(data)
    print(map.instructions)
    print(map.nodes)
    steps = map.part1()
    print('Answer', steps)


def part_2(data):
    p('== Part 2 ==')
    map = Map(data)

    steps = map.part2()
    print('Answer', steps)


def main(data):
    _data = [
        'LLR',
        '',
        'AAA = (BBB, BBB)',
        'BBB = (AAA, ZZZ)',
        'ZZZ = (ZZZ, ZZZ)',
    ]
    # part_1(data)
    _data = [
        'LR',
        '',
        '11A = (11B, XXX)',
        '11B = (XXX, 11Z)',
        '11Z = (11B, XXX)',
        '22A = (22B, XXX)',
        '22B = (22C, 22C)',
        '22C = (22Z, 22Z)',
        '22Z = (22B, 22B)',
        'XXX = (XXX, XXX)',
    ]
    part_2(data)


if __name__ == '__main__':
    data = load_data()
    main(data)
