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

    def copy(self, q):
        """Copy a candidate solution (prevent aliasing)"""
        self.board = q.board.copy()

    def actions(self):
        """Return a list of possible actions given the current placements."""
        possible_actions = []
        N = len(self.board)
        for col in range(N):
            for row in range(N):
                if self.board[col] != row:
                    new_queens = Queens(N)
                    new_queens.board = self.board.copy()
                    new_queens.board[col] = row
                    possible_actions.append(new_queens)
        return possible_actions

    def cost(self):
        """Compute the cost of this solution."""
        N = len(self.board)

        row_freq = N * [0]
        diag_freq = 2 * N * [0] 
        anti_diag_freq = 2 * N * [0]

        for i in range(N):
            row_freq[self.board[i]] += 1
            diag_freq[N - 1 - self.board[i] + i] += 1
            anti_diag_freq[self.board[i] + i] += 1
        
        ans = 0
        for i in range(2 * N):
            if i < N:
                ans += math.comb(row_freq[i], 2)
            ans += math.comb(diag_freq[i], 2)
            ans += math.comb(anti_diag_freq[i], 2)
        
        return int(ans)


class QueensSearch(object):

    def __init__(self, root, N):
        self.root = root
        self.N = N

    def run(self):
        env = Chess.ChessEnvironment(self.root, self.N)
        x = Queens(self.N)
        steps = 0
        while x.cost() > 0:
            next = min(x.actions(), key=lambda queens: queens.cost())
            if next.cost() < x.cost():
                x = next
            else:
                x = Queens(self.N)
            env.display(x)
            steps += 1
            time.sleep(0.1)
        print("Solved after {} steps.\n".format(steps))


if __name__ == '__main__':
    ## Initialize environemnt
    root = Tk()
    root.title("N-Queens")
    root.geometry("600x500")
    search = QueensSearch(root, 8)
    search.run()
    root.mainloop()
