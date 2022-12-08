#!/usr/bin/env python3

import pathlib


def part_1(data):
    signal = data[0]
    signal_length = len(signal)

    marker = 0

    for i in range(3, signal_length):
        last_4 = signal[i-3:i+1]
        if len(set(last_4)) == 4:
            marker = i
            break

    print(f'Marker at {marker}: {last_4}')

    # for i in range(marker-10, marker+10):
    #     line = f'{i}: {signal[i]}'
    #     if i == marker:
    #         line += ' marker'
    #     print(line)

    processed = len(signal) - marker
    print(f'Part 1 Marker:        {marker}')


def part_2(data):
    signal = data[0]
    signal_length = len(signal)

    marker = 0

    for i in range(13, signal_length):
        last_14 = signal[i-13:i+1]
        if len(set(last_14)) == 14:
            marker = i
            break

    print(f'Marker at {marker}: {last_14}')

    # for i in range(marker-10, marker+10):
    #     line = f'{i}: {signal[i]}'
    #     if i == marker:
    #         line += ' marker'
    #     print(line)

    processed = len(signal) - marker
    print(f'Part 2 Marker:        {marker}')



def main(data):
    part_1(data)
    part_2(data)

if __name__ == '__main__':
    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00input.txt
    with open(f'{stem}input.txt', mode='r+') as fp:
        data = [line.strip() for line in fp.readlines()]

    main(data)

