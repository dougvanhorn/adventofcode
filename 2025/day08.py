#!/usr/bin/env python

import collections
import dataclasses
import itertools
import logging
import math
import pathlib

import rich
from rich.progress import track


logging.basicConfig(level=logging.DEBUG, format='%(message)s')
log = logging.getLogger('aoc')

# Null out print for full data set.
def _print(*args, **kwargs):
    pass
print = _print


def load_data():
    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00-input.txt
    with open(f'{stem}-input.txt', mode='r+') as fp:
        data = [line.strip('\n') for line in fp.readlines()]
    return data


def part_1(data):
    rich.print('[bold red]== Part 1 ==[/bold red]')
    rich.print('Connect first 1000 closest points into circuits.')

    combinations = [Pair(a, b) for a, b in itertools.combinations(data, 2)]
    print('Total combinations:', len(combinations))

    combinations.sort(key=lambda p: p.distance)
    # for pair in combinations[:11]:
    #     print(pair)

    circuits = []
    lookup = {}

    MAX_CONNECTIONS = 1000
    connections = 0
    for i, pair in enumerate(combinations):
        print(f'Processing pair {i}: {pair}')
        print(f'  Circuit count: {len(circuits)}')
        print('  Circuits:')
        for circuit in circuits:
            print(f'    {circuit.id}: {circuit.list_points()}')

        print('  Lookups:')
        for point in lookup:
            print(f'    Dict: {point} -> Circuit {lookup[point].id}')

        a_circuit = lookup.get(pair.a)
        b_circuit = lookup.get(pair.b)
        if a_circuit:
            print(f'  {pair.a} IN {a_circuit}')
        if b_circuit:
            print(f'  {pair.b} IN {b_circuit}')

        if a_circuit and b_circuit:
            if a_circuit is b_circuit:
                # Pair exists within same circuit, add it.
                print(f'  SKIP: {pair} already in {a_circuit}')
                a_circuit.add_pair(pair)
                connections += 1

            else:
                # Pair exsist in two different circuits, merge them.
                print(f'  MERGE: {pair} circuits {a_circuit.id} and {b_circuit.id}')
                # Merge circuits, move b into a.
                print("    Pairs in A:", len(a_circuit.pairs))
                print("    Pairs in B:", len(b_circuit.pairs))
                for p in b_circuit.pairs:
                    # Add into a.
                    a_circuit.add_pair(p)
                    # update lookup
                    lookup[p.a] = a_circuit
                    lookup[p.b] = a_circuit
                # Remove b circuit, it exists within a.
                circuits.remove(b_circuit)

                # Finally, add the new pair.
                a_circuit.add_pair(pair)
                print("    Pairs in A after merge:", len(a_circuit.pairs))
                connections += 1

        elif a_circuit or b_circuit:
            # Add this pair to an existing circuit.
            circuit = a_circuit or b_circuit
            print(f'  JOIN: {pair} to {circuit}')
            circuit.add_pair(pair)
            lookup[pair.a] = circuit
            lookup[pair.b] = circuit
            connections += 1

        else:
            # Create a new circuit.
            circuit = Circuit()
            print(f'  NEW {pair} to {circuit}')
            circuit.add_pair(pair)
            lookup[pair.a] = circuit
            lookup[pair.b] = circuit
            circuits.append(circuit)
            connections += 1

        print(f'  Connections made: {connections}')
        print()
        if connections >= MAX_CONNECTIONS:
            break

    print('Total circuits:', len(circuits))

    for circuit in circuits:
        print(circuit)
        print('  Points:')
        for point in circuit.points:
            print(f'    {point}')
        print('  Pairs:')
        for pair in circuit.pairs:
            print(f'    {pair}')
        print()

    sizes = [circuit.size for circuit in circuits]
    sizes.sort(reverse=True)
    print(f'Circuit sizes: {sizes}')
    answer = math.prod(sizes[:3])
    rich.print(f'[bold green]Answer: {answer}[/bold green]')


