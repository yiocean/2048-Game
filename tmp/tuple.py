from board import Board
import numpy as np
import random
import os
import math
import time

class Tuple():
    def __init__(self):
        self.tuple = []
        self.alpha = 0.00025
        self.gamma = 1.0
        self.maxtile = 0
        self.resetCount()

        if os.path.isfile("tupleNet/tuple1.npy"):
            print("Found tuple")
            self.loadTuple("tupleNet/tuple")
            print("Completed")
        else:
            print("Building tuple")
            self.buildTuple()
            print("Completed")

    def buildTuple(self):
        #self.tuple = np.random.uniform(0, 1, (17, 50625))
        self.tuple = np.zeros((17, 50625))
        #self.tuple = np.zeros((17))
        self.value = np.zeros((17))

    def loadTuple(self, filename):
        self.value = np.zeros((17))
        for i in range(17):
            self.tuple.append(np.load(filename+str(i+1)+".npy"))
            print(self.tuple[i])

    def saveTuple(self):
        for i in range(17):
            np.save("tupleNet/tuple%d" % (i+1), self.tuple[i])

    def findPowerOfTwo(self, number):
        power = math.log(number, 2)
        return power

    def cot16(self, a1, b1, c1, d1):
        a = 0
        b = 0
        c = 0
        d = 0
        sumnum = 0
        if a1 != 0:
            a = self.findPowerOfTwo(a1)
        else:
            a = a1
        if b1 != 0:
            b = self.findPowerOfTwo(b1)
        else:
            b = b1
        if c1 != 0:
            c = self.findPowerOfTwo(c1)
        else:
            c = c1
        if d1 != 0:
            d = self.findPowerOfTwo(d1)
        else:
            d = d1

        sumnum = a + b * 15 + c * 15 * 15 + d * 15 * 15 * 15
        return int(sumnum)
    
    def getTupleValueSum(self, board):
        sumnum = 0
        for i in range(17):
            self.value[i] = 0
        
        self.value[0] = self.tuple[0][self.cot16(board[0][0], board[0][1], board[1][0], board[1][1])]
        self.value[1] = self.tuple[1][self.cot16(board[0][2], board[0][3], board[1][2], board[1][3])]
        self.value[2] = self.tuple[2][self.cot16(board[2][0], board[2][1], board[3][0], board[3][1])]
        self.value[3] = self.tuple[3][self.cot16(board[2][2], board[2][3], board[3][2], board[3][3])]
        for i in range(4):
            self.value[i+3] = self.tuple[i+3][self.cot16(board[i][0], board[i][1], board[i][2], board[i][3])]
        for i in range(4):
            self.value[i+7] = self.tuple[i+7][self.cot16(board[0][i], board[1][i], board[2][i], board[3][i])]
        self.value[12] = self.tuple[12][self.cot16(board[0][1], board[0][2], board[1][1], board[1][2])]
        self.value[13] = self.tuple[13][self.cot16(board[1][0], board[1][1], board[2][0], board[2][1])]
        self.value[14] = self.tuple[14][self.cot16(board[1][1], board[1][2], board[2][1], board[2][2])]
        self.value[15] = self.tuple[15][self.cot16(board[1][2], board[1][3], board[2][1], board[2][2])]
        self.value[16] = self.tuple[16][self.cot16(board[2][1], board[2][2], board[3][1], board[3][2])]

        # for i in range(17):
        #     if self.value[i] > 50625

        for i in range(17):
            sumnum += self.tuple[i][int(self.value[i])]

        return sumnum
    
    def udpTuple(self, board, difference):
        tmpr = difference * self.alpha
        self.tuple[0][self.cot16(board[0][0], board[0][1], board[1][0], board[1][1])] += tmpr
        self.tuple[1][self.cot16(board[0][2], board[0][3], board[1][2], board[1][3])] += tmpr
        self.tuple[2][self.cot16(board[2][0], board[2][1], board[3][0], board[3][1])] += tmpr
        self.tuple[3][self.cot16(board[2][2], board[2][3], board[3][2], board[3][3])] += tmpr
        for i in range(4):
            self.tuple[i+3][self.cot16(board[i][0], board[i][1], board[i][2], board[i][3])] += tmpr
        for i in range(4):
            self.tuple[i+7][self.cot16(board[0][i], board[1][i], board[2][i], board[3][i])] += tmpr
        self.tuple[12][self.cot16(board[0][1], board[0][2], board[1][1], board[1][2])] += tmpr
        self.tuple[13][self.cot16(board[1][0], board[1][1], board[2][0], board[2][1])] += tmpr
        self.tuple[14][self.cot16(board[1][1], board[1][2], board[2][1], board[2][2])] += tmpr
        self.tuple[15][self.cot16(board[1][2], board[1][3], board[2][1], board[2][2])] += tmpr
        self.tuple[16][self.cot16(board[2][1], board[2][2], board[3][1], board[3][2])] += tmpr
    
        
    def printTuple(self, board):
        self.getTupleValue(board)
        for i in range(17):
            print("The number of tuple", i, " is ", self.tuple[i])

    def takeAction(self, list, pre):
        irecord = -1
        tmax = -10000
        tmp = Board()
        for i in range(4):
            tmp.copyBoard(pre)
            r, tmp.board = tmp.move(list[i])
            if r != -5:
                tmp.newTile()
                t = self.getTupleValueSum(tmp.board) + r
                if t > tmax:
                    tmax = t
                    irecord = i

        if irecord != -1:
            tmp.copyBoard(pre)
            r, cur = pre.move(list[irecord])
            return r, cur
        else :
            return -1, -1
    
    def printValue(self, board):
        valuesum = 0
        self.getValue(board)
        for i in range(17):
            valuesum += self.value[i]
        print("sum value is ", valuesum)
        return valuesum
    
    # record % of tiles
    def resetCount(self):
        self.maxtile = 0
        self.count = [0 for i in range(25)]
    
    def addCount(self,b):
        mt = 0
        for pos in range(16):
            r = pos // 4
            c = pos % 4
            t = b.board[r][c]
            t = int(self.findPowerOfTwo(t))
            if t > mt :
                mt = t
            if mt > self.maxtile :
                self.maxtile = mt
        for idx in range(1, mt + 1):
            self.count[idx] += 1

    
    def printCount(self, milestone, file):
        for i in range(self.maxtile, max(self.maxtile-6,1), -1):
            print("{}: {:.2%}".format((np.int32(1) << np.int32(i)), (self.count[i] / milestone)))
            line = "{}: {:.2%}\n".format((np.int32(1) << np.int32(i)), (self.count[i] / milestone))
            file.write(line)
