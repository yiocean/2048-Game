import numpy as np
import random
import copy

class Board():
    def __init__(self):
        self.board = np.zeros((4, 4), dtype = np.uint32)
        self.tmpboard = np.zeros((4, 4), dtype = np.uint32)
        self.startNewGame()
    
    def copyBoard(self, tmp):
        self.board = tmp.board.copy()

    def newTile(self):
        list = []
        move_flag = 0
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    list.append((i, j))
                    move_flag += 1

        if move_flag != 0:
            randomList = random.choice(list)
            r = randomList[0]
            c = randomList[1]
            num = random.choices([2, 4], weights = [90, 10], k=1)[0]
            self.board[r][c] = num

        # r = random.randint(0, 3)
        # c = random.randint(0, 3)
        # num = random.choices([2, 4], weights = [90, 10], k=1)[0]
        # #num = random.choice([2, 4])
        # while self.board[r][c] != 0:
        #     r = random.randint(0, 3)
        #     c = random.randint(0, 3)
        # self.board[r][c] = num

    def getTile(self, r, c):
        return self.board[r][c]
    
    def startNewGame(self):
        self.board = np.zeros((4, 4), dtype = np.uint32)
        self.newTile()
        self.newTile()

    def printBoard(self):
        print(self.board)

    def checkWinLoseTuple(self, board, ntuple, cin_flag, score, n):
        checknum = board.check()
        if checknum == -5:
            return score, -5
        elif checknum == 100:
            return score, -1
        else:
            tmpboard = board.board.copy()
            if cin_flag == 1:
                print("current score: ", score)
                board.printBoard()
                ntuple.printTuple(tmpboard)
                ntuple.printValue(tmpboard)
                n = input("please input: ")
                #tmpboard = game.board.copy()

            tmpscore = board.move(n)
            score = score + tmpscore

            k_flag = 0
            checkBoard = board.checkBoard(tmpboard)
            
            if checkBoard < 16:
                board.newTile()
                cin_flag = 1
            else:
                n = input("Your step seems wrong. Please input the step you want to do: ")
                cin_flag = 0
                k_flag = 1

            if checkBoard >= 16 and cin_flag == 0 and k_flag == 0:
                n = input("Your step seems wrong. Please input the step you want to do: ")
            elif checkBoard < 16 and cin_flag == 0:
                cin_flag = 1

            return score, cin_flag

    def checkWinLoseContinue(self, game, ntuple, cin_flag, score, n):
        checknum = game.check()
        if checknum == -5:
            print("current score: ", score)
            game.printBoard()
            print("Lose !!")
            return score, -5, n
        elif checknum == 100:
            print("current score: ", score)
            game.printBoard()
            print("win !!")
            return score, -1, n
        else:
            tmpboard = game.board.copy()
            if cin_flag == 1:
                print("current score: ", score)
                game.printBoard()
                ntuple.printTuple(tmpboard)
                ntuple.printValue(tmpboard)
                n = input("please input: ")
                #tmpboard = game.board.copy()

            tmpscore = game.move(n)
            score = score + tmpscore

            k_flag = 0
            checkBoard = game.checkBoard(tmpboard)
            
            if checkBoard < 16:
                game.newTile()
                cin_flag = 1
            else:
                n = input("Your step seems wrong. Please input the step you want to do: ")
                cin_flag = 0
                k_flag = 1

            if checkBoard >= 16 and cin_flag == 0 and k_flag == 0:
                n = input("Your step seems wrong. Please input the step you want to do: ")
            elif checkBoard < 16 and cin_flag == 0:
                cin_flag = 1

            return score, cin_flag, n

    def move(self, direction):
        if direction == "U": #0
            return self.moveUp()
        if direction == "R": #1
            #print("moveright")
            return self.moveRight()
        if direction == "D": #2
            return self.moveDown()
        if direction == "L": #3
            return self.moveLeft()
        return -5

    def moveUp(self):
        score = 0
        cur = self.board.copy()
        for i in range(4):
            merged = [False] * 4
            for j in range(1, 4):
                if cur[j][i] != 0:
                    k = j
                    while k - 1 >= 0:
                        if cur[k - 1][i] == 0:
                            cur[k - 1][i] = cur[k][i]
                            cur[k][i] = 0
                            k -= 1
                        elif cur[k - 1][i] == cur[k][i] and not merged[k - 1]:
                            cur[k - 1][i] *= 2
                            score += cur[k - 1][i]
                            cur[k][i] = 0
                            merged[k - 1] = True
                            break
                        else:
                            break
        if np.array_equal(cur, self.board):
            return -5, cur
        return score, cur
    
    def moveDown(self):
        score = 0
        cur = self.board.copy()
        for i in range(4):
            merged = [False] * 4
            for j in range(2, -1, -1):
                if cur[j][i] != 0:
                    k = j
                    while k + 1 < 4:
                        if cur[k + 1][i] == 0:
                            cur[k + 1][i] = cur[k][i]
                            cur[k][i] = 0
                            k += 1
                        elif cur[k + 1][i] == cur[k][i] and not merged[k + 1]:
                            cur[k + 1][i] *= 2
                            score += cur[k + 1][i]
                            cur[k][i] = 0
                            merged[k + 1] = True
                            break
                        else:
                            break
        if np.array_equal(cur, self.board):
            return -5, cur
        return score, cur

    def moveRight(self):
        score = 0
        cur = self.board.copy()
        for i in range(4):
            merged = [False] * 4 
            for j in range(2, -1, -1):
                if cur[i][j] != 0:
                    k = j
                    while k + 1 < 4:
                        if cur[i][k + 1] == 0:
                            cur[i][k + 1] = cur[i][k]
                            cur[i][k] = 0
                            k += 1
                        elif cur[i][k + 1] == cur[i][k] and not merged[k + 1]:
                            cur[i][k + 1] *= 2
                            score += cur[i][k + 1]
                            cur[i][k] = 0
                            merged[k + 1] = True
                            break
                        else:
                            break
        if np.array_equal(cur, self.board):
            return -5, cur
        return score, cur
    
    def moveLeft(self):
        score = 0
        cur = self.board.copy()
        for i in range(4):
            merged = [False] * 4 
            for j in range(1, 4):
                if cur[i][j] != 0:
                    k = j
                    while k - 1 >= 0:
                        if cur[i][k - 1] == 0:
                            cur[i][k - 1] = cur[i][k]
                            cur[i][k] = 0
                            k -= 1
                        elif cur[i][k - 1] == cur[i][k] and not merged[k - 1]:
                            cur[i][k - 1] *= 2
                            score += cur[i][k - 1]
                            cur[i][k] = 0
                            merged[k - 1] = True
                            break
                        else:
                            break
        if np.array_equal(cur, self.board):
            return -5, cur
        return score, cur

    def check(self):
        flag = 10 #10:OK, 100:win, -5:lose
        total_falg = 0
        Board = self.board

        for i in range(4):
            for j in range(4):
                if Board[i][j] != 0:
                    total_falg += 1
                if Board[i][j] >= 2048:
                    #print("Win !!!")
                    flag = 100
                    return flag
        return -1

    def endOfGame(self):
        tmp = Board()
        tmp.copyBoard(self)
        r1, _ = tmp.moveUp()
        r2, _ = tmp.moveDown()
        r3, _ = tmp.moveLeft()
        r4, _ = tmp.moveRight()
        if r1 == -5 and r2 == -5 and r3 == -5 and r4 == -5:
            return True
        else:
            return False
