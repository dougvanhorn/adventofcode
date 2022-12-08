#!/usr/bin/env python3

import pathlib

ROCK = ('A', 'X')
PAPER = ('B', 'Y')
SCISSORS = ('C', 'Z')

SHAPE_POINTS = {
    'A': 1,
    'X': 1,
    'B': 2,
    'Y': 2,
    'C': 3,
    'Z': 3,
}
GAME_POINTS = {
    'A X': 3,  # Rock = Rock
    'A Y': 6,  # Rock < Paper
    'A Z': 0,  # Rock > Scissors
    'B X': 0,  # Paper > Rock
    'B Y': 3,  # Paper = Paper
    'B Z': 6,  # Paper < Scissors
    'C X': 6,  # Scissors < Rock
    'C Y': 0,  # Scissors > Paper
    'C Z': 3,  # Scissors = Scissors
}


def part_1(data):

    total_score = 0
    for game in data:
        opponent, player = game.split(' ')
        points = SHAPE_POINTS[player]
        points += GAME_POINTS[game]
        total_score += points

    print(f'Part 1 Total Score: {total_score}')


LOSE = {
    'A': 'Z',
    'B': 'X',
    'C': 'Y',
}
DRAW = {
    'A': 'X',
    'B': 'Y',
    'C': 'Z',
}
WIN = {
    'A': 'Y',
    'B': 'Z',
    'C': 'X',
}

# Part 2
def part_2(data):
    total_score = 0
    for game in data:
        opponent, outcome = game.split(' ')
        if outcome == 'X':  # lose
            player = LOSE[opponent]
        elif outcome == 'Y':  # draw
            player = DRAW[opponent]
        elif outcome == 'Z':  # win
            player = WIN[opponent]

        points = SHAPE_POINTS[player]
        points += GAME_POINTS[f'{opponent} {player}']
        total_score += points

    print(f'Part 2 Total Score: {total_score}')


if __name__ == '__main__':
    stem = pathlib.Path(__file__).stem
    with open(f'{stem}input.txt', mode='r+') as fp:
        data = [line.strip() for line in fp.readlines()]

    part_1(data)
    part_2(data)

