import pandas as pd
import numpy as np
from random import randrange
import pygame

ROW_RANGE = 6
COL_RANGE = 7

class Player(object):
    def __init__(self, color):
        self.id = color

    def getInput(self):
        return int(input('Player 1 enter column (1-7):')) - 1

class RandomPlayer(object):
    def __init__(self, color):
        self.id = color

    def getInput(self):
        return int(randrange(7))

class GameLogic(object):
    def __init__(self, row_num, col_num, player1, player2):
        self.ROW_RANGE = row_num
        self.COL_RANGE = col_num
        self.board = np.zeros((self.ROW_RANGE,self.COL_RANGE))
        self.player1 = player1
        self.player2 = player2

    def resetGame(self):
        """Reset the board to all nulls"""
        self.board = np.zeros((self.ROW_RANGE, self.COL_RANGE))

    def validInput(self,col):
        """check if the column user chooses in within range and is not full"""
        return ((col<self.COL_RANGE) & (self.board[0][col]==0))

    def getNextRow(self,col):
        """Find the row for column chosen by the user"""
        i=self.ROW_RANGE-1
        while(i>=0):
            if self.board[i][col]==0:
                return i
            i-=1

    def checkWin(self, row,col, turn):
        board = self.board
        """Check all possible winning combinations to see if user wins"""
        #horizontal
        """"""
        for c in range(COL_RANGE-3):
            if set(board[row,c: c + 4])=={turn}: return True
        #vertical
        if row<3 and set(board[row:row+4,col])=={turn}: return True
        # if set(board[min(ROW_RANGE-1, row+4)][col])=={1}: return True
        #diagonalupward
        for r in range(ROW_RANGE-3,ROW_RANGE):
            for c in range(COL_RANGE - 3):
                if (board[r][c]==turn and
                        board[r - 1][c + 1] == turn and
                        board[r - 2][c + 2] == turn and
                        board[r - 3][c + 3] == turn
                ): return True
        #diagonal2
        for r in range(0,ROW_RANGE-3):
            for c in range(COL_RANGE - 3):
                if (board[r][c]==turn and
                        board[r - 1][c -1] == turn and
                        board[r - 2][c - 2] == turn and
                        board[r - 3][c - 3] == turn
                ): return True

    def play(self):
        board = self.board
        turn = 1
        while(True):
            if len(board[board==0])==0:
                print('Draw')
                break
            print(board.astype(int))
            if turn==1:
                while(True):
                    col = self.player1.getInput()
                    if self.validInput(col):
                        break
                    print('Invalid input. Please try again')
                row = self.getNextRow(col)
                board[row][col] = self.player1.id
            elif turn==2:
                while(True):
                    col = self.player2.getInput()
                    if self.validInput(col):
                        break
                    print('Invalid input. Please try again')
                row = self.getNextRow(col)
                board[row][col] = self.player2.id

            # print(row,':',min(ROW_RANGE - 1, row + 4))
            if self.checkWin(row,col,turn):
                if turn==1: x = self.player1.id
                else: x = self.player2.id
                print('Player ',x,' wins!!')
                break
            turn = 3 - turn




if __name__ == '__main__':
    yellowPlayer = Player(1)
    redPlayer = RandomPlayer(2)
    c4 = GameLogic(ROW_RANGE, COL_RANGE, yellowPlayer, redPlayer)
    c4.play()


