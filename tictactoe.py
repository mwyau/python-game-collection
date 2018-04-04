#!/usr/bin/env python3


class TicTacToe:

    def __init__(self, board_size=3):
        self.BOARD_SIZE = board_size
        self._board = [
            [None] * self.BOARD_SIZE for i in range(self.BOARD_SIZE)]

    def __str__(self):

        hori_line = ' ' + '-'*(self.BOARD_SIZE*2+1)

        board_string = '  ' + ' '.join(str(s)
                                       for s in range(1, self.BOARD_SIZE+1)) + '\n'
        board_string += hori_line
        for i in range(self.BOARD_SIZE):
            board_string += '\n' + str(i+1) + '|'
            for j in range(self.BOARD_SIZE):
                if self._board[i][j] is not None:
                    board_string += self._board[i][j]
                else:
                    board_string += ' '
                board_string += '|'

            board_string += '\n' + hori_line

        return board_string

    def place(self, player, x, y):
        if self._board[x][y] is None:
            self._board[x][y] = player
            return True
        else:
            # Return False if placement is invalid
            return False

    def get_winner(self):

        # Check row
        for i in range(self.BOARD_SIZE):
            player = self._board[i][0]
            if player is not None and \
                    all(player == self._board[i][j] for j in range(1, self.BOARD_SIZE)):
                return player

        # Check column
        for j in range(self.BOARD_SIZE):
            player = self._board[0][j]
            if player is not None and \
                    all(player == self._board[i][j] for i in range(1, self.BOARD_SIZE)):
                return player

        # Check diagonal
        player = self._board[0][0]
        if player is not None and \
                all(player == self._board[i][i] for i in range(1, self.BOARD_SIZE)):
            return player
        player = self._board[0][self.BOARD_SIZE-1]
        if player is not None and \
                all(player == self._board[i][self.BOARD_SIZE-1-i]
                    for i in range(1, self.BOARD_SIZE)):
            return player

        return None


def test_winner():
    game = TicTacToe()
    game.place('X', 0, 0)
    game.place('X', 1, 1)
    game.place('X', 2, 2)
    assert game.get_winner() == 'X'


def test_placement():
    game = TicTacToe()
    game.place('X', 0, 0)
    assert not game.place('X', 0, 0)


def main():
    while True:
        player = input('Which player goes first? [X/O]: ')
        if player in ('X', 'O'):
            break
        else:
            print('Invalid player! ', end='')
            continue

    game = TicTacToe()
    print(game)

    while True:
        try:
            x, y = input('Player ' + player +
                         '\'s turn, enter coordinate [row column]: ').split(' ')
            i, j = int(x)-1, int(y)-1
            assert i >= 0 and i <= game.BOARD_SIZE-1
            assert j >= 0 and j <= game.BOARD_SIZE-1
            if game.place(player, i, j):
                print(game)
                player = 'O' if player == 'X' else 'X'
                winner = game.get_winner()
                if winner:
                    print('Player ' + winner + ' has won!')
                    break
            else:
                print('Coordinate occupied! Please try again.')

        except (ValueError, AssertionError):
            print('Invalid input! Please try again.')


if __name__ == '__main__':
    main()
