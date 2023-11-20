from board import Board
from tuple import Tuple
import numpy as np
import copy

if __name__ == "__main__":
    game = Board()
    ntuple = Tuple()
    score = 0
    cin_flag = 1
    n = 0
    
    while True:
        score, cin_flag, n = game.checkWinLoseContinue(game, ntuple, cin_flag, score, n)
        if score == -5 or score == -1:
            break
        else:
            continue


