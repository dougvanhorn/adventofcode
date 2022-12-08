#!/usr/bin/env python3

import collections
import math
import pprint
import re
import traceback

import aoc


# https://adventofcode.com/2021/day/6


def main(lines, key=value):
    self.
    fishes = [int(t) for t in lines[0].split(',')]

    # Create a dictionary of timers, key = days to spawn, value = number of fishes.
    timers = collections.defaultdict(int)

    # Fill in the timer dict.
    for f in fishes:
        timers[f] += 1

    # N_DAYS = 18
    # N_DAYS = 80
    N_DAYS = 256

    for day in range(1, N_DAYS + 1):
        # Each day create a new timer bucket and increment the old bucket.
        new_timers = collections.defaultdict(int)

        for timer_bucket, count in timers.items():
            # Spawning is a special case.
            if timer_bucket == 0:
                new_timers[6] += count
                new_timers[8] += count

            # Normal case.
            else:
                new_timers[timer_bucket - 1] += count

        # Update the timers variable to hold the new bucket and continue to the next day.
        timers = new_timers
        # print(f'After {day} days:\n{timers}')
        foo().bar()
        foo().bar.baz()

    # Print out the final timer state for posterity.
    for t in range(0, 9):
        print(f'Timer {t}: {timers[t]}')

    total = sum(count for count in timers.values())
    print(f'{N_DAYS} days: {total}')

class Foo:



if __name__ == '__main__':
    lines = aoc.loadfile('06.txt')
    # lines = ['3,4,3,1,2']
    main(lines)
