#!/usr/bin/env python

import collections
from itertools import count
import logging
import math
import pathlib

import pulp
import rich
from rich.progress import track


logging.basicConfig(level=logging.ERROR, format='%(message)s')
log = logging.getLogger('aoc')

def noop(*args, **kwargs):
    pass

def load_data():
    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00-input.txt
    with open(f'{stem}-input.txt', mode='r+') as fp:
        data = [line.strip('\n') for line in fp.readlines()]
    return data


def part_1(machines):
    rich.print('[bold red]== Part 1 ==[/bold red]')
    rich.print('State machine simulation.  Breadth first search.')

    og_print = rich.print
    answer = 0
    for machine in machines:
        rich.print(f'[bold blue]Machine: {machine}[/bold blue]')
        rich.print = noop
        count = machine.part_1_solution()
        rich.print = og_print
        if count is None:
            rich.print('  [bold red]No solution found.[/bold red]')
            continue
        rich.print(f'  [bold green]Solution found in {count} button presses.[/bold green]')
        answer += count
        print()

    rich.print(f'[bold green]Part 1 Answer[/bold green]: [bold]{answer}[/bold]')


def part_2(machines):
    rich.print('[bold red]== Part 2 ==[/bold red]')
    rich.print('Press buttons until final joltages reached.')

    og_print = rich.print
    answer = 0
    for machine in machines:
        rich.print(f'[bold blue]Machine: {machine}[/bold blue]')

        rich.print = noop
        presses = machine.part_2_solution_2()
        rich.print = og_print

        if presses is None:
            rich.print('  [bold red]No solution found.[/bold red]')
            continue

        rich.print(f'  [bold green]Solution found in {presses} button presses.[/bold green]')
        answer += presses

    rich.print(f'[bold green]Part 2 Answer[/bold green]: [bold]{answer}[/bold]')

# Constants / Defines
ON = True
OFF = False


class Button:
    def __init__(self, transition):
        parts = transition.strip('()').split(',')
        self.targets = [int(part) for part in parts]

    def __repr__(self):
        return f'Button(targets={self.targets})'

    def press(self, state):
        new_state = list(state)
        for target in self.targets:
            new_state[target] = not new_state[target]
        return tuple(new_state)

    def jolt(self, state):
        new_state = list(state)
        for target in self.targets:
            new_state[target] += 1
        return tuple(new_state)


