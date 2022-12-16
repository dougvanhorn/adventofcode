#!/usr/bin/env python3

import collections
import math
import logging
import pathlib
import re

logging.basicConfig(level=logging.ERROR, format='%(message)s')

class Sensor:
    @staticmethod
    def from_input(data):
        match = re.match(
            r'Sensor at x=(?P<sensor_x>-?\d+), y=(?P<sensor_y>-?\d+): closest beacon is at x=(?P<beacon_x>-?\d+), y=(?P<beacon_y>-?\d+)',
            data,
        )
        sensor = Sensor(
            int(match['sensor_x']),
            int(match['sensor_y']),
            int(match['beacon_x']),
            int(match['beacon_y']),
        )
        return sensor

    def __init__(self, sensor_x, sensor_y, beacon_x, beacon_y):
        self.sensor_x = sensor_x
        self.sensor_y = sensor_y
        self.beacon_x = beacon_x
        self.beacon_y = beacon_y
        self.distance_x = abs(self.sensor_x - self.beacon_x)
        self.distance_y = abs(self.sensor_y - self.beacon_y)
        self.distance = self.distance_x + self.distance_y
        self.top = sensor_y - self.distance
        self.bottom = sensor_y + self.distance
        self.left = sensor_x - self.distance
        self.right = sensor_x + self.distance

    def __str__(self):
        return f'S:{self.sensor_point} B:{self.beacon_point} D:{self.distance}'

    @property
    def sensor_point(self):
        return (self.sensor_x, self.sensor_y)

    @property
    def beacon_point(self):
        return (self.beacon_x, self.beacon_y)

    def calculate_distance(self, x, y):
        d_x = abs(x - self.sensor_x)
        d_y = abs(y - self.sensor_y)
        return d_x + d_y

    def in_range(self, x, y):
        d_x = abs(x - self.sensor_x)
        d_y = abs(y - self.sensor_y)
        #check_distance = self.calculate_distance(x, y)
        check_distance = d_x + d_y
        is_in_range = (check_distance <= self.distance)
        #if is_in_range:
            #print(f'D: {check_distance} <= {self.distance} Checking ({x}, {y}) in range of {self}')
        #    pass

        return is_in_range

    def behind(self, x, y):
        # if the sensor is out of range to the left.
        if (self.calculate_distance(x, y) > self.distance) and (x < self.sensor_x):
            return False
        else:
            return True

def debug(message):
    log = logging.getLogger('aoc')
    log.debug(message)


def part_1(data, y):
    debug('== Part 1 ==')
    sensors = [Sensor.from_input(row) for row in data]
    for sensor in sensors:
        print(sensor)

    all_x = [s.sensor_x for s in sensors]
    all_x.extend([s.beacon_x for s in sensors])
    min_x = min(all_x)
    max_x = max(all_x)

    beacon_points = set(sensor.beacon_point for sensor in sensors)
    sensor_points = set(sensor.sensor_point for sensor in sensors)
    all_things = beacon_points.union(sensor_points)

    # given a sensor, it's range at row y is 
    #dy = (sensor.sensor_y - y)
    #left = sensor.sensor_x - dy
    #right = sensor.sensor_x + dy

    sensor_ranges_at_y = []
    print(f'CALCULATING X ranges at y={y}')
    print('='*79)
    for sensor in sensors:
        print(f'Sensor: {sensor}')
        min_y = sensor.sensor_y - sensor.distance
        max_y = sensor.sensor_y + sensor.distance
        print(f'    min, max y: {min_y}, {max_y}')
        if min_y > y or max_y < y:
            # max_y is above y, min_y is below y.
            print(f'    skipping {sensor}, {min_y} and {max_y} ')
            # skip, our y level is further away than our distance can rea
            continue

        # We can get to our y level, let's calculate how far we can move left and right.
        d = sensor.distance
        dy = abs(sensor.sensor_y - y)
        remaining_d = sensor.distance - dy
        print(f'    dy: {dy}')
        print(f'    remaining_d: {remaining_d}')
        left = sensor.sensor_x - remaining_d
        right = sensor.sensor_x + remaining_d
        print(f'    left: {left}')
        print(f'    right: {right}')
        sensor_ranges_at_y.append((left, right, sensor))

    sensor_ranges_at_y.sort(key=lambda t: (t[0], t[1]))
    print(f'Sorted segments:')
    for left, right, sensor in sensor_ranges_at_y:
        print(f'({left}, {right})  {sensor}')

    segments = []
    current_segment = (sensor_ranges_at_y[0][0], sensor_ranges_at_y[0][1]) 
    for seg_left, seg_right, sensor in sensor_ranges_at_y[1:]:
        #print(f'Comparing ({seg_left}, {seg_right}) left to {current_segment}s right')
        if seg_left <= current_segment[1]:
            # New segment starts within current segment, make the right side the max of the two.
            old_segment = current_segment
            current_segment = (current_segment[0], max(current_segment[1], seg_right))
            #print(f'   extending {old_segment} to {current_segment}')
            continue

        if seg_left > current_segment[1]:
            segments.append(current_segment)
            current_segment = (seg_left, seg_right)
    
    print(f'Final segments: {current_segment}, {segments}')
    range_count = abs(current_segment[0] - current_segment[1]) + 1
    print(range_count)
    for thing in all_things:
        print('thing', thing)
        if (thing[1] == y) and (current_segment[0] <= thing[0] <= current_segment[1]):
            range_count -= 1

    print(range_count)


