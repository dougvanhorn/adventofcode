#!/usr/bin/env python

import collections
import logging
import math
import pathlib

import rich
from rich.progress import track


logging.basicConfig(level=logging.DEBUG, format='%(message)s')
log = logging.getLogger('aoc')


def load_data():
    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00-input.txt
    with open(f'{stem}-input.txt', mode='r+') as fp:
        data = [line.strip('\n') for line in fp.readlines()]
    return data


def part_1(network):
    rich.print('[bold red]== Part 1 ==[/bold red]')
    rich.print('Find all paths from you to out.')

    answer = network.part_1()
    rich.print(f'[bold green]Answer: {answer}[/bold green]')


def part_2(network):
    rich.print('[bold red]== Part 2 ==[/bold red]')
    rich.print('Find all paths from svr to out which include dac an fft hosts.')

    answer = network.part_2()
    rich.print(f'[bold green]Answer: {answer}[/bold green]')


class Node:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Node({self.name})'


class Edge:
    def __init__(self, from_node, to_node):
        self.from_node = from_node
        self.to_node = to_node

    def __repr__(self):
        return f'Edge({self.from_node} -> {self.to_node})'


class Network:
    def __init__(self, data):
        self.nodes = {}
        self.edges = []

        self.hosts = collections.defaultdict(list)

        for row in data:
            host = row[0:3]
            connections = row[5:].split(' ')
            self.hosts[host] = connections

        # Build a graph of "inbound connections" per host.
        self.inbound= collections.defaultdict(list)
        for host, connections in self.hosts.items():
            for conn in connections:
                self.inbound[conn].append(host)

        # Build a count of inbound connections per host.
        self.inbound_counts = {
            host: len(inbound_connections)
            for host, inbound_connections in self.inbound.items()
        }

        # Build the list
        self.topological_order = []

        # This finds all hosts with no inbound connections.
        # Namely, svr.
        # Which is how they kept part 1 easy.
        hosts_no_inbound = [
            host
            for host in self.hosts
            if host not in self.inbound_counts or self.inbound_counts[host] == 0
        ]
        # we'll start with svr
        while hosts_no_inbound:
            # for all hosts that have no inbound connections
            # take the latest
            # loop over its outbound connections
            # decrement their inbound counts
            # if the inbound count drops to 0, add it to the hosts no inbound list.
            # this leaves us with an ordering of hosts
            # as you would encounter them traversing from svr to out.
            # we will use this sorting to help inform the sub-tree traversals in part 2.

            host = hosts_no_inbound.pop()
            self.topological_order.append(host)

            # Remove this host from all its outbound connections.
            for outbound in self.hosts[host]:
                # Reduce this connected outbound host's inbound count by 1.
                self.inbound_counts[outbound] -= 1
                # If the inbound host inbound count is now 0, then there
                # are no more paths to this host, so we can add it to sorted topo ordering.
                # This means that the topo order has hosts in the maximum distance from svr.
                if self.inbound_counts[outbound] == 0:
                    hosts_no_inbound.append(outbound)

    def part_1(self):
        # Find _all_ paths from you to out.
        # DFS?
        START = 'you'
        END = 'out'

        def dfs(host, path):
            # Base case, we've arrived at out.
            if host == END:
                return 1

            connections = self.hosts[host]
            new_path = path + [host]
            child_paths = 0
            for conn in connections:
                count = dfs(conn, new_path)
                child_paths += count

            return child_paths

        paths = dfs(START, [])
        return paths

    def part_2(self):
        # Courtesy of: https://github.com/romamik/aoc2025/blob/master/day11/day11p2.py
        # Reddit Thread: https://www.reddit.com/r/adventofcode/comments/1pjp1rm/2025_day_11_solutions/
        # Topological sort then multiple possibilities.
        # We sort the nodes as they will be visisted (topo sort)
        # Then we break the paths down into segments
        # Then we sum the paths through each segment.
        #   i need to understand this piece better.
        # The we multiply the segments together and sum the two possible routes.

        # Find _all_ paths from svr to out that include dac and fft.
        START = 'svr'
        FFT = 'fft'
        DAC = 'dac'
        END = 'out'

        # Count paths between two hosts using the topological order.
        def count_paths(start, end):
            path_counts = collections.defaultdict(int)

            # We use the topological sorted hosts to...
            start_index = self.topological_order.index(start)
            end_index = self.topological_order.index(end)

            # 1 path to the start.
            path_counts[start] = 1
            # Begin just after the start host, but include the end host.
            # The topo order lets us move from nearest to farthest from start.
            for host in self.topological_order[start_index + 1:end_index + 1]:
                # e.g., the host just after start...
                # we sum all the path counts from inbound connections to this host.
                # so for the second host, we'd sum "1" from path_counts[start]
                # and any other inbound connections to this host.
                # e.g., there are n-ways to this host.
                # Once we've looped over every host in the topo order, the end host
                # will have the total path counts from every previous host.
                path_counts[host] = sum(
                    path_counts[inbound_host]
                    for inbound_host in self.inbound[host]
                )
            return path_counts[end]

        # Two ways through the graph.
        svr2fft = count_paths(START, FFT)
        fft2dac = count_paths(FFT, DAC)
        dac2out = count_paths(DAC, END)

        svr2dac = count_paths(START, DAC)
        dac2fft = count_paths(DAC, FFT)
        fft2out = count_paths(FFT, END)

        total_paths = (svr2fft * fft2dac * dac2out) + (svr2dac * dac2fft * fft2out)
        return total_paths


def main(data):
    _data = [
        'aaa: you hhh',
        'you: bbb ccc',
        'bbb: ddd eee',
        'ccc: ddd eee fff',
        'ddd: ggg',
        'eee: out',
        'fff: out',
        'ggg: out',
        'hhh: ccc fff iii',
        'iii: out',
    ]
    # network = Network(data)
    # part_1(network)

    _data = [
        'svr: aaa bbb',
        'aaa: fft',
        'fft: ccc',
        'bbb: tty',
        'tty: ccc',
        'ccc: ddd eee',
        'ddd: hub',
        'hub: fff',
        'eee: dac',
        'dac: fff',
        'fff: ggg hhh',
        'ggg: out',
        'hhh: out',
    ]
    network = Network(data)
    part_2(network)


if __name__ == '__main__':
    data = load_data()
    main(data)
