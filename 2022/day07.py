#!/usr/bin/env python3

import pathlib


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = int(size)


class Dir:
    def __init__(self, name=None):
        self.name = name
        self.parent = None

        # Can I do this?  when in root cd .. does nothing.
        if self.name is None:
            self.parent = self

        self.dirs = {}
        self.files = {}

        self.size = 0
        self._total_size = 0

    @property
    def is_root(self):
        return self.name is None

    def mkdir(self, name):
        # Optionally make a directory and return it.
        dir = self.dirs.setdefault(name, Dir(name))
        dir.parent = self
        return dir

    def touch(self, name, size):
        file = File(name, size)
        self.files[name] = file
        self.size += file.size

    @property
    def total_size(self):
        # cache the total, we'll only calculate once
        if self._total_size:
            return self._total_size
        self._total_size = self.size
        for name, dir in self.dirs.items():
            self._total_size += dir.total_size
        return self._total_size


class Filesystem:
    @staticmethod
    def from_history(history):
        filesystem = Filesystem()

        for line in history:
            if line.startswith('$ cd'):
                filesystem.cd(line[5:])

            elif line.startswith('$ ls'):
                pass

            elif line.startswith('dir'):
                # print(f'Adding dir {line[4:]}')
                filesystem.mkdir(line[4:])

            else:
                size, name = line.split(' ')
                #print(f'Adding file: {size} {name}')
                filesystem.touch(name, size)

        return filesystem

    def __init__(self):
        self.root = Dir()
        self.current_dir = self.root

    def cd(self, name):
        if name == '/':
            # print('CD to root.')
            self.current_dir = self.root

        elif name == '..':
            # print('CD up a directory.')
            self.current_dir = self.current_dir.parent

        else:
            # print(f'CD into {name}')
            self.current_dir = self.current_dir.mkdir(name)

    def mkdir(self, name):
        self.current_dir.mkdir(name)

    def touch(self, name, size):
        self.current_dir.touch(name, size)

    def part_1(self):
        # walk the dirs, find all total sizes < 100_000, sum them.
        found = []
        def walk(dir):
            for name, child in dir.dirs.items():
                if child.total_size <= 100_000:
                    found.append(child)
                walk(child)

        walk(self.root)

        total = sum(dir.total_size for dir in found)
        print(f'Part 1: {total}')


    def part_2(self):
        disk_space = 70_000_000
        unused_space = 30_000_000
        used_space = self.root.total_size
        available_space = disk_space - used_space
        needed_space = unused_space - available_space
        #print(f'Total space: {disk_space}')
        #print(f'Used space:  {self.root.total_size}')
        #print(f'Available:   {available_space}')
        #print(f'Needed:      {needed_space}')

        all_dirs = []
        def walk(dir):
            for name, child in dir.dirs.items():
                all_dirs.append(child)
                walk(child)

        walk(self.root)

        all_dirs.sort(key=lambda d: d.total_size)
        for d in all_dirs:
            if d.total_size > needed_space:
                print(f'Part 2: Delete {d.name} {d.total_size}')
                break

    def __str__(self):
        def _print_dir(dir, indent=0):
            tab = ' ' * indent
            if dir.is_root:
                s = f'- / (dir) Local Size: {dir.size}, Total Size: {dir.total_size}\n'
            else:
                s = f'{tab}- {dir.name} (dir) Local Size: {dir.size}, Total Size: {dir.total_size}\n'

            for name, child in dir.dirs.items():
                s += _print_dir(child, indent=indent+2)

            for name, file in dir.files.items():
                tab = ' ' * (indent + 2)
                s += f'{tab}- {file.name} (file, size={file.size})\n'
                
            return s

        return _print_dir(self.root, indent=0)


def part_1(data):
    filesystem = Filesystem.from_history(data)
    # Our string function walks the entire tree and caches total sizes.
    str(filesystem)
    filesystem.part_1()
    filesystem.part_2()


def part_2(data):
    pass


def main(data):
    test_input = [
        '$ cd /',
        '$ ls',
        'dir a',
        '14848514 b.txt',
        '8504156 c.dat',
        'dir d',
        '$ cd a',
        '$ ls',
        'dir e',
        '29116 f',
        '2557 g',
        '62596 h.lst',
        '$ cd e',
        '$ ls',
        '584 i',
        '$ cd ..',
        '$ cd ..',
        '$ cd d',
        '$ ls',
        '4060174 j',
        '8033020 d.log',
        '5626152 d.ext',
        '7214296 k',
    ]
    part_1(data)
    part_2(data)


if __name__ == '__main__':
    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00input.txt
    with open(f'{stem}input.txt', mode='r+') as fp:
        data = [line.strip() for line in fp.readlines()]

    main(data)