def part_2(data, size):
    debug('== Part 2 ==')
    # Courtesy of:  https://www.youtube.com/watch?v=DtnvoqZZqJ0
    sensors = [Sensor.from_input(row) for row in data]
    #for s in sensors:
    #    print(f'{s.top:2d}, {s.bottom:2d}, {s.left:2d}, {s.right:2d}')

    for Y_LEVEL in range(0, size+1):
        if (Y_LEVEL % 500000) == 0:
            print(Y_LEVEL)

        ranges = []
        for s in sensors:
            # Test if this sensor is covering this y level.
            if s.top <= Y_LEVEL and s.bottom >= Y_LEVEL:
                dy = abs(Y_LEVEL - s.sensor_y)
                # it is, so add the range it covers at this y level.
                ranges.append([s.left + dy, s.right - dy])

        #print(f'For {Y_LEVEL}:')
        #print(f'Ranges: {ranges}')
        left = 0
        right = 0
        # collapse the ranges.
        while left < len(ranges):
            while right < len(ranges):
                if left == right:
                    continue  # skip self compare

                Lleft, Lright = ranges[left]  # left segment left and right
                Rleft, Rright = ranges[right]  # right segment left and right
                # check for overlap
                #print(f'Comparing {ranges[left]} and {ranges[right]}')
                # if the rhs of the left segment is bigger than the lhs of the right segment
                #   read: the left segment sticks into the right
                # or the rhs of the right segment is bigger than the lhs of the left segment
                #   read: the right segment sticks into the left
                if (Lright >= Rleft) and (Rright >= Lleft):
                    merged = [min(Lleft, Rleft), max(Lright, Rright)]
                    #print(f'    merged {merged}')
                    del ranges[max(left, right)]
                    del ranges[min(left, right)]
                    ranges.append(merged)
                    # Reset comparisons to 0
                    left = 0
                    right = -1
                right += 1
                #print(f'Ranges: {ranges}  Left: {left}  Right {right}')
            left += 1

        if len(ranges) == 2:
            print(Y_LEVEL, ranges)


def main(data):
    INPUT = [
        'Sensor at x=2, y=18: closest beacon is at x=-2, y=15',
        'Sensor at x=9, y=16: closest beacon is at x=10, y=16',
        'Sensor at x=13, y=2: closest beacon is at x=15, y=3',
        'Sensor at x=12, y=14: closest beacon is at x=10, y=16',
        'Sensor at x=10, y=20: closest beacon is at x=10, y=16',
        'Sensor at x=14, y=17: closest beacon is at x=10, y=16',
        'Sensor at x=8, y=7: closest beacon is at x=2, y=10',
        'Sensor at x=2, y=0: closest beacon is at x=2, y=10',
        'Sensor at x=0, y=11: closest beacon is at x=2, y=10',
        'Sensor at x=20, y=14: closest beacon is at x=25, y=17',
        'Sensor at x=17, y=20: closest beacon is at x=21, y=22',
        'Sensor at x=16, y=7: closest beacon is at x=15, y=3',
        'Sensor at x=14, y=3: closest beacon is at x=15, y=3',
        'Sensor at x=20, y=1: closest beacon is at x=15, y=3',
    ]
    #part_1(INPUT, 10)
    #part_1(data, 2_000_000)
    #part_2(INPUT, 20)
    part_2(data, 4000000)


if __name__ == '__main__':
    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00input.txt
    with open(f'{stem}input.txt', mode='r+') as fp:
        data = [line.strip() for line in fp.readlines()]

    main(data)

