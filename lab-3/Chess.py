#!/usr/bin/env python3
## 
## chessboard display based on FunChess written by Andrew Lamoureux
##

from tkinter import *
import time
import random
import numpy as np
import math
import base64

DARK_SQUARE_COLOR = '#58ae8b'
LIGHT_SQUARE_COLOR = '#feffed'


class ChessEnvironment(object):
    def __init__(self, tk_root, N):
        ## Set up canvas for drawing board
        self.root = tk_root
        self.exitFlag = False
        self.canvas = Canvas(self.root, width=500, height=500)
        self.canvas.place(x=0, y=0)
        self.canvas.img = PhotoImage(file='blackq.gif')

        squareWidth = 500 / N
        squareHeight = 500 / N
        for ridx, rname in enumerate(list('87654321')):
            for fidx, fname in enumerate(list('abcdefgh')):
                tag = fname + rname
                color = [LIGHT_SQUARE_COLOR, DARK_SQUARE_COLOR][(ridx - fidx) % 2]
                shade = ['light', 'dark'][(ridx - fidx) % 2]

                tags = [fname + rname, shade, 'square']

                self.canvas.create_rectangle(
                    fidx * squareWidth, ridx * squareHeight,
                    fidx * squareWidth + squareWidth, ridx * squareHeight + squareHeight,
                    outline=color, fill=color, tag=tags)

        self.control = Frame(self.root, width=100, height=100)
        self.control.place(x=510, y=10)
        Button(self.control, text="Exit", command=self.finish).pack(anchor=W, fill=X)

    def clear(self):
        self.canvas.delete('piece')

    def finish(self):
        # self.runEvent.set() ## signal waiting thread
        self.exitFlag = True
        self.root.destroy()

    def display(self, queens):
        """Display the board."""

        if self.exitFlag: exit(0)
        self.clear()
        for r in range(len(queens.board)):
            for c in range(len(queens.board)):
                if queens.board[c] == r:
                    self.canvas.create_image(r * (500 / len(queens.board)) + 250 / len(queens.board),
                                             c * (500 / len(queens.board)) + 250 / len(queens.board),
                                             image=self.canvas.img, tag='piece')
        self.canvas.update_idletasks()
        self.canvas.update()
