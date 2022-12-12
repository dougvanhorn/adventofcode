#!/usr/bin/env python3

import pathlib
import re


class Compiler:
    def __init__(self, input):
        self.input = input
        self.monkeys = []
        self.common_modulus = 1

    def compile(self):
        # As we loop over lines, we need to 

        # Find locations of each new monkey definition.
        monkey_indexes = [
            i for i, line in enumerate(self.input)
            if line.startswith('Monkey')
        ]
        # Add a final index of None for later slicing.
        monkey_indexes.append(None)

        self.monkeys = []
        for i, input_index in enumerate(monkey_indexes[:-1]):
            start_line = input_index
            end_line = monkey_indexes[i+1]
            monkey = Monkey(self.input[start_line:end_line])
            self.monkeys.append(monkey)
            self.common_modulus *= monkey.divisible_by

    def run(self, rounds=1, reduce_worry=lambda x: x):
        for round in range(1, rounds+1):
            #print(f'=== Round {round} ===')
            #print('='*79)
            for monkey in self.monkeys:
                #print('-'*79)
                #print(f'Monkey {monkey.monkey_id}')
                #print('-'*79)
                for worry_level in monkey.item_list:
                    #print(f'  Monkey inspects an item with a worry level of {worry_level}')
                    #print(f'  Operation {monkey.operation_value} {monkey.operation} {worry_level}')

                    calculated_worry = monkey.inspect_item(worry_level, reduce_worry=reduce_worry)
                    throw_to_monkey = monkey.get_throw_to(calculated_worry)
                    #print(f'  Item with worry level {calculated_worry} is throw to monkey {throw_to_monkey}.')
                    
                    next_monkey = self.monkeys[throw_to_monkey] 
                    next_monkey.item_list.append(calculated_worry)

                    #if reduce_worry:
                    #    next_monkey.item_list.append(calculated_worry)

                    #else:
                        # Get a congruent modulo for th item before we append it to the new monkey
                        # prevent a 0 from passing through
                        #print('next monkey', next_monkey.monkey_id)
                        #print('  current worry', calculated_worry)
                        #print('  next_monkey', next_monkey.operation, next_monkey.operation_value, 'mod', next_monkey.divisible_by)

                        #next_worry = next_monkey.inspect_item(calculated_worry, reduce_worry=False, count=False)
                        #print('  next worry', next_worry)
                        #print('  next modulo', next_worry % next_monkey.divisible_by)
                        #print('  next throw to', next_monkey.get_throw_to(next_worry))

                        #congruent_modulo = (calculated_worry % next_monkey.divisible_by) + next_monkey.divisible_by
                        #print('  congruent modulo', congruent_modulo)
                        #next_worry = next_monkey.inspect_item(congruent_modulo, reduce_worry=False, count=False)
                        #print('  next worry', next_worry)
                        #print('  next modulo', next_worry % next_monkey.divisible_by)
                        #print('  next throw to', next_monkey.get_throw_to(congruent_modulo))

                        #next_monkey.item_list.append(congruent_modulo)
                        #print(f'{monkey.monkey_id} throwing {calculated_worry} to {next_monkey.monkey_id}')
                        #next_monkey.catch_item(calculated_worry)

                # After we've thrown all this monkey's items, reset the list.
                monkey.item_list = []
                #print()

            #print(f'After round {round}')
            #for monkey in self.monkeys:
            #    print(monkey)

            #print()

        for monkey in self.monkeys:
            print(f'Monkey {monkey.monkey_id} inspected {monkey.inspection_count} times.')

        self.monkeys.sort(key=lambda m: m.inspection_count, reverse=True)
        monkey_business = self.monkeys[0].inspection_count * self.monkeys[1].inspection_count
        return monkey_business


