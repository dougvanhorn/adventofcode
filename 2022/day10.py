#!/usr/bin/env python3

import pathlib


class CPU:
    def __init__(self):
        self.cycle = 1
        self.x = 1
        self.x_values = [1]

        self.crt = ['.'] * 240

    def __str__(self):
        return f'{self.cycle}: {self.x}'

    def print_screen(self):
        print(''.join(self.crt[0:40]))
        print(''.join(self.crt[40:80]))
        print(''.join(self.crt[80:120]))
        print(''.join(self.crt[120:160]))
        print(''.join(self.crt[160:200]))
        print(''.join(self.crt[200:240]))

    def part_1(self, data):
        for i, row in enumerate(data):
            #print(f'Cycle {self.cycle}')
            #print(f'  x = {self.x}')
            #print(f'  {row}')
            if row.startswith('addx'):
                addx, value = row.split(' ')
                self.tick()
                self.addx(int(value))
                self.tick()

            elif row.startswith('noop'):
                self.noop()
                self.tick()

            else:
                raise Exception(f'Bad instruction: {row}')

            #print(f'  {self.x}')

    def part_2(self, data):
        for i, row in enumerate(data):
            if row.startswith('addx'):
                addx, value = row.split(' ')

                self.draw()
                self.tick()
                self.draw()
                self.addx(int(value))
                self.tick()

            elif row.startswith('noop'):
                self.noop()
                self.draw()
                self.tick()

            else:
                raise Exception(f'Bad instruction: {row}')

            #print(f'  {self.x}')

    def draw(self):
        # x is the "sprite, 3 wide, so [x-1, x, x+1]"
        # during each cycle, we see if the cycle_i is in current_sprite.
        # if it is, we light that crt pixel self.crt[i] = '#'
        #print(f'Cycle: {self.cycle}')
        #print(f'  Sprite: {self.x}')
        line, mod_cycle = divmod(self.cycle-1, 40)
        #print(f'  Line: {line}, Mod: {mod_cycle}')
        sprite = (self.x - 1, self.x, self.x + 1)
        #sprite_display = ''.join(['#' if i in sprite else '.' for i in range(40)])
        #print(f'  Sprite {sprite}')
        #print(f'  {sprite_display}')

        #in_sprite = ['.'] * 80
        #in_sprite[self.cycle-1] = '?'
        #print(' ', ''.join(in_sprite[:40]))
        #if (self.cycle-1) in sprite:
        if mod_cycle in sprite:
            #print(f'  Ligthing pixel {self.cycle-1}')
            self.crt[self.cycle-1] = '#'

        #current_display = ''.join(self.crt[:40])
        #print(f'  {current_display}')

    def addx(self, value):
        self.x += value

    def noop(self):
        pass

    def tick(self):
        self.cycle += 1
        self.x_values.append(self.x)

    def answer(self):
        print(f'Total Cycles: {self.cycle}')

        #for i, x in enumerate(self.x_values):
        #    print(f'{i:03d}: {x}')

        total_value = 0
        for i in range(19, len(self.x_values), 40):
            print(f'self.x_values[{i+1}]: {self.x_values[i]}')
            total_value += (i+1) * self.x_values[i]

        print(f'Total Value: {total_value}')


def part_1(data):
    cpu = CPU()
    print('Part 1')
    cpu.part_1(data)
    cpu.answer()


def part_2(data):
    cpu = CPU()
    cpu.part_2(data)
    cpu.print_screen()


def main(data):
    INPUT = [
        'addx 15', 'addx -11', 'addx 6', 'addx -3', 'addx 5', 'addx -1', 'addx -8', 'addx 13', 'addx 4', 'noop',
        'addx -1', 'addx 5', 'addx -1', 'addx 5', 'addx -1', 'addx 5', 'addx -1', 'addx 5', 'addx -1', 'addx -35',
        'addx 1', 'addx 24', 'addx -19', 'addx 1', 'addx 16', 'addx -11', 'noop', 'noop', 'addx 21', 'addx -15',
        'noop', 'noop', 'addx -3', 'addx 9', 'addx 1', 'addx -3', 'addx 8', 'addx 1', 'addx 5', 'noop',
        'noop', 'noop', 'noop', 'noop', 'addx -36', 'noop', 'addx 1', 'addx 7', 'noop', 'noop',
        'noop', 'addx 2', 'addx 6', 'noop', 'noop', 'noop', 'noop', 'noop', 'addx 1', 'noop',
        'noop', 'addx 7', 'addx 1', 'noop', 'addx -13', 'addx 13', 'addx 7', 'noop', 'addx 1', 'addx -33',
        'noop', 'noop', 'noop', 'addx 2', 'noop', 'noop', 'noop', 'addx 8', 'noop', 'addx -1',
        'addx 2', 'addx 1', 'noop', 'addx 17', 'addx -9', 'addx 1', 'addx 1', 'addx -3', 'addx 11', 'noop',
        'noop', 'addx 1', 'noop', 'addx 1', 'noop', 'noop', 'addx -13', 'addx -19', 'addx 1', 'addx 3',
        'addx 26', 'addx -30', 'addx 12', 'addx -1', 'addx 3', 'addx 1', 'noop', 'noop', 'noop', 'addx -9',
        'addx 18', 'addx 1', 'addx 2', 'noop', 'noop', 'addx 9', 'noop', 'noop', 'noop', 'addx -1',
        'addx 2', 'addx -37', 'addx 1', 'addx 3', 'noop', 'addx 15', 'addx -21', 'addx 22', 'addx -6', 'addx 1',
        'noop', 'addx 2', 'addx 1', 'noop', 'addx -10', 'noop', 'noop', 'addx 20', 'addx 1', 'addx 2',
        'addx 2', 'addx -6', 'addx -11', 'noop', 'noop', 'noop',
    ]
    #part_1(data)
    part_2(data)


if __name__ == '__main__':
    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00input.txt
    with open(f'{stem}input.txt', mode='r+') as fp:
        data = [line.strip() for line in fp.readlines()]

    main(data)

