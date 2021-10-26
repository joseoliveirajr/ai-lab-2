import time
import random
import numpy as np
import math
from tkinter import *
import threading

import Chess


class Queens(object):
    """An N-queens candidate solution."""

    def __init__(self, N):
        """A random N-queens instance. There is a queen in every column. The
queen in column i is in row board[i]"""
        self.board = dict()
        for col in range(N):
            row = random.choice(range(N))
            self.board[col] = row
        print(self.board)

    def copy(self, q):
        """Copy a candidate solution (prevent aliasing)"""
        self.board = q.board.copy()

    def actions(self):
        """Return a list of possible actions given the current placements."""
        possible_actions = []
        N = len(self.board)
        for col in range(N):
            for row in range(N):
                new_board = self.board.copy()
                new_board[col] = row
                possible_actions.append(new_board)
        return possible_actions

    def cost(self):
        """Compute the cost of this solution."""
        attacking_pairs_number = 0
        N = len(self.board)

        # Rows
        print("Rows")
        for row in range(N):
            queens_number = 0
            for col in range(N):
                if self.board[col] == row:
                    queens_number += 1
            print("Queens number:", queens_number)
            attacking_pairs_number += math.comb(queens_number, 2)
        print("Attacking:", attacking_pairs_number)


        # Diagonals
        for i in range(N):
            queens_number = 0
            for row in range(N):
                if row + i > 8:
                    continue
                if self.board[row] == row + i:
                    queens_number += 1
            attacking_pairs_number += math.comb(queens_number, 2)

        return attacking_pairs_number



class QueensSearch(object):

    def __init__(self, root, N):
        self.root = root
        self.N = N

    def run(self):
        env = Chess.ChessEnvironment(self.root, self.N)
        x = Queens(self.N)
        steps = 0
        while x.cost() > 0:
            ####################
            # YOU FILL THIS IN #
            ####################
            env.display(x)
            steps += 1
        print("Solved after {} steps.\n".format(steps))


if __name__ == '__main__':
    ## Initialize environemnt
    root = Tk()
    root.title("N-Queens")
    root.geometry("600x500")
    search = QueensSearch(root, 8)
    search.run()
    root.mainloop()
