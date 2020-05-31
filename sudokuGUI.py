#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 30 13:23:12 2020

@author: rohith
"""

import tkinter
import sqlite3
import random

class gui:
    
    def screen(self,ar,n):
        master = tkinter.Tk(className='N Queen')
        for i in range(1,n+1):
            master.rowconfigure(i,weight=1)
            tkinter.Label(master, text=i, bg='white',width=10,height=2).grid(row=i,column=0)
        for j in range(1,n+1):
            master.columnconfigure(j,weight=1)
            tkinter.Label(master, text=j, bg='white',width=10,height=2).grid(row=0,column=j)
        tkinter.Button(master,text = 'click me', bg='blue', width=10,height=2).grid(row=0,column=0,padx=1, pady =1)
        for i in range(0,n):
            for j in range(0,n):
                if ar[i][j]==1:
                    tkinter.Label(master,text = 'Q', fg='white', bg='red', width=10,height=2).grid(row=i+1,column=j+1,padx=1, pady =1)
                else:
                    tkinter.Label(master,text = '', bg='green', width=10,height=2).grid(row=i+1,column=j+1,padx=1, pady =1)
        master.mainloop()
        
class backTrack:
    solved = False
    
    def getRandomSudoku(self):
        sudokulayout = []
        sudokustr = None
        caseind = random.randint(0,1)
        if caseind==0:
            sudokulayout =  [[3,0,6,5,0,8,4,0,0],
                       [5,2,0,0,0,0,0,0,0],
                       [0,8,7,0,0,0,0,3,1],
                       [0,0,3,0,1,0,0,8,0],
                       [9,0,0,8,6,3,0,0,5],
                       [0,5,0,0,9,0,6,0,0],
                       [1,3,0,0,0,0,2,5,0],
                       [0,0,0,0,0,0,0,7,4],
                       [0,0,5,2,0,6,3,0,0]]
        if caseind==1:
            sudokulayout =  [[0,6,7,4,2,5,0,0,0],
                        [0,0,0,1,8,0,0,6,0],
                        [8,9,0,6,0,7,0,5,2],
                        [4,0,0,0,6,0,9,1,3],
                        [6,0,2,3,9,4,5,7,0],
                        [9,7,3,8,0,1,6,2,0],
                        [0,0,0,2,4,3,7,9,5],
                        [0,2,4,9,7,6,8,0,0],
                        [0,3,0,5,1,8,2,0,0]]
        try:
            conn = sqlite3.connect("SudokuDB.sqlite")
            cur = conn.cursor()
            cur.execute(''' SELECT COUNT(*) FROM Sudoku ''')
            count = cur.fetchone()#this is a tupule
            randind = random.randint(1,count[0])
            print("Fetcing Sudoku No-", randind, "from DB.....")
            cur.execute(''' SELECT sudokuLayout from Sudoku WHERE ind = ? ; ''',(randind,))
            sstr = cur.fetchone()#get a random tupule
            sudokustr = sstr[0]
            sudokulayout = []
            #print(sudokustr)
            for i in range(0,9):
                lst = []
                for j in range(0,9):
                    lst.append(int(sudokustr[(9*i)+j]))
                sudokulayout.append(lst)
            conn.close()
        except:
            print("Couldn't connect to database(Run Generate_sudoku.py to create and populate database)")
        return sudokulayout
        
    def initialize(self,master,sudokulayout,n):
        print("Initializing Window")
        self.solved=False
        for i in range(1,n+1):
            master.rowconfigure(i,weight=1)
            tkinter.Label(master, text=i, bg='white',width=10,height=2).grid(row=i,column=0)
        for j in range(1,n+1):
            master.columnconfigure(j,weight=1)
            tkinter.Label(master, text=j, bg='white',width=10,height=2).grid(row=0,column=j)
        tkinter.Button(master,text = 'Solve Sudoku', bg='blue', width=10,height=2,command= lambda:self.sudoku_check(master,ar,n,0,0)).grid(row=0,column=0,padx=1, pady =1)
        elist = []
        esize=0
        for i in range(n):
            for j in range(n):
                if sudokulayout[i][j]==0:#change sudoku here
                    elist.append(tkinter.Entry(master,bg='white', width=6, borderwidth=10, font = ('Verdana',15)))
                    elist[esize].grid(row=i+1,column=j+1,padx=1, pady =1,sticky=tkinter.W)
                    esize = esize +1
                else:
                    tkinter.Label(master,text = sudokulayout[i][j], bg='green', width=10,height=2).grid(row=i+1,column=j+1,padx=1, pady =1)#change sudoku here
        tkinter.Button(master,text = 'check', bg = 'purple', fg = 'white', width=7,height=2,command= lambda:self.checkuserans(sudokulayout,elist,n)).grid(row=10,column=8,padx=1,pady=1)
        
    def checkuserans(self,ar,elist,n):
        if self.solved:
            print("Solution Revealed")
            tkinter.Label(master,text = 'Solution\nRevealed', bg='Red', width=10,height=2).grid(row=10,column=2,padx=1, pady =1)
            return
        
        print("In checkans")
        esize = 0
        error = False
        inputs = [e.get() for e in elist]
        for i in inputs:
            if not i:
                print("One or more Values not entered")
                tkinter.Label(master,text = 'Wrong\n(Blanks)', bg='Red', width=10,height=2).grid(row=10,column=2,padx=1, pady =1)
                error =True
                break
            else:
                try:
                    num = int(i)
                    if num<=0 or num>9:
                        print("Invald number Entered")
                        tkinter.Label(master,text = 'Wrong\nInvalid Num', bg='Red', width=10,height=2).grid(row=10,column=2,padx=1, pady =1)
                        error =True
                        break
                except:
                    print("Invalid Character Entered")
                    tkinter.Label(master,text = 'Wrong\nInvalid Char', bg='Red', width=10,height=2).grid(row=10,column=2,padx=1, pady =1)
                    error =True
                    break
        if error:
            return
        checkans = []
        for i in range(n):
            lst = []
            for j in range(n):
                if ar[i][j]!=0:
                    lst.append(ar[i][j])
                else:
                    lst.append(int(inputs[esize]))
                    esize = esize+1
            checkans.append(lst)
        #self.printar(checkans,n)
        for i in range(n):
            for j in range(n):
                if not self.constraints(checkans,n,i,j,checkans[i][j]):
                    tkinter.Label(master,text = 'Wrong', bg='Red', width=10,height=2).grid(row=10,column=2,padx=1, pady =1)
                    break
        tkinter.Label(master,text = 'Correct', bg='Green', width=10,height=2).grid(row=10,column=2,padx=1, pady =1)
        return
        
    def printar(self,ar,n):
        for i in range(0,n):
            for j in range(0,n):
                print(ar[i][j],end=" ")
            print()
        print()
        
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
    
    def sudoku_check(self,master,ar,n,cur_row,cur_col):
        ans = self.sudoku(master,ar,n,cur_row,cur_col)
        self.solved = True
        if not ans:
            master.destroy()
            print("No solution found")

    def sudoku(self,master,ar,n,cur_row,cur_col):
        if cur_row == n:
            return True
        if cur_col == n:
            return self.sudoku(master,ar,n,cur_row+1,0)
        if ar[cur_row][cur_col]!=0:
            return self.sudoku(master,ar,n,cur_row,cur_col+1)
        for i in range(1,n+1):
            if self.constraints(ar,n,cur_row,cur_col,i):
                ar[cur_row][cur_col]=i
                tkinter.Label(master,text = i, fg='white', bg='red', width=10,height=2).grid(row=cur_row+1,column=cur_col+1,padx=1, pady =1)
                if self.sudoku(master,ar,n,cur_row,cur_col+1):
                    return True
                ar[cur_row][cur_col]=0
                tkinter.Label(master,text = '', bg='green', width=10,height=2).grid(row=cur_row+1,column=cur_col+1,padx=1, pady =1)
        return False
        
if __name__ == "__main__":
    #n = int(input("Enter n:"))
    n = 9
    master = tkinter.Tk(className='sudoku')
    nq = backTrack()
    ar =nq.getRandomSudoku()
    nq.initialize(master,ar,n)
    master.mainloop()
    """if nq.sudoku(master,ar,n,0):
        #nq.printar(ar,n)
        g = gui()
        g.screen(ar,n)
    else:
        print("No solution exists")"""
