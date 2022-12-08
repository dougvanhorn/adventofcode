#!/usr/bin/env python3

import collections
import math
import pprint
import re
import traceback

import aoc


class Bag_:
    def __init__(self, quantity, name):
        self.quantity = quantity
        self.name = name

    def __str__(self):
        return f"Bag(quantity='{self.quantity}', name='{self.name}')"

    def __repr__(self):
        return self.__str__()


class Rule_:
    def __init__(self, text):
        # A text rule looks like this:
        # color ::= [adjective] [color_text]
        # parent_bag ::= color "bags"
        # sub_bag ::= color "bag"
        # sub_bag_quantity ::= int sub_bag
        # rule ::= parent_bag "contain" sub_bag_quantity[, sub_bag_quantity].
        self.text_rule = text
        regex_text = r'(\w+ \w+) bags contain (.*).'
        result = re.match(regex_text, self.text_rule)
        self.bag_name, self.bag_components_text = result.groups()

        self.direct_gold = False
        self.indirect_gold = False

        self.bag = Bag_(1, self.bag_name)
        self.bag_components = {}
        if 'no other' not in self.bag_components_text:
            parts = self.bag_components_text.split(', ')
            for component in parts:
                result = re.match(r'^(\d+) (\w+ \w+) bag', component)
                quantity, name = result.groups()
                bag = Bag_(quantity, name)
                self.bag_components[bag.name] = bag

                # Track if this rule contains gold.
                if name == 'shiny gold':
                    self.direct_gold = True

    def __str__(self):
        return f'{self.text_rule}\n{self.bag}: {self.bag_components}'


class Bag:
    def __init__(self, name):
        self.name = name
        self.gold = False
        self.parent_bags = []
        self.component_bags = []
        self.quantity = 0

    def __str__(self):
        return f'{self.name} {self.quantity}'

    def __repr__(self):
        return self.__str__()

    def add_component(self, component_bag):
        self.component_bags.append(component_bag)

    def add_parent(self, parent_bag):
        self.parent_bags.append(parent_bag)

    def set_gold(self):
        # Set every parent to gold, short circuit if already gold.
        self.gold = True
        for parent in self.parent_bags:
            if not parent.gold:
                parent.set_gold()

    def sum_bags(self):
        total = 0
        for bag in self.component_bags:
            total += bag.quantity
            total += PARENT_BAGS[bag.name].sum_bags()
        return total

class Rule:
    def __init__(self, text_rule):
        self.text_rule = text_rule
        regex_text = r'(\w+ \w+) bags contain (.*).'
        result = re.match(regex_text, self.text_rule)

        self.bag_name, self.bag_components_text = result.groups()

        self.direct_gold = False
        self.indirect_gold = False

        self.bag = Bag_(1, self.bag_name)
        self.bag_components = {}
        if 'no other' not in self.bag_components_text:
            parts = self.bag_components_text.split(', ')
            for component in parts:
                result = re.match(r'^(\d+) (\w+ \w+) bag', component)
                quantity, name = result.groups()
                bag = Bag_(quantity, name)
                self.bag_components[bag.name] = bag

                # Track if this rule contains gold.
                if name == 'shiny gold':
                    self.direct_gold = True


def parse_line(line):
    # bag_name ::= <adj> <color>
    # rule ::= <bag_name> bags contain [no other bags | <bag_name>+].
    result = re.match(r'(\w+ \w+) bags contain (.*).', line)
    bag_name, components_text = result.groups()

    data = {}
    data['name'] = bag_name
    data['contains'] = []

    parts = components_text.split(', ')
    for component in parts:
        result = re.match(r'^(\d+) (\w+ \w+) bag', component)
        if not result:
            continue
        quantity, name = result.groups()
        # Get the bag is if's already in our dict.
        data['contains'].append({'name': name, 'quantity': int(quantity)})

    return data


class Bag:
    def __init__(self, parsed_line):
        self.parsed_line = parsed_line
        self.name = parsed_line['name']
        self.contains_shiny_gold = False
        self.inner_bags = []
        self.parents = []

    def __str__(self):
        details = [f'  {bag.quantity} {bag.name}' for bag in self.inner_bags]
        details.insert(0, self.name)
        return '\n'.join(details)

    def print_tree(self, BAGS, indent=2, name=True):
        SPACE = ' ' * indent
        lines = []

        if name:
            lines.append(self.name)

        for inner_bag in self.inner_bags:
            lines.append(f'{SPACE}{inner_bag.quantity} {inner_bag.name}')
            bag = BAGS[inner_bag.name]
            sub_lines = bag.print_tree(BAGS, indent=indent+2, name=False)
            lines.extend(sub_lines)

        return lines

    def add_parent(self, descendent_bag):
        self.parents.append(descendent_bag)

    def build(self, BAGS):
        # BAGS: a dict DB of bags.
        for bag_data in self.parsed_line['contains']:
            inner_bag = InnerBag(bag_data['name'], bag_data['quantity'])
            self.inner_bags.append(inner_bag)
            if 'shiny gold' in inner_bag.name:
                self.contains_shiny_gold = True
            bag = BAGS[inner_bag.name]
            bag.add_parent(self)

    def check_for_shiny_gold(self, BAGS):
        if self.contains_shiny_gold:
            return True
        for inner_bag in self.inner_bags:
            bag = BAGS[inner_bag.name]
            if bag.check_for_shiny_gold(BAGS):
                self.contains_shiny_gold = True
                return True

        return False

    def sum_bags(self, BAGS):
        total = 0
        for inner_bag in self.inner_bags:
            sum1 = inner_bag.quantity
            bag = BAGS[inner_bag.name]
            sum2 = bag.sum_bags(BAGS)
            sum2 *= inner_bag.quantity
            total += (sum1 + sum2)
        return total


class InnerBag:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity


def main():
    lines = aoc.loadfile('07.txt')

    #rules = [Rule_(line) for line in lines]

    # The "database" of bags, a dict keyed on bag name.
    parsed_lines = [parse_line(line) for line in lines]

    bags = [Bag(data) for data in parsed_lines]
    BAGS = {bag.name: bag for bag in bags}

    print(f'Bag count: {len(bags)}')

    lines = []
    for bag in bags:
        bag.build(BAGS)

    for bag in bags:
        lines.extend(bag.print_tree(BAGS))
    with open('debug.txt', mode='w+') as fp:
        for row in lines:
            fp.write(f'{row}\n')
    print('wrote debug.txt')

    count = 0
    for bag in bags:
        if bag.check_for_shiny_gold(BAGS):
            count += 1

    print(f'Bags containing gold: {count}')

    shiny_gold = BAGS['shiny gold']

    lines = shiny_gold.print_tree(BAGS)
    print('\n'.join(lines))

    print(f'{shiny_gold.name} contains {shiny_gold.sum_bags(BAGS)} bags.')


if __name__ == '__main__':
    main()
