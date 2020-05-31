#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 11:04:37 2020

@author: rohith
"""

import sqlite3
import random

class SudokuGenerator:
    
    def GenerateSudoku(self,n,k):
        sudoku = self.initialize()
        sudoku = self.fillDiagonalCubes(sudoku)
        #print("Diagonals cubes filled")
        if self.solveSudoku(sudoku,n,0,0):
            sudoku = self.removeKDigits(sudoku,k)
            #print("Removed k digits")
            #self.printar(sudoku,n)
            sudokustr = ""
            for i in range(0,9):
                for j in range(0,9):
                    sudokustr = sudokustr+str(sudoku[i][j])
            return sudokustr
        else:
            print("No solution found")
            return None
    
    def initialize(self):
        sudoku = [[0 for i in range(0,9)] for j in range(0,9)]
        return sudoku
    
    def printar(self,ar,n):
        for i in range(0,n):
            for j in range(0,n):
                print(ar[i][j],end=" ")
            print()
        print()
    
    def getcube(self):
        cube = [[0 for i in range(0,3)] for j in range(0,3)]
        caseind = random.randint(0,2)
        #print(caseind)
        if caseind==0:
            for i in range(0,9):
                row = int(i/3)
                col = i%3
                cube[row][col]=i+1
            return cube
        elif caseind == 1:
            for i in range(8,-1,-1):
                row = int(i/3)
                col = i%3
                cube[row][col]=i+1
            return cube
        elif caseind==2 :
            for i in range(0,3):
                rnum = random.randint(0,8)
                row = int(rnum/3)
                col = rnum%3
                while cube[row][col]!=0:
                    rnum = random.randint(0,8)
                    row = int(rnum/3)
                    col = rnum%3
                cube[row][col]=i+1
            num=4
            for i in range(0,3):
                for j in range(0,3):
                    if cube[i][j]==0:
                        cube[i][j]=num
                        num=num+1
            #print(cube)
            return cube
    
    def fillDiagonalCubes(self,ar):
        #"get the cubes in diagonal as they are independent
        cube1 = self.getcube()
        cube2 = self.getcube()
        cube3 = self.getcube()
        for i in range(0,9):
            for j in range(0,9):
                if i<3 and j<3:
                    ar[i][j]=cube1[i][j]
                elif i>=3 and i<6 and j>=3 and j<6:
                    ar[i][j]=cube2[i-3][j-3]
                elif i>=6 and i<9 and j>=6 and j<9:
                    ar[i][j]=cube3[i-6][j-6]
        #print("Only diagonals filled")
        #self.printar(ar,n)
        return ar
    
    def constraints(self,ar,n,x,y,val):
        for i in range(0,n):
            if ar[i][y]==val:
                return False
        for j in range(0,n):
            if ar[x][j]==val:
                return False
        cur_gridx = int(x/3)
        cur_gridy = int(y/3)
        for i in range(cur_gridx*3,(cur_gridx*3)+3):
            for j in range(cur_gridy*3,(cur_gridy*3)+3):
                if ar[i][j]==val:
                    return False
        return True
            
    def solveSudoku(self,ar,n,cur_row,cur_col):
        if cur_row == n:
            return True
        if cur_col == n:
            return self.solveSudoku(ar,n,cur_row+1,0)
        if ar[cur_row][cur_col]!=0:
            return self.solveSudoku(ar,n,cur_row,cur_col+1)
        for i in range(1,n+1):
            if self.constraints(ar,n,cur_row,cur_col,i):
                ar[cur_row][cur_col]=i
                if self.solveSudoku(ar,n,cur_row,cur_col+1):
                    return True
                ar[cur_row][cur_col]=0
        return False    
        
    def removeKDigits(self,ar,k):
        while(k>0):
            ind = random.randint(0,80)
            row = int(ind/9)
            col = ind%9
            if ar[row][col]!=0:
                ar[row][col]=0
                k = k-1
        return ar
            
if __name__ == "__main__":
    conn = sqlite3.connect("SudokuDB.sqlite")
    cur = conn.cursor()

    cur.executescript('''
                DROP TABLE IF EXISTS Sudoku;
                CREATE TABLE Sudoku(
                ind            INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                sudokuLayout   TEXT UNIQUE
                 );
                 ''')
    nos = int(input("Enter number of sudoku:"))
    n = 9
    k = 40#Maximun numbers of blanks in the generated sudoku
    for i in range(0,nos):
        obj = SudokuGenerator()
        sudokustr = obj.GenerateSudoku(n,k)
        if sudokustr is not None:
            #print(sudokustr)
            cur.execute('''
                        INSERT OR IGNORE INTO Sudoku(sudokuLayout) VALUES(?) 
                        ''', (sudokustr,))
            conn.commit()
            print("successfully inserted one sudoku")
        else:
            i = i-1
    conn.close()        