#!/usr/bin/env python3

import collections
import logging
import math
import pathlib


logging.basicConfig(level=logging.DEBUG, format='%(message)s')

DEBUG = True

def load_data():
    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00-input.txt
    with open(f'{stem}-input.txt', mode='r+') as fp:
        data = [line.strip() for line in fp.readlines()]
    return data


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


def part_2(data):
    debug('== Part 2 ==')
    pass

FILE = 'file'
SPACE = 'space'

class File:
    def __init__(self, file_id, size):
        # This is the block index number
        self.file_id = file_id
        self.size = size
        self.kind = FILE

    def __str__(self):
        return f'File({self.file_id}, {self.size})'

    def __repr__(self):
        return f'File({self.file_id}, {self.size})'

    def fmt(self):
        return f'{self.file_id}' * self.size


class Space:
    def __init__(self, size):
        self.size = size
        self.kind = SPACE

    def __str__(self):
        return f'Space({self.size})'

    def __repr__(self):
        return f'Space({self.size})'

    def fmt(self):
        return '.' * self.size

    def is_available(self, size):
        return self.size >= size

    def split(self, size):
        if self.size < size:
            raise Exception(f'Not enough space to split. {self.size} < {size}')
        elif self.size == size:
            return self, None
        else:
            new_space = Space(self.size - size)
            self.size -= size
            return self, new_space



class Filesystem:
    def __init__(self, data):
        self.data = [int(i) for i in data]

        # Length of data.
        debug('Data length:', len(self.data))

        # Disk size.
        # Each number represents size on disk.
        self.disk_size = sum(self.data)
        # debug('data', self.data)
        debug(f'Disk size: {self.disk_size}')

        self.disk_db = sqlite3.connect(':memory:')
        self.disk_db.execute('CREATE TABLE empty_space (block_id INTEGER PRIMARY KEY, block_size INTEGER)')



        # Fill in the disk.
        self.disk = []
        self.disk2 = []
        for i in range(0, len(self.data), 2):
            file_id = i // 2
            file_size = self.data[i]  # the block contains the file size.

            # debug('file_id:', file_id, 'block:', block)
            self.disk.extend([file_id] * file_size)
            self.disk2.append(File(file_id, file_size))

            try:
                empty_space = self.data[i + 1]
                self.disk.extend(['.'] * empty_space)
                if empty_space > 0:
                    self.disk2.append(Space(empty_space))

                if empty_space > 0:
                    disk_db.execute('INSERT INTO empty_space VALUES (?, ?)', (block.file_id, block.size))

            except IndexError:
                # Last file.
                pass

        if len(self.disk) != self.disk_size:
            raise Exception('Disk size does not match.')

    def __str__(self):
        return ''.join(str(i) for i in self.disk[:100])


    def part_1(self):
        debug('=== Part 1 ===')
        end_of_disk = len(self.disk)

        def move_back(end_of_disk):
            back_one = end_of_disk - 1
            while self.disk[back_one] == '.':
                back_one -= 1

            debug(f'  Walking back to disk[{back_one}]={self.disk[back_one]}')
            return back_one

        def debug_pointers(i, end_of_disk):
            pointers = [' ' for _ in range(len(self.disk[:100]))]
            try:
                pointers[i] = '>'
            except IndexError:
                pass
            try:
                pointers[end_of_disk] = '<'
            except IndexError:
                pass
            debug(''.join(pointers))


        end_of_disk = move_back(end_of_disk)

        debug('=' * 80)
        debug('Starting Disk:')
        debug_pointers(0, end_of_disk)
        debug(str(self))
        debug('-' * 80)

        for i in range(0, self.disk_size):
            if self.disk[i] == '.':
                # swap empty space with end of disk data.
                # Swap data
                debug('=' * 80)
                debug('Block is empty')
                debug_pointers(i, end_of_disk)
                debug(str(self))

                # debug pointers before the swap.
                debug(f'  Swapping disk[{i}]={self.disk[i]} and disk[{end_of_disk}]={self.disk[end_of_disk]}')

                self.disk[i] = self.disk[end_of_disk]
                self.disk[end_of_disk] = '.'

                # Move the end of file pointer to the next non-empty block.
                end_of_disk = move_back(end_of_disk)
                debug('-' * 80)

            else:
                debug('=' * 80)
                debug('Block is not empty.')
                debug_pointers(i, end_of_disk)
                debug(str(self))
                debug('-' * 80)

            if i >= end_of_disk:
                break

        debug('Disk Compressed')
        debug(str(self))

        # checksum
        checksum = 0
        for i, block in enumerate(self.disk):
            if block == '.':
                break
            checksum += i * block

        debug('Checksum:', checksum)

    def debug_disk2(self, current_file, end_of_disk):
        pointers = ''
        filesystem = ''
        for i, block in enumerate(self.disk2[:20]):
            filesystem += block.fmt()
            if i == current_file:
                pointers += '>' + (' ' * (block.size - 1))
            elif i == end_of_disk:
                pointers += '<' + (' ' * (block.size - 1))
            else:
                pointers += ' ' * block.size

        debug(pointers)
        debug(filesystem)

    def part_2(self):
        # Same as 1, but attempt to move whole file into empty space.
        end_of_disk = len(self.disk2)

        for block in self.disk2:
            print(block)

        def previous_file_index(end_of_disk):
            back_one = end_of_disk - 1
            while self.disk2[back_one].kind == SPACE:
                back_one -= 1

            debug(f'  Walking back to disk[{back_one}]={self.disk2[back_one]}')
            return back_one

        end_of_disk = previous_file_index(end_of_disk)

        debug('Disk:', self.disk2)
        debug('Start:', 0)
        debug('End', end_of_disk)
        self.debug_disk2(0, end_of_disk)

        i = 0
        while i <= end_of_disk:
            current_block = self.disk2[i]
            last_file = self.disk2[end_of_disk]

            if current_block.kind == FILE:
                debug('=' * 80)
                debug('Block is not empty.')
                self.debug_disk2(i, end_of_disk)
                i += 1
                debug('-' * 80)
                continue

            debug('=' * 80)
            debug(f'  Block is empty: {current_block }')
            self.debug_disk2(i, end_of_disk)
            debug(f'  Will last file fit?  {last_file}')
            if last_file.size <= current_block.size:
                debug('  Yes.')
                debug('  Moving file to empty space.')
                # Pull file from current spot, replace with empty space.
                consumed_space, remaining_space = current_block.split(last_file.size)

                self.disk2[i] = last_file
                self.disk2[end_of_disk] = consumed_space
                if remaining_space:
                    self.disk2.insert(i+1, remaining_space)
                    # when we do this, we've increased the number of blocks.
                    # so we need to move the end of disk pointer back one.
                    end_of_disk += 1

            else:
                debug('  No.  Nothing to do.')

            debug('-' * 80)
            # Either the file was moved or it wasn't.  We're done either way.
            end_of_disk = previous_file_index(end_of_disk)



def main(data):
    data = [int(i) for i in data]
    filesystem = Filesystem(data)
    # filesystem.part_1()
    filesystem.part_2()


if __name__ == '__main__':
    # just under 100k disk size.
    data = load_data()
    # disk size 42
    data = ['2333133121414131402']
    # DEBUG = False
    main(data[0])
