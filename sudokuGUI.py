#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 30 13:23:12 2020

@author: rohith
"""

import tkinter

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
    def initialize(self,master,n):
        sudoku1 =  [[3,0,6,5,0,8,4,0,0],
                   [5,2,0,0,0,0,0,0,0],
                   [0,8,7,0,0,0,0,3,1],
                   [0,0,3,0,1,0,0,8,0],
                   [9,0,0,8,6,3,0,0,5],
                   [0,5,0,0,9,0,6,0,0],
                   [1,3,0,0,0,0,2,5,0],
                   [0,0,0,0,0,0,0,7,4],
                   [0,0,5,2,0,6,3,0,0]]
        sudoku2 =  [[0,6,7,4,2,5,0,0,0],
                   [0,0,0,1,8,0,0,6,0],
                   [8,9,0,6,0,7,0,5,2],
                   [4,0,0,0,6,0,9,1,3],
                   [6,0,2,3,9,4,5,7,0],
                   [9,7,3,8,0,1,6,2,0],
                   [0,0,0,2,4,3,7,9,5],
                   [0,2,4,9,7,6,8,0,0],
                   [0,3,0,5,1,8,2,0,0]]
        for i in range(1,n+1):
            master.rowconfigure(i,weight=1)
            tkinter.Label(master, text=i, bg='white',width=10,height=2).grid(row=i,column=0)
        for j in range(1,n+1):
            master.columnconfigure(j,weight=1)
            tkinter.Label(master, text=j, bg='white',width=10,height=2).grid(row=0,column=j)
        tkinter.Button(master,text = 'Solve Sudoku', bg='blue', width=10,height=2,command= lambda:self.sudoku_check(master,ar,n,0,0)).grid(row=0,column=0,padx=1, pady =1)
        for i in range(n):
            for j in range(n):
                if sudoku2[i][j]==0:
                    tkinter.Label(master,text = '', bg='green', width=10,height=2).grid(row=i+1,column=j+1,padx=1, pady =1)
                else:
                    tkinter.Label(master,text = sudoku2[i][j], bg='green', width=10,height=2).grid(row=i+1,column=j+1,padx=1, pady =1)
        return sudoku2
    
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
    ar = nq.initialize(master,n)
    master.mainloop()
    """if nq.nqueen(master,ar,n,0):
        #nq.printar(ar,n)
        g = gui()
        g.screen(ar,n)
    else:
        print("No solution exists")"""
