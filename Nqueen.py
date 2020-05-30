
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
        lst = [[0 for j in range(0,n)] for i in range(0,n)]
        for i in range(1,n+1):
            master.rowconfigure(i,weight=1)
            tkinter.Label(master, text=i, bg='white',width=10,height=2).grid(row=i,column=0)
        for j in range(1,n+1):
            master.columnconfigure(j,weight=1)
            tkinter.Label(master, text=j, bg='white',width=10,height=2).grid(row=0,column=j)
        tkinter.Button(master,text = 'Show Answer', bg='blue', width=10,height=2,command= lambda:self.check_nqueen(master,ar,n,0)).grid(row=0,column=0,padx=1, pady =1)
        for i in range(n):
            for j in range(n):
                tkinter.Label(master,text = '', bg='green', width=10,height=2).grid(row=i+1,column=j+1,padx=1, pady =1)
        return lst
    
    def printar(self,ar,n):
        for i in range(0,n):
            for j in range(0,n):
                print(ar[i][j],end=" ")
            print()
        print()
        
    def constraints(self,ar,n,x,y):
        for i in range(x,-1,-1):
            if ar[i][y]==1:
                return False
        i = x
        j = y
        while i>=0 and j>=0:
            if ar[i][j]==1:
                return False
            i = i-1
            j = j-1
        i = x
        j = y
        while i>=0 and j<n:
            if ar[i][j]==1:
                return False
            i = i-1
            j = j+1
        return True
    
    def check_nqueen(self,master,ar,n,cur_row):
    	ans = self.nqueen(master,ar,n,cur_row)
    	if not ans:
    		master.destroy()
    		print("No solution for n=",n)
            
    def nqueen(self,master,ar,n,cur_row):
        if cur_row == n:
            return True
        for j in range(0,n):
            if self.constraints(ar,n,cur_row,j):
                ar[cur_row][j]=1
                tkinter.Label(master,text = 'Q', fg='white', bg='red', width=10,height=2).grid(row=cur_row+1,column=j+1,padx=1, pady =1)
                if self.nqueen(master,ar,n,cur_row+1):
                    return True
                ar[cur_row][j]=0
                tkinter.Label(master,text = '', bg='green', width=10,height=2).grid(row=cur_row+1,column=j+1,padx=1, pady =1)
        return False
        
if __name__ == "__main__":
    #n = int(input("Enter n:"))
    n = 3
    master = tkinter.Tk(className='N Queen')
    nq = backTrack()
    ar = nq.initialize(master,n)
    master.mainloop()
    """if nq.nqueen(master,ar,n,0):
        #nq.printar(ar,n)
        g = gui()
        g.screen(a
    else:
        print("No solution exists")"""