class Machine:
    def __init__(self, rules):
        self.rules = rules
        parts = rules.split(' ')
        # First if final state
        _final_state = parts[0]
        # Last is joltage (cost, edge weight)
        _joltage = parts[-1]
        # State transitions.
        _transitions = parts[1:-1]

        # # indicates light is on.
        self.final_state = tuple(c == '#' for c in _final_state[1:-1])
        self.state = tuple(OFF for _ in self.final_state)

        self.final_joltages = tuple(int(jolt) for jolt in _joltage.strip('{}').split(','))
        self.joltages = tuple(0 for _ in self.final_joltages)

        self.buttons = [Button(transition) for transition in _transitions]

    def __str__(self):
        state_str = ''.join('#' if s else '.' for s in self.state)
        return f'[{state_str}]'

    def __repr__(self):
        return f'Machine(state={self.state}, final_state={self.final_state}, buttons={self.buttons}, joltages={self.joltages}, final_joltages={self.final_joltages} )'

    @property
    def is_correct(self):
        return self.state == self.final_state

    def press(self, button_idx):
        button = self.buttons[button_idx]
        # original_state = list(self.state)
        for target in button.targets:
            self.state[target] = not self.state[target]

    def part_1_solution(self):
        # Bredth first search
        state = tuple(self.state)

        states = {
            state: 0
        }
        next_states = list(states.items())
        while True:
            # Press buttons until we reach final state.
            rich.print('Exploring next states:')
            for state, count in next_states:
                visual_state = ''.join('#' if s else '.' for s in state)
                rich.print(f'  State: {visual_state} after {count} presses.')
            new_states = {}
            for state, count in next_states:
                visual_state = ''.join('#' if s else '.' for s in state)
                rich.print(f'At state: {visual_state} after {count} presses.')
                for button in self.buttons:
                    new_state = button.press(state)
                    rich.print(f'  {button} {visual_state}')
                    new_visual_state = ''.join('#' if s else '.' for s in new_state)
                    rich.print(f'    New state: {new_visual_state}')
                    # If we reach final state, return the count + 1.
                    if new_state == self.final_state:
                        rich.print('    [bold red]FINAL STATE REACHED![/bold red]')
                        return count + 1

                    if new_state in states:
                        previous_count = states[new_state]
                        rich.print(f'    State seen: {new_visual_state} after {previous_count} presses.  Current count: {count + 1}.')
                        # The new state is already in the states dict.
                        # No need to add it again.
                        continue

                    # We have a new state
                    rich.print(f'    [bold green]New state discovered: {new_visual_state}[/bold green]')
                    states[new_state] = count + 1
                    new_states[new_state] = count + 1
                    # Indicate we found new state, and are not looping.
                    loop = False

            # If no button presses created new state, we are looping.
            if not new_states:
                rich.print('After every button press, we found no new states.')
                # We looped through all buttons and found no new states.
                # This means we are done.
                return

            # Prepare the next states to explore.
            next_states = list(new_states.items())
            rich.print()

    def part_2_solution(self):
        # Breadth first, but keep 
        joltage = tuple(self.joltages)

        # All joltages we've reached so far.
        joltages = {
            joltage: 0
        }

        next_states = list(joltages.items())
        while True:
            # Press buttons until we reach final state.
            rich.print('Exploring next states:')
            for state, count in next_states:
                visual_state = ','.join(str(j) for j in state)
                rich.print(f'  State: {visual_state} after {count} presses.')

            new_joltages = {}
            for state, count in next_states:
                visual_state = ','.join(str(j) for j in state)
                rich.print(f'State: {visual_state}, {count} presses.')

                for button in self.buttons:
                    new_joltage = button.jolt(state)
                    rich.print(f'  {button} {visual_state}')

                    new_visual_state = ','.join(str(j) for j in new_joltage)
                    rich.print(f'    New state: {new_visual_state}')

                    # If we reach final state, return the count + 1.
                    if new_joltage == self.final_joltages:
                        rich.print('    [bold red]FINAL JOLTAGE REACHED![/bold red]')
                        return count + 1

                    if new_joltage in joltages:
                        previous_count = joltages[new_joltage]
                        rich.print(f'    Joltage seen: {new_visual_state} after {previous_count} presses.  Current count: {count + 1}.')
                        # The new state is already in the states dict.
                        # No need to add it again.
                        continue

                    # If any joltage exceeds final, skip, discard.
                    discard = False
                    for new_j, final_j in zip(new_joltage, self.final_joltages):
                        if new_j > final_j:
                            rich.print(f'    [bold yellow]Joltage {new_j} exceeds final {final_j}.  Discarding state {new_visual_state}.[/bold yellow]')
                            discard = True
                            break
                    if discard:
                        continue

                    # We have a new state, it's legal, add it to the list.
                    rich.print(f'    [bold green]New state discovered: {new_visual_state}[/bold green]')
                    joltages[new_joltage] = count + 1
                    new_joltages[new_joltage] = count + 1
                    # Indicate we found new state, and are not looping.

            # If no button presses created new state, we are looping.
            if not new_joltages:
                rich.print('After every button press, we found no new joltage states.')
                # We looped through all buttons and found no new states.
                # This means we are done.
                return

            # Prepare the next states to explore.
            next_states = list(new_joltages.items())
            rich.print()

    def part_2_solution_2(self):
        # Use pulp, a linear programming tool.
        # Define buttons as vectors.
        buttons = []
        for button in self.buttons:
            rich.print(f'Button: {button}')
            adder = [
                1 if i in button.targets else 0
                for i in range(len(self.final_joltages))
            ]
            rich.print(f'Adder: {adder}')
            buttons.append(adder)

        # Define the problem.
        # Objective: minimize total button presses.
        problem = pulp.LpProblem('ButtonPressProblem', pulp.LpMinimize)
        # Define the variables.  Could be done in loop above.
        button_vars = [
            pulp.LpVariable(f'button_{i}', lowBound=0, cat='Integer')
            for i in range(len(buttons))
        ]

        # Define the Objective Function (the solution).
        problem += pulp.lpSum(button_vars)

        # Constraints: final joltages reached.
        for joltage_index in range(len(self.final_joltages)):
            # e.g., 3, 5, 4, 7
            # Define what each button press does (adds joltages).
            # For each button, define how it increases joltages, state 
            problem += (
                pulp.lpSum(
                    button[joltage_index] * button_vars[button_index]  # 0 0 0 1, 0 1 0 1
                    for button_index, button in enumerate(buttons)
                ) == self.final_joltages[joltage_index]
            )
        # Solve the problem.  Disable ouptut.
        problem.solve(pulp.PULP_CBC_CMD(msg=False))
        # Return the total button presses.
        return pulp.value(problem.objective)


def main(data):
    _data = [
        '[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}',  # 2 preess, 4 5
        '[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}',  # 3 presses: 2 3 4
        '[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}',  # 2 presses: 1 2
    ]
    machines = [Machine(manual) for manual in data]
    # part_1(machines)
    part_2(machines)


if __name__ == '__main__':
    data = load_data()
    main(data)
