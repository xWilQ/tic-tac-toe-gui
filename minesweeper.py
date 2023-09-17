import tkinter as tk
from tkinter import font
import random as random

window = tk.Tk()
window.geometry("500x600")
window.title("Minesweeper")

gridFrame = tk.Frame(master=window)
gridFrame.pack(pady=20)

infoFrame = tk.Frame(master=window)
infoFrame.pack()

cells = {} #Dictionary to store needed data for each cell. 0 = buttonObj, 1 = row, 2 = cell, 3 = symbol
cellsCleared = 0
cellNumber = 0
boardSize = 8
mines = 0
flags = 0

def CreateMines():
    global mines
    for i in range(10):
        randomCell = random.randrange(len(cells))
        #cells[randomCell]["button"].config(text="X", font=font.Font(size=18)) #SHOW MINES IN GUI
        cells[randomCell]["symbol"] = "X"
        mines += 1

def checkNeighbors(thisCell):
    
    num = [-9, -8, -7, -1, +1, +7, +8, +9] #Numbers to add to the cell number to get the surrounding cells

    for i in range (len(num)):
        
        n = num[i]
        neighborCell = thisCell + n
        
        if neighborCell >= 0 and neighborCell < 64: #Check if the neighborCell is on the board
            
            row = cells[thisCell]["row"]
            neighborRow = cells[neighborCell]["row"]
            col = cells[thisCell]["col"]
            neighborCol = cells[neighborCell]["col"]
            
            if neighborRow == row - 1 or neighborRow == row or neighborRow == row + 1:
                if neighborCol == col - 1 or neighborCol == col or neighborCol == col + 1:
                    
                    if cells[neighborCell]["symbol"] != "X" and cells[neighborCell]["state"] == "enabled":
                        bombs = cells[neighborCell]["symbol"]
                        cells[neighborCell]["button"].config(text=bombs, font=font.Font(size=18), bg="white", state="disabled")#Reveal the cell
                        cells[neighborCell]["state"] = "disabled"
                        global cellsCleared
                        cellsCleared += 1    
                 
def onClick(event, clickedCell):
    
    #print(f"Clicked on cell {cells[clickedCell]}")
    
    if cells[clickedCell]["state"] == "disabled":
        return
    
    if cells[clickedCell]["symbol"] == "X":
        cells[clickedCell]["button"].config(text= cells[clickedCell]["symbol"], font=font.Font(size=18), fg="red", bg="red", state="disabled")
        GameOver()
        return
    
    symbol = cells[clickedCell]["symbol"]
    cells[clickedCell]["button"].config(text=symbol, font=font.Font(size=18), bg="white", state="disabled")
    cells[clickedCell]["state"] = "disabled"
    global cellsCleared
    cellsCleared += 1
    
    checkNeighbors(clickedCell)

    if cellsCleared >= cellNumber - mines:
        print(f"Cleared {cellsCleared} out of {cellNumber - mines} cells")
        Win()
    
  
def PlaceFlag(event, thisCell):
    
    if cells[thisCell]["flag"] == False:
        cells[thisCell]["button"].config(text="?", font=font.Font(size=18), bg="green")
        cells[thisCell]["flag"] = True
        cells[thisCell]["state"] = "disabled"
    
    elif cells[thisCell]["flag"] == True:
        cells[thisCell]["button"].config(text="", bg="grey")
        cells[thisCell]["flag"] = False
        cells[thisCell]["state"] = "enabled"
    """" 
    if cells[thisCell]["symbol"] == "X" and cells[thisCell]["flag"] == True:
        global flags
        print("Flagged a mine")
        flags += 1
        
    if flags == mines:
        print("Flagged all mines")
        #Win()
    """
    
def AssignCells(): #Check trough all the cells and see if there are any mines around them
    
    for i in range(len(cells)):
        
        if cells[i]["symbol"] != "X": #If the cell is a mine, skip it
            
            num = [-9, -8, -7, -1, +1, +7, +8, +9]
            bombsNextTo = 0
        
            for j in range(len(num)):#Check all the neighbors
        
                a = num[j] #Get the number from the list
                b = i + a #Add the number to the cell number to get the surrounding cells
         
                if b >= 0 and b < 64: #Check if the cell is on the board
                    row = cells[i]["row"]
                    neighborRow = cells[b]["row"]
                    col = cells[i]["col"]
                    neighborCol = cells[b]["col"]
            
                    if neighborRow == row - 1 or neighborRow == row or neighborRow == row + 1:
                        if neighborCol == col - 1 or neighborCol == col or neighborCol == col + 1:
                            if cells[b]["symbol"] == "X":
                                bombsNextTo += 1
        
                if(bombsNextTo > 0):
                    cells[i]["symbol"] = bombsNextTo
                    
def CreateBoard():
    
    global cellNumber
    
    for row in range(boardSize):
        
        gridFrame.rowconfigure(row, weight=1, minsize=50)
        gridFrame.columnconfigure(row, weight=1, minsize=50)

        for col in range(boardSize):
            button = tk.Button(master=gridFrame, relief="raised", bg="grey", width=1, height=1)
            button.grid(row=row,column=col,padx=0,pady=0,sticky="nsew")
            button.bind("<ButtonPress-1>", lambda event, arg=cellNumber:onClick(event, arg))
            button.bind("<ButtonPress-3>", lambda event, arg=cellNumber:PlaceFlag(event, arg))
            cells[cellNumber] = ({"button":button,"row":row, "col":col, "symbol":"", "state":"enabled", "flag":False})
            cellNumber += 1
    
def Win():
    label = tk.Label(master=infoFrame, text="You Won!", font=font.Font(size=24))
    label.pack(padx=5, pady=5)
    button = tk.Button(master=infoFrame, text="Play again", font=font.Font(size=24), fg="black", width=10, relief="raised")
    button.bind("<ButtonPress-1>", RestartGame)
    button.pack(padx=5, pady=5)
    
    for i in range(len(cells)):
        cells[i]["button"].config(state="disabled")
        cells[i]["state"] = "disabled"

def GameOver():
    label = tk.Label(master=infoFrame, text="Game Over!", font=font.Font(size=24))
    label.pack(padx=5, pady=5)
    button = tk.Button(master=infoFrame, text="Play again", font=font.Font(size=18), fg="black", width=10, relief="raised")
    button.bind("<ButtonPress-1>", RestartGame)
    button.pack(padx=5, pady=5)
    
    for i in range(len(cells)):
        cells[i]["button"].config(state="disabled")
        cells[i]["state"] = "disabled"
        
        if(cells[i]["symbol"] == "X"):
            cells[i]["button"].config(text="X", font=font.Font(size=18), fg="red", bg="red", state="disabled")

def RestartGame(event):
    
    global cells
    cells = {} #Dictionary to store needed data for each cell. 0 = buttonObj, 1 = row, 2 = cell, 3 = symbol
    global cellsCleared
    cellsCleared = 0
    global cellNumber
    cellNumber = 0
    global mines
    mines = 0
    global flags
    flags = 0
    
    #Clear the grid and info button & text
    for widget in gridFrame.winfo_children():
        widget.destroy()
    
    for widget in infoFrame.winfo_children():
        widget.destroy()
    
    StartGame()

def StartGame():
    CreateBoard() #Create the game board
    CreateMines() #Generate the mines
    AssignCells() #Assign the cells with the number of mines around them
    
StartGame()  

window.mainloop()