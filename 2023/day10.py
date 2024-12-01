#!/usr/bin/env python3

import collections
import logging
import math
import pathlib
import operator


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


NS = '|'
EW = '-'
NE = 'L'
NW = 'J'
SW = '7'
SE = 'F'
G = '.'
START = 'S'

class Pipe:
    """
    | is a vertical pipe connecting north and south.
    - is a horizontal pipe connecting east and west.
    L is a 90-degree bend connecting north and east.
    J is a 90-degree bend connecting north and west.
    7 is a 90-degree bend connecting south and west.
    F is a 90-degree bend connecting south and east.
    . is ground; there is no pipe in this tile.
    S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
    """
    def __init__(self, pipe, coords, size):
        self.pipe_type = pipe
        self.row, self.col = coords 
        self.coords = coords
        self.max_rows, self.max_cols = size

        self.is_start = (pipe == START)

    def __str__(self):
        return self.pipe_type

    def __repr__(self):
        s = f'{self.pipe_type}: ({self.row}, {self.col})'
        return s

    def _is_valid_coord(self, coord):
        if not (0 <= coord[0] < self.max_rows):
            return False
        if not (0 <= coord[1] < self.max_cols):
            return False
        return True

    def adjacent(self):
        north = (self.row - 1, self.col)
        south = (self.row + 1, self.col)
        east = (self.row, self.col + 1)
        west = (self.row, self.col - 1)

        if self.pipe_type == NS:
            pipes = [coord for coord in (north, south) if self._is_valid_coord(coord)]
            return pipes

        if self.pipe_type == EW:
            pipes = [coord for coord in (east, west) if self._is_valid_coord(coord)]
            return pipes

        if self.pipe_type == NE:
            pipes = [coord for coord in (north, east) if self._is_valid_coord(coord)]
            return pipes

        if self.pipe_type == NW:
            pipes = [coord for coord in (north, west) if self._is_valid_coord(coord)]
            return pipes

        if self.pipe_type == SE:
            pipes = [coord for coord in (south, east) if self._is_valid_coord(coord)]
            return pipes

        if self.pipe_type == SW:
            pipes = [coord for coord in (south, west ) if self._is_valid_coord(coord)]
            return pipes

        return []


class Map:
    def __init__(self, data):
        self.data = data
        self.size = (len(data), len(data[0]))
        self.max_rows, self.max_cols = self.size
        self.pipes = []
        self.start = None

        self.by_coord = {}

        for i, row in enumerate(self.data):
            pipe_row = []
            self.pipes.append(pipe_row)
            for j, pipe_char in enumerate(row):
                pipe = Pipe(pipe_char, (i, j), self.size)
                pipe_row.append(pipe)
                self.by_coord[(i, j)] = pipe
                if pipe_char == START:
                    self.start = pipe

        above_row = self.start.row - 1
        below_row = self.start.row + 1
        left_col = self.start.col - 1
        right_col = self.start.col + 1

        adjacent = []
        if above_row >= 0:
            pipe = self.pipes[above_row][self.start.col]
            # North of me, check for S connections.
            if pipe.pipe_type in (NS, SE, SW):
                adjacent.append(pipe)

        if below_row < self.max_rows:
            pipe = self.pipes[below_row][self.start.col]
            # South of me, check for N connections
            if pipe.pipe_type in (NS, NE, NW):
                adjacent.append(pipe)

        if left_col >= 0:
            pipe = self.pipes[self.start.row][left_col]
            # West of me, check for E connections
            if pipe.pipe_type in (EW, NE, SE):
                adjacent.append(pipe)

        if right_col < self.max_cols:
            pipe = self.pipes[self.start.row][right_col]
            # East of me, check for W connections
            if pipe.pipe_type in (EW, NW, SW):
                adjacent.append(pipe)

        self.start_adjacent = adjacent

    def __str__(self):
        output = []
        output.append('-'*79)
        for row in self.pipes:
            output.append(''.join(str(pipe) for pipe in row))

        output.append('')
        output.append(f'START: {repr(self.start)}')
        output.append('-'*79)
        return '\n'.join(output)

    def walk_loop(self):
        path = [self.start]
        visited = {self.start: True}

        from_pipe = self.start
        current_pipe = self.start_adjacent[0]
        path.append(current_pipe)
        visited[current_pipe] = True

        rounds = 20
        i = 0
        while True:
            
            print('Step')
            print('-'*79)
            i += 1
            if i > 20:
                print('too many, breaking.')
                break

            print(f'current pipe: {repr(current_pipe)}')
            print(f'from pipe: {repr(from_pipe)}')
            # Every pipe has two connections.
            adjacent = current_pipe.adjacent()

            next_coord = [coord for coord in adjacent if coord != from_pipe.coords][0]

            _pipe = self.by_coord[next_coord]
            print(f'next pipe: {repr(_pipe)}')

            if _pipe.pipe_type == START:
                print('found start, quitting.')
                break

            # Move to the next pipe.
            print(f'moving to {repr(_pipe)}.')
            path.append(_pipe)
            visited[_pipe] = True
            from_pipe = current_pipe
            current_pipe = _pipe

            print()
            print()


        print('Loop completed.')
        print(f'Length: {len(path)}')
        for i, pipe in enumerate(path):
            print(f'{i}: {repr(pipe)}')


    def flow(self):
        pipe1_path = [self.start]
        pipe2_path = [self.start]

        # two starting positions.
        pipe1= self.start_adjacent[0]
        pipe1.last_pipe = self.start
        pipe1_path.append(pipe1)

        pipe2 = self.start_adjacent[1]
        pipe2.last_pipe = self.start
        pipe2_path.append(pipe2)

        def _next_pipe(current_pipe, last_pipe):
            adjacent = current_pipe.adjacent()
            coords = [
                coord for coord in adjacent
                if coord != last_pipe.coords
            ]
            return self.by_coord[coords[0]]
        
        steps = 1
        while pipe1 != pipe2:
            next1 = _next_pipe(pipe1, pipe1.last_pipe)
            next1.last_pipe = pipe1
            pipe1_path.append(next1)
            pipe1 = next1

            next2 = _next_pipe(pipe2, pipe2.last_pipe)
            next2.last_pipe = pipe2
            pipe2_path.append(next2)
            pipe2 = next2

            steps += 1

            #if steps > 
            #    print('too many steps')
            #    break


        self.path = pipe1_path
        rpath = pipe2_path[1:-1]
        rpath.reverse()
        self.path.extend(rpath)
        return steps


def part_1(data):
    p('== Part 1 ==')
    land = Map(data)
    #print(land)
    steps = land.flow()
    print('Answer', steps)

def part_2(data):
    p('== Part 2 ==')
    land = Map(data)
    land.flow()
    print(land)
    for i, pipe in enumerate(land.path):
        print(f'{i}: {repr(pipe)}')

    print('-'*79)
    print('loop')
    pipe_set = {pipe for pipe in land.path}
    for row in land.pipes:
        chars = []
        for pipe in row:
            c = 'x' if pipe in pipe_set else ' '
            chars.append(c)
        print(''.join(chars))


    pipes_by_row = collections.defaultdict(list)
    pipes_by_col = collections.defaultdict(list)
    for pipe in land.path:
        pipes_by_row[pipe.row].append(pipe)
        pipes_by_col[pipe.col].append(pipe)

    # find space between rows
    horizontal_space = set()
    for row, pipes in pipes_by_row.items():
        pipes.sort(key=operator.attrgetter('coords'))
        print('-'*79)
        print(f'row {row}: {pipes}')

        cols = [pipe.col for pipe in pipes]
        diffs = [cols[i+1]-cols[i] for i in range(0, len(cols)-1)]
        print(diffs)

        breakpoints = [0]
        for index, diff in enumerate(diffs, start=1):
            if diff != 1:
                breakpoints.append(index)

        print('breakpoint indexes', breakpoints)




        continue

        left = 0
        while left < len(cols):
            for i, diff in enumerate(diffs[left:]):
                if diff != 1:
                    right = i
                    print(f'range: {cols[left]}, {cols[right]}')
                    left = i+1
                    break


        continue

        span = (cols[0], cols[1])
        left = 0
        last_pipe = left
        while (left < len(cols) - 1):
            while right < len(cols) - 1:
                right = last_pipe + 1
                diff = cols[right] - cols[last_pipe]
            if diff > 1:
                print(f'  range({cols[left]}, {cols[right]})')
                left = right + 1
            else:
                last_pipe = right

            right = left
            print(f'left: {left}: {cols[left]}, right: {right}: {cols[right]}')
            diff = cols[right+1] - cols[right]
            # the next value to the right is one bigger than current.
            if diff == 1:
                right = right + 1
                if (right) >= (len(cols)):
                    # We're at the end of the cols, close out the span.
                    print(f'  range({cols[left]}, {cols[right]})')
                    break
                continue
            # the next value to the right is bigger than one
            else:
                print(f'  range({cols[left]}, {cols[right]})')
                left = right + 1
                right = left + 1

        #print(f'range({cols[left]}, {cols[right]})')
        

def main(data):
    _data = [
        '7-F7-',
        '.FJ|7',
        'SJLL7',
        '|F--J',
        'LJ.LJ',
    ]
    _data = [
        '...........',
        '.S-------7.',
        '.|F-----7|.',
        '.||.....||.',
        '.||.....||.',
        '.|L-7.F-J|.',
        '.|..|.|..|.',
        '.L--J.L--J.',
        '...........',
    ]
    # part_1(data)
    part_2(_data)


if __name__ == '__main__':
    data = load_data()
    main(data)
