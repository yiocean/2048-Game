from board import Board
import numpy as np
import random
import os
import math

class Tuple():
    def __init__(self):
        # self.episode = []
        # self.net = []
        self.alpha = 0.0025
        self.gamma = 1.0
        # self.resetCount()

        self.buildTuple()

    def buildTuple(self):
        #self.tuple = np.random.uniform(0, 1, (17, 50625))
        self.tuple = np.zeros((17, 50625))
        #self.tuple = np.zeros((17))
        self.value = np.zeros((17))

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
        #return min(max(sumnum, 0), 50624)
    
    def getTupleValueSum(self, board):
        sumnum = 0
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
    
    #def findMaxStep()
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

    
    # def getTupleValue(self, board):
    #     self.tuple[0] = self.cot16(board[0][0], board[0][1], board[1][0], board[1][1])
    #     self.tuple[1] = self.cot16(board[0][2], board[0][3], board[1][2], board[1][3])
    #     self.tuple[2] = self.cot16(board[2][0], board[2][1], board[3][0], board[3][1])
    #     self.tuple[3] = self.cot16(board[2][2], board[2][3], board[3][2], board[3][3])
    #     for i in range(4):
    #         self.tuple[i+3] = self.cot16(board[i][0], board[i][1], board[i][2], board[i][3])
    #     for i in range(4):
    #         self.tuple[i+7] = self.cot16(board[0][i], board[1][i], board[2][i], board[3][i])
    #     self.tuple[12] = self.cot16(board[0][1], board[0][2], board[1][1], board[1][2])
    #     self.tuple[13] = self.cot16(board[1][0], board[1][1], board[2][0], board[2][1])
    #     self.tuple[14] = self.cot16(board[1][1], board[1][2], board[2][1], board[2][2])
    #     self.tuple[15] = self.cot16(board[1][2], board[1][3], board[2][1], board[2][2])
    #     self.tuple[16] = self.cot16(board[2][1], board[2][2], board[3][1], board[3][2])
    
        
    def printTuple(self, board):
        self.getTupleValue(board)
        for i in range(17):
            print("The number of tuple", i, " is ", self.tuple[i])

    
    def getValue(self, board):
        self.value[0] = board[0][0] + board[0][1] + board[1][0] + board[1][1]
        self.value[1] = board[0][2] + board[0][3] + board[1][2] + board[1][3]
        self.value[2] = board[2][0] + board[2][1] + board[3][0] + board[3][1]
        self.value[3] = board[2][2] + board[2][3] + board[3][2] + board[3][3]
        for i in range(4):
            self.value[i+3] = board[i][0] + board[i][1] + board[i][2] + board[i][3]
        for i in range(4):
            self.value[i+7] = board[0][i] + board[1][i] + board[2][i] + board[3][i]
        self.value[12] = board[0][1] + board[0][2] + board[1][1] + board[1][2]
        self.value[13] = board[1][0] + board[1][1] + board[2][0] + board[2][1]
        self.value[14] = board[1][1] + board[1][2] + board[2][1] + board[2][2]
        self.value[15] = board[1][2] + board[1][3] + board[2][1] + board[2][2]
        self.value[16] = board[2][1] + board[2][2] + board[3][1] + board[3][2]

    def printValue(self, board):
        valuesum = 0
        self.getValue(board)
        for i in range(17):
            valuesum += self.value[i]
        print("sum value is ", valuesum)
        return valuesum