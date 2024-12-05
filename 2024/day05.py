#!/usr/bin/env python3

import collections
import logging
import math
import pathlib


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


def part_1(rules, manuals):
    p('== Part 1 ==')
    p(f'{len(rules):>3} Rules')
    p(f'{len(manuals):>3} Manuals')
    print('-'*80)

    middle_pages = []
    for manual in manuals:
        p(f'Manual: {manual}')

        is_valid = manual.validate(rules)
        if is_valid:
            p(f'        Valid, adding {manual.middle_page}')
            middle_pages.append(manual.middle_page)

        else:
            p('        NOT Valid')

    answer = sum(middle_pages)
    print(f'{len(middle_pages)} valid manuals')
    print(f'Answer: {answer}')


def part_2(rules, manuals):
    p('== Part 2 ==')
    p(f'{len(rules):>3} Rules')
    p(f'{len(manuals):>3} Manuals')
    print('-'*80)

    middle_pages = []
    for manual in manuals:
        print('-'*80)
        p(f'Manual: {manual}')

        counter = 0
        violations = manual.part_2(rules)
        if not violations:
            continue

        p(f'  Violations: {violations}')

        MAX_ITERATIONS = 1000
        while violations and counter < MAX_ITERATIONS:
            manual.fix(violations[0])
            counter += 1
            violations = manual.part_2(rules)

        if counter > MAX_ITERATIONS:
            raise ValueError(f'Too many iterations [{MAX_ITERATIONS}].')
        else:
            p(f'  Fixed: {manual}')

        middle_pages.append(manual.middle_page)
        print('-'*80)

    print(f'Answer: {sum(middle_pages)}')


class Rule:
    def __init__(self, rule_string):
        self.rule_string = rule_string
        before, after = rule_string.split('|')
        self.before = int(before)
        self.after = int(after)

    def __repr__(self):
        return self.rule_string

    def __str__(self):
        return self.rule_string


class Page:
    def __init__(self, page, index):
        self.page = page
        self.index = index

class RuleSet:
    def __init__(self, rules, pages):
        self.rules = rules
        self.pages = pages

        self.before_index = collections.defaultdict(list)
        self.after_index = collections.defaultdict(list)
        # Naming is from the current page perspective.
        for rule in rules:
            # The current page is in the before position.
            self.before_index[rule.before].append(rule)
            # The current page is in ther after position.
            self.after_index[rule.after].append(rule)

        # Page number index lookup.
        self.page_index = {page: index for index, page in enumerate(self.pages)}

    def validate(self, current_page, return_violations=False):
        current_index = self.page_index[current_page]

        violations = []
        is_valid = True
        # Check before rules.
        before_rules = self.before_index.get(current_page, [])
        for rule in before_rules:
            # Get the index of the after page
            if rule.after in self.page_index:
                after_index = self.page_index[rule.after]
                # current page should come before, but does not.
                if current_index > after_index:
                    p(f'        Rule Violation: {current_page} is after {rule.after}, rule {rule}')
                    violations.append(rule)

        # Check after rules.
        after_rules = self.after_index.get(current_page, [])
        for rule in after_rules:
            # Get the index of the after page
            if rule.before in self.page_index:
                before_index = self.page_index[rule.before]
                # current page should come after, but does not.
                if current_index < before_index:
                    p(f'        Rule Violation: {current_page} is before {rule.before}, rule {rule}')
                    violations.append(rule)

        if return_violations:
            return violations
        else:
            return bool(violations)


class Manual:
    def __init__(self, update_string):
        self.update_string = update_string
        self.pages = [int(x) for x in update_string.split(',')]
        self.page_count = len(self.pages)

    def __str__(self):
        return ','.join(str(x) for x in self.pages)

    @property
    def middle_page(self):
        if self.page_count % 2 == 0:
            raise ValueError('Even number of pages.')

        return self.pages[self.page_count // 2]

    def validate(self, rules):
        rule_set = RuleSet(rules, self.pages)

        # Loops over pages, checks rules.
        for current_page in self.pages:
            is_valid = rule_set.validate(current_page)
            if not is_valid:
                return False

        return True

    def part_2(self, rules):
        print(f'Building ruleset for {self.pages}')
        rule_set = RuleSet(rules, self.pages)
        for current_page in self.pages:
            violations = rule_set.validate(current_page, return_violations=True)
            if violations:
                return violations

    def fix(self, rule):
        print(f'  --> Fixing: {self.pages}, Rule: {rule}')
        self.page_index = {page: index for index, page in enumerate(self.pages)}
        # Swap the pages in the rule to fix the violation.
        before_index = self.page_index[rule.before]
        after_index = self.page_index[rule.after]
        p(f'  ...swapping {rule.before}[{before_index}] and {rule.after}[{after_index}]')
        self.pages[before_index] = rule.after
        self.pages[after_index] = rule.before
        print(f'  ...pages: {self.pages}')


def main(data):
    # Prepare the data.
    rules = []
    manuals = []
    for row in data:
        if not row:
            continue

        if '|' in row:
            rules.append(Rule(row))

        else:
            manuals.append(Manual(row))

    # part_1(rules, manuals)
    part_2(rules, manuals)


if __name__ == '__main__':
    data = load_data()
    _data = [
        '47|53',
        '97|13',
        '97|61',
        '97|47',
        '75|29',
        '61|13',
        '75|53',
        '29|13',
        '97|29',
        '53|29',
        '61|53',
        '97|53',
        '61|29',
        '47|13',
        '75|47',
        '97|75',
        '47|61',
        '75|61',
        '47|29',
        '75|13',
        '53|13',
        '',
        '75,47,61,53,29',
        '97,61,53,29,13',
        '75,29,13',
        '75,97,47,61,53',
        '61,13,29',
        '97,13,75,29,47',
    ]
    main(data)
