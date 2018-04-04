#!/usr/bin/env python3

import random

MINE = '*'
BLOCK = ' '
BLANK = '\u2588'  # █
MARKED = '\u2691'  # ⚑


class MineSweeper:

    def __init__(self, w=8, h=8, n_mines=10):

        if w < 8 or w > 30 or h < 8 or h > 24:
            raise ValueError(
                'Board size out of range: (width: 8-30, height: 8-24')
        if n_mines > (w-1)*(h-1):
            raise ValueError(
                'Too many bombs: (max number of bombs: (width-1)*(height-1)')

        self._gameover = False
        self._w = w
        self._h = h
        self._n_mines = n_mines
        self._board = [[BLANK]*self._w for y in range(self._h)]
        self._mines = None
        self._fill_mines()

    def __str__(self):
        column_nums = '  ' + ''.join('{:2}'.format(x+1)
                                     for x in range(self._w))
        board_string = column_nums
        for y in range(self._h):
            board_string += '\n{:2}|'.format(y+1) + \
                '|'.join(self._board[y]) + '|' + \
                '{:<2}'.format(y+1)
        board_string += '\n' + column_nums
        if self._gameover:
            return board_string
        else:
            return board_string.replace(MINE, BLANK)

    def _set(self, x, y, target):
        self._board[y][x] = target

    def _fill_mines(self):
        mines = random.sample(range(self._h*self._w), self._n_mines)
        self._mines = set((mine % self._w, mine // self._w) for mine in mines)
        for x, y in self._mines:
            self._set(x, y, MINE)

    def out_of_bound(self, x, y):
        return x < 0 or x >= self._w or y < 0 or y >= self._h

    def click(self, x, y):
        if self.is_mine(x, y):
            self._gameover = True
        else:
            count = 0
            for i in range(x-1, x+2):
                for j in range(y-1, y+2):
                    if not self.out_of_bound(i, j) and self.is_mine(i, j):
                        count += 1
            if count == 0:
                self._set(x, y, BLOCK)
                for i in range(x-1, x+2):
                    for j in range(y-2, y+2):
                        if not self.out_of_bound(i, j) and self.is_blank(i, j):
                            self.click(i, j)
            else:
                self._set(x, y, str(count))

    def mark(self, x, y):
        if self.is_mine(x, y):
            self._set(x, y, MARKED)
            self._n_mines -= 1

        elif self.is_marked(x, y):
            self._set(x, y, MARKED)

        elif self.is_marked(x, y):
            if (x, y) in self._mines:
                self._set(x, y, MINE)
                self._n_mines += 1
            else:
                self._set(x, y, BLANK)

    def is_blank(self, x, y):
        return self._board[y][x] == BLANK

    def is_marked(self, x, y):
        return self._board[y][x] == MARKED

    def is_mine(self, x, y):
        return (x, y) in self._mines

    def is_gameover(self):
        return self._n_mines == 0 or self._gameover


def main():

    difficulty = ((8, 8, 10), (16, 16, 40), (24, 24, 99), (30, 24, 200))

    while True:
        try:
            level = int(input(
                'Enter difficulty (1: Beginner, 2: Intermediate, 3: Expert, 4: Insane): '))-1
            game = MineSweeper(*difficulty[level])
            break
        except (IndexError, ValueError):
            print('Invalid input! ', end='')
            continue

    print(game)

    while not game.is_gameover():

        try:
            action, y, x = input(
                'c for click, m for mark, [c/m row column]: ').split()
            i, j = int(x)-1, int(y)-1
            if action == 'c':
                game.click(i, j)
                print(game)
            elif action == 'm':
                game.mark(i, j)
                print(game)
            else:
                continue
        except (IndexError, ValueError):
            print('Invalid input! ', end='')
            continue

    print('Game Over!')
    print(game)


if __name__ == '__main__':
    main()