def part_2(points):
    rich.print('[bold red]== Part 2 ==[/bold red]')
    rich.print('Connect until there is one circuit.')

    # Keep track of all points.
    combinations = [Pair(a, b) for a, b in itertools.combinations(points, 2)]
    print('Total points:', len(points))
    print('Total combinations:', len(combinations))

    combinations.sort(key=lambda p: p.distance)

    circuits = []
    lookup = {}

    point_pool = set(points)
    for i, pair in enumerate(combinations):
        print(f'Processing pair {i}: {pair}')
        print(f'  Circuit count: {len(circuits)}')
        print('  Circuits:')
        for circuit in circuits:
            print(f'    {circuit.id}: {circuit.list_points()}')

        print('  Lookups:')
        for point in lookup:
            print(f'    Dict: {point} -> Circuit {lookup[point].id}')

        a_circuit = lookup.get(pair.a)
        b_circuit = lookup.get(pair.b)
        if a_circuit:
            print(f'  {pair.a} IN {a_circuit}')
        if b_circuit:
            print(f'  {pair.b} IN {b_circuit}')

        if a_circuit and b_circuit:
            if a_circuit is b_circuit:
                # Pair exists within same circuit, add it.
                print(f'  SKIP: {pair} already in {a_circuit}')
                a_circuit.add_pair(pair)

            else:
                # Pair exsist in two different circuits, merge them.
                print(f'  MERGE: {pair} circuits {a_circuit.id} and {b_circuit.id}')
                # Merge circuits, move b into a.
                print("    Pairs in A:", len(a_circuit.pairs))
                print("    Pairs in B:", len(b_circuit.pairs))
                for p in b_circuit.pairs:
                    # Add into a.
                    a_circuit.add_pair(p)
                    # update lookup
                    lookup[p.a] = a_circuit
                    lookup[p.b] = a_circuit
                # Remove b circuit, it exists within a.
                circuits.remove(b_circuit)

                # Finally, add the new pair.
                a_circuit.add_pair(pair)
                print("    Pairs in A after merge:", len(a_circuit.pairs))

        elif a_circuit or b_circuit:
            # Add this pair to an existing circuit.
            circuit = a_circuit or b_circuit
            print(f'  JOIN: {pair} to {circuit}')
            circuit.add_pair(pair)
            lookup[pair.a] = circuit
            lookup[pair.b] = circuit

        else:
            # Create a new circuit.
            circuit = Circuit()
            print(f'  NEW {pair} to {circuit}')
            circuit.add_pair(pair)
            lookup[pair.a] = circuit
            lookup[pair.b] = circuit
            circuits.append(circuit)

        # Pair has been connected in some way, remove from point pool.
        try:
            point_pool.remove(pair.a)
        except KeyError:
            pass
        try:
            point_pool.remove(pair.b)
        except KeyError:
            pass

        # When the point pool is empty AND the circuit count is 1, we're done.
        if not point_pool and len(circuits) == 1:
            print('All points connected into a single circuit.')
            # Which means we just connected the last circuit.
            # So we need to print out the a.x and b.x product.
            answer = pair.a.x * pair.b.x
            rich.print(f'[bold green]Answer: {answer}[/bold green]')
            return


class Point:
    def __init__(self, str):
        self.x, self.y, self.z = [int(n) for n in str.split(',')]

    def __str__(self):
        return f'({self.x},{self.y},{self.z})'

    def __repr__(self):
        return self.__str__()


class Pair:
    def __init__(self, a: Point, b: Point):
        self.a = a
        self.b = b
        self.distance = self._eclidean_distance()

    def __str__(self):
        return f'{self.a} <-> {self.b}: {self.distance:.3f}'

    def __repr__(self):
        return self.__str__()

    def _eclidean_distance(self):
        return math.sqrt(
            (self.a.x - self.b.x) ** 2 +
            (self.a.y - self.b.y) ** 2 +
            (self.a.z - self.b.z) ** 2
        )


class Circuit:
    circuit_counter = 0
    def __init__(self):
        self.pairs = []
        self.id = Circuit.circuit_counter
        Circuit.circuit_counter += 1

    def __str__(self):
        return f'Circuit {self.id}: {self.size}'

    def __repr__(self):
        return self.__str__()

    @property
    def points(self):
        points = set()
        for pair in self.pairs:
            points.add(pair.a)
            points.add(pair.b)
        return list(points)

    @property
    def size(self):
        return len(self.points)

    def add_pair(self, pair: Pair):
        self.pairs.append(pair)

    def list_points(self):
        points = ', '.join(str(p) for p in self.points)
        return points

def main(data):
    _data = [
        '162,817,812',
        '57,618,57',
        '906,360,560',
        '592,479,940',
        '352,342,300',
        '466,668,158',
        '542,29,236',
        '431,825,988',
        '739,650,466',
        '52,470,668',
        '216,146,977',
        '819,987,18',
        '117,168,530',
        '805,96,715',
        '346,949,466',
        '970,615,88',
        '941,993,340',
        '862,61,35',
        '984,92,344',
        '425,690,689',
    ]
    points = [Point(str) for str in data]
    # part_1(points)
    part_2(points)


if __name__ == '__main__':
    data = load_data()
    main(data)