class Monkey:
    def __init__(self, input):
        self.input = input

        self.inspection_count = 0

        # Things a monkey will need
        self.monkey_id = None
        self.item_list = []

        # The operation after inspection
        self.operation = None
        self.operation_value = None

        # Mokey ids to throw to.
        self.true_monkey_id = None
        self.false_monkey_id = None

        self.compile()

    def __str__(self):
        return f'{self.monkey_id}: {self.item_list}'

    def inspect_item(self, worry_level, reduce_worry=lambda x: x, count=True):
        if count:
            self.inspection_count += 1

        if self.operation_value == 'old':
            op_value = worry_level
        else:
            op_value = int(self.operation_value)

        if self.operation == '+':
            worry_after_operation = worry_level + op_value
        elif self.operation == '*':
            worry_after_operation = worry_level * op_value
        else:
            raise Exception('Unexpected operation.')

        reduced_worry_level = reduce_worry(worry_after_operation)
        return reduced_worry_level

    def get_throw_to(self, worry_level):
        if (worry_level % self.divisible_by) == 0:
            return self.true_monkey_id
        else:
            return self.false_monkey_id

    def compile(self):
        # Monkey 0:
        match = re.match(r'Monkey (?P<monkey_id>\d+):', self.input[0])
        self.monkey_id = int(match['monkey_id'])
        #print(f'monkey_id: {self.monkey_id}')

        # Starting items: 79, 98
        match = re.match(r'^  Starting items: (?P<item_list>[0-9, ]*)$', self.input[1])
        self.item_list = [int(item_number) for item_number in match['item_list'].split(',')]
        #print(f'item_list: {self.item_list}')

        # Operation: new = old * 19
        #print('Input 2: ', self.input[2])
        match = re.match(r'  Operation: new = old (?P<operator>[+-/*]) (?P<value>.+)$', self.input[2])
        self.operation = match['operator']
        # int or `old``
        self.operation_value = match['value']
        #print(f'Operation: new = old {self.operation} {self.operation_value}')

        # Test: divisible by 23
        match = re.match(r'^  Test: divisible by (?P<divisible_by>\d+)$', self.input[3])
        self.divisible_by = int(match['divisible_by'])
        #print(f'Divisible by: {self.divisible_by}')

        # If true: throw to monkey 2
        match = re.match(r'^    If true: throw to monkey (?P<monkey_id>\d+)$', self.input[4])
        self.true_monkey_id = int(match['monkey_id'])
        #print(f'true_monkey_id: {self.true_monkey_id}')

        # If false: throw to monkey 3
        match = re.match(r'^    If false: throw to monkey (?P<monkey_id>\d+)$', self.input[5])
        self.false_monkey_id = int(match['monkey_id'])
        #print(f'false_monkey_id: {self.false_monkey_id}')

        #print()


def part_1(data):
    compiler = Compiler(data)
    compiler.compile()
    monkey_business = compiler.run(rounds=20, reduce_worry=lambda x: x // 3)

    print(f'Part 1: {monkey_business}')


def part_2(data):
    compiler = Compiler(data)
    compiler.compile()
    common_modulus = compiler.common_modulus
    monkey_business = compiler.run(rounds=10000, reduce_worry=lambda x: x % common_modulus)

    print(f'Part 2: {monkey_business}')


def main(data):
    TEST_INPUT = [
        'Monkey 0:',
        '  Starting items: 79, 98',
        '  Operation: new = old * 19',
        '  Test: divisible by 23',
        '    If true: throw to monkey 2',
        '    If false: throw to monkey 3',
        '',
        'Monkey 1:',
        '  Starting items: 54, 65, 75, 74',
        '  Operation: new = old + 6',
        '  Test: divisible by 19',
        '    If true: throw to monkey 2',
        '    If false: throw to monkey 0',
        '',
        'Monkey 2:',
        '  Starting items: 79, 60, 97',
        '  Operation: new = old * old',
        '  Test: divisible by 13',
        '    If true: throw to monkey 1',
        '    If false: throw to monkey 3',
        '',
        'Monkey 3:',
        '  Starting items: 74',
        '  Operation: new = old + 3',
        '  Test: divisible by 17',
        '    If true: throw to monkey 0',
        '    If false: throw to monkey 1',
    ]
    part_1(data)
    #print()
    #print('='*79)
    #print()
    part_2(data)


if __name__ == '__main__':
    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00input.txt
    with open(f'{stem}input.txt', mode='r+') as fp:
        data = [line for line in fp.readlines()]

    main(data)

