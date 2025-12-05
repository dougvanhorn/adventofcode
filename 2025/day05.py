#!/usr/bin/env python

import collections
import logging
import math
import pathlib


import rich
from rich.progress import track

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


def part_1(spans, skus):
    rich.print('[bold red]== Part 1 ==[/bold red]')
    rich.print('Find skus that are in any range.')
    fresh = []
    for sku in track(skus, description="Processing SKUs..."):
        for span in spans:
            if span.contains(sku):
                fresh.append(sku)
                break

    rich.print(f'[bold green]Fresh SKUs: {len(fresh)}[/bold green]')



def part_2(spans, skus):
    rich.print('[bold red]== Part 2 ==[/bold red]')
    rich.print('Find count of all fresh skus.')

    # sort ranges
    spans.sort(key=lambda r: r.start)

    merged_spans = []
    merged_spans.append(spans[0])

    for span in track(spans[1:], description='Merging spans...'):
        # rich.print(f'Span: {span}')
        # Check for overlap with previous range.
        previous_span = merged_spans[-1]
        if previous_span.end + 1 >= span.start:  # Add 1 to allow touching ranges.
            # rich.print(f' Overlaps with previous span: {previous_span}')
            previous_span.merge(span)
        else:
            merged_spans.append(span)

    # rich.print('[bold blue]Merged Spans:[/bold blue]')
    # for span in merged_spans:
    #     rich.print(f'  {span}')

    sku_count = sum(span.size for span in merged_spans)
    rich.print(f'[bold green]Total fresh SKUs: {sku_count}[/bold green]')


class Span:
    def __init__(self, range_str):
        parts = range_str.split('-')
        self.start = int(parts[0])
        self.end = int(parts[1])

    def __repr__(self):
        return f'Span({self.start}-{self.end})'

    def __str__(self):
        return f'Span({self.start}-{self.end})'

    def contains(self, value):
        return self.start <= value <= self.end

    def merge(self, other):
        self.start = min(self.start, other.start)
        self.end = max(self.end, other.end)

    @property
    def size(self):
        return self.end - self.start + 1


def main(data):
    _data = [
        '3-5',
        '10-14',
        '16-20',
        '12-18',
        '',
        '1',
        '5',
        '8',
        '11',
        '17',
        '32',
    ]
    delimit = data.index('')

    spans = [
        Span(range_str)
        for range_str in data[:delimit]
    ]

    skus = [
        int(sku)
        for sku in data[delimit+1:]
    ]
    # part_1(spans, skus)
    part_2(spans, skus)


if __name__ == '__main__':
    data = load_data()
    main(data)
