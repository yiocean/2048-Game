from board import Board
from tuple import Tuple
import numpy as np
import copy
import os
import openpyxl
import csv

if __name__ == "__main__":

    #creat Excel
    exl = openpyxl.Workbook()
    exl.save('Tuple2.xlsx')
    exl = openpyxl.load_workbook('Tuple2.xlsx') 
    sheet1 = exl['Sheet']
    sheet1.cell(1, 1).value = 'Game number' #(row, col) = (1, 1)
    sheet1.cell(1, 2).value = 'Win or lose'
    sheet1.cell(1, 3).value = 'Final Score'
    exl.save('Tuple2.xlsx')

    #creat csv file -> record step
    row = ['current num', 'win lose continue','cur score', 'chose', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 'reward']
    # win = 1, lose = -1, continue = 0
    csvfile = open('step3.csv', 'w', newline='')
    csvfile = csv.writer(csvfile)
    csvfile.writerow(row)
    
    ntuple = Tuple()
    
    winCot = 0
    loseCot = 0
    #highestScore = 0
    #playCot = 0 # record how many board had played
    #n = 0
    #list = ["U", "R", "D", "L"]
    list = ["R", "D", "L", "U"]

    k = 1000 #episode
    final = np.zeros((k, 3), dtype = np.uint32)
    score200 = []
    score200sum = 0
    
    for j in range(k):
        original_tuple = np.copy(ntuple.tuple)
        game = Board()
        winFlag = 0
        score = 0
        cin_flag = -1
        #record init board
        row = [j, 0, score, 'init board'] + [game.board[i][j] for i in range(4) for j in range(4)] + [0]
        csvfile.writerow(row)
        #final[i][0] = j
        while True:
            #score, cin_flag, n = game.checkWinLoseContinue(game, ntuple, cin_flag, score, n)
            tmp = Board()
            tmax = -1
            irecord = -1
            scorelist = [0, 0, 0, 0]
            r = 0

            # find max step
            for i in range(4):
                tmp.board = game.board
                m, tmp.board = tmp.move(list[i]) # m = reward
               # tmp.board = boardNotUse #check
                scorelist[i] = m
                checksum = tmp.check()
                if checksum == -5:
                    continue
                elif checksum == 100:
                    winFlag = 1
                    irecord = i
                    break
                else:
                    if m != -5:
                        tmp.newTile()
                        t = ntuple.getTupleValueSum(tmp.board) + m
                        if t > tmax:
                            tmax = t
                            irecord = i
            
            #get tuple 1
            getT1 = ntuple.getTupleValueSum(game.board)
            if winFlag == 1:
                print("win")
                r, game.board = game.move(list[i])
                game.newTile()
                getT2 = ntuple.getTupleValueSum(game.board)
                score += r
                cin_flag = 1 #win or lose

                # more than 2048 (more than 16384 -> 16384)
                ntuple.udpTuple(game.board, r + (getT2 - getT1))
                row = [j, 1, score, list[irecord]] + [game.board[i][j] for i in range(4) for j in range(4)]
                #csvfile.writerow(row)
                break
            elif tmax == -1: #四個方向都不能走 -> 遊戲結束
                print("lose")
                maxscore = -1
                irecordm = -1
                for w in range(4): #找score最大的走
                    if scorelist[w] > maxscore:
                        maxscore = scorelist[w]
                        irecordm = w
                r, game.board = game.move(list[irecordm])
                score += r
                cin_flag = 0
                row = [j, -1, score, 'no move'] + [game.board[i][j] for i in range(4) for j in range(4)]
                break
            else:
                r, tboard = game.move(list[irecord])
                game.board = tboard
                #get tuple 2
                
                score += r
                if r != -5:
                    game.newTile()
                
                getT2 = ntuple.getTupleValueSum(game.board)
                row = [j, 0, score, list[irecord]] + [game.board[i][j] for i in range(4) for j in range(4)]
                #game.printBoard()
                #print("Score: ", score)
            
            row = row + [r]
            ntuple.udpTuple(game.board, r + (getT2 - getT1))
            csvfile.writerow(row)

            # test if tuple value change
            # changed_indices = np.where(ntuple.tuple != original_tuple)
            # for r, c in zip(*changed_indices):
            #     print(f"position ({r}, {c}) 's value from {original_tuple[r, c]} change to {ntuple.tuple[r, c]}")             
            

        game.printBoard()
        print("Score: ", score)
        print("k: ", j)
        
        if cin_flag == 0:
            loseCot += 1
        elif cin_flag == 1:
            winCot += 1

        final[j][0] = j
        final[j][1] = cin_flag
        final[j][2] = score
        
        sheet1.cell(j+2, 1).value = j
        sheet1.cell(j+2, 2).value = cin_flag
        sheet1.cell(j+2, 3).value = score
        exl.save('Tuple2.xlsx')

        score200sum += score
        if j % 200 == 0:
            score200.append(score200sum / j)
            score200sum = 0
    
    print(winCot / k)
    print(final)
    sheet1.cell(k+5, 1).value = (winCot / k)
    exl.save('Tuple2.xlsx')
    # print(score200sum)
    print(score200)
        #exl.save

    #csvfile.close()
