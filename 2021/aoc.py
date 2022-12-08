#!/usr/bin/env python3
import collections
import math
import re
import traceback


# =============================================================================
# Command Line Coloring
# -----------------------------------------------------------------------------
RESET = "\033[0m"

BOLD = "\033[1m"
DIM = "\033[2m"
UNDERLINED = "\033[4m"
BLINK = "\033[5m"
REVERSE = "\033[7m"
HIDDEN = "\033[8m"
FORMATTING = {
    'bold': BOLD,
    'dim': DIM,
    'underlined': UNDERLINED,
    'blink': BLINK,
    'reverse': REVERSE,
    'hidden': HIDDEN,
}

RESETBOLD = "\033[21m"
RESETDIM = "\033[22m"
RESETUNDERLINED = "\033[24m"
RESETBLINK = "\033[25m"
RESETREVERSE = "\033[27m"
RESETHIDDEN = "\033[28m"
RESET_FORMATTING = {
    'bold': RESETBOLD,
    'dim': RESETDIM,
    'underlined': RESETUNDERLINED,
    'blink': RESETBLINK,
    'reverse': RESETREVERSE,
    'hidden': RESETHIDDEN,
}

DEFAULT = "\033[39m"
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
LIGHTGRAY = "\033[37m"
DARKGRAY = "\033[90m"
LIGHTRED = "\033[91m"
LIGHTGREEN = "\033[92m"
LIGHTYELLOW = "\033[93m"
LIGHTBLUE = "\033[94m"
LIGHTMAGENTA = "\033[95m"
LIGHTCYAN = "\033[96m"
WHITE = "\033[97m"
COLORS = {
    'default': DEFAULT,
    'black': BLACK,
    'red': RED,
    'green': GREEN,
    'yellow': YELLOW,
    'blue': BLUE,
    'magenta': MAGENTA,
    'cyan': CYAN,
    'lightgray': LIGHTGRAY,
    'darkgray': DARKGRAY,
    'lightred': LIGHTRED,
    'lightgreen': LIGHTGREEN,
    'lightyellow': LIGHTYELLOW,
    'lightblue': LIGHTBLUE,
    'lightmagenta': LIGHTMAGENTA,
    'lightcyan': LIGHTCYAN,
    'white': WHITE,
}

BG_DEFAULT = "\033[49m"
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_LIGHTGRAY = "\033[47m"
BG_DARKGRAY = "\033[100m"
BG_LIGHTRED = "\033[101m"
BG_LIGHTGREEN = "\033[102m"
BG_LIGHTYELLOW = "\033[103m"
BG_LIGHTBLUE = "\033[104m"
BG_LIGHTMAGENTA = "\033[105m"
BG_LIGHTCYAN = "\033[106m"
BG_WHITE = "\033[107m"
BG_COLORS = {
    'bg_default': BG_DEFAULT,
    'bg_black': BG_BLACK,
    'bg_red': BG_RED,
    'bg_green': BG_GREEN,
    'bg_yellow': BG_YELLOW,
    'bg_blue': BG_BLUE,
    'bg_magenta': BG_MAGENTA,
    'bg_cyan': BG_CYAN,
    'bg_lightgray': BG_LIGHTGRAY,
    'bg_darkgray': BG_DARKGRAY,
    'bg_lightred': BG_LIGHTRED,
    'bg_lightgreen': BG_LIGHTGREEN,
    'bg_lightyellow': BG_LIGHTYELLOW,
    'bg_lightblue': BG_LIGHTBLUE,
    'bg_lightmagenta': BG_LIGHTMAGENTA,
    'bg_lightcyan': BG_LIGHTCYAN,
    'bg_white': BG_WHITE,
}


def format(s, format_string):
    parts = format_string.split(' ')
    prefix = []
    for part in parts:
        prefix.append(FORMATTING.get(part))
        prefix.append(COLORS.get(part))
        prefix.append(BG_COLORS.get(part))
    # valid_prefixes = [code for code in prefix if code]
    # print(f'format_string; {format_string}, valid_prefixes: {len(valid_prefixes)}')
    prefix_string = ''.join(code for code in prefix if code)
    return f'{prefix_string}{s}{RESET}'
# -----------------------------------------------------------------------------


# =============================================================================
# Grid
# -----------------------------------------------------------------------------
class Cell:
    def __init__(self, row, col, value=None, default='.'):
        self.row = row
        self.col = col
        self.value = value
        self.default = default

    def __str__(self):
        if self.value is None:
            return str(self.default)
        else:
            return str(self.value)

    def __repr__(self):
        return f'[({self.row}, {self.col}), {self.value}]' 


class Grid:
    def __init__(self):
        self.lines = None
        self.cells = None

    @classmethod
    def from_lines(cls, lines):

        for row, line in enumerate(lines):
            for col, value in enumerate(line):
                cell = Cell(row, col, value=value)
class Cell:
    def __init__(self, row=None, col=None, value=None):
        self.row = row
        self.col = col
        self.value = value
        self.default = '.'

    def __str__(self):
        if self.value is None:
            return str(self.default)
        else:
            return str(self.value)

    def __repr__(self):
        return f'[({self.row}, {self.col}), {self.value}]' 

    @property
    def id(self):
        return (self.row, self.col)

    def pprint(self):
        return str(self)


class Grid:
    def __init__(self, lines):
        self.lines = lines
        self.cells = []
        # Lookup cells by id.
        self.cell_db = {}
        for row, line in enumerate(lines):
            cell_row = []
            for col, value in enumerate(line):
                cell = Cell(row=row, col=col, value=int(value))
                cell_row.append(cell)
                self.cell_db[cell.id] = cell
            self.cells.append(cell_row)

        self.MAX_ROWS = len(self.cells)
        self.MAX_COLS = len(self.cells[0])

        self.populate_neighbors()

    def print_grid(self):
        rows = []
        for i, row in enumerate(self.cells):
            values = []
            for cell in row:
                values.append(cell.format_cell())
            col = ' '.join(values)
            rows.append(f'{i:>02}: {col}')
        print('\n'.join(rows))

    def iterate_cells(self):
        # Loop over rows, cells as a generator.
        for row in self.cells:
            for cell in row:
                yield cell

    def populate_neighbors(self):
        # Append a list of neighbors to each cell.
        for cell in self.iterate_cells():
            row, col = cell.id
            moves = [
                (-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 1),
                (1, -1), (1, 0), (1, 1),
            ]
            neighbors = []
            for row_delta, col_delta in moves:
                neighbor_id = (row + row_delta, col + col_delta)
                neighbor_cell = self.cell_db.get(neighbor_id)
                if neighbor_cell:
                    neighbors.append(neighbor_cell)

            cell.neighbors = neighbors







def loadfile(filename):
    """Load lines from file, stripping whitespace.
    """
    with open(filename, mode='r+') as fp:
        lines = [line.strip() for line in fp.readlines()]
    return lines


def group_lines(lines):
    """Groups lines based on blank lines as delimiter.
    """
    groups = []
    group = []
    for line in lines:
        if line:
            group.append(line)
        else:
            groups.append(group)
            group = []

    groups.append(group)
    return groups

