import tkinter as tk
from tkinter import font

#Set up the window
window = tk.Tk()
window.title("Tic-Tac-Toe")
window.geometry("400x500") #Set the size of the window

playerTurn = 0
cells = {}

menuFrame = tk.Frame(master=window, bg="black")
menuFrame.pack()
turnLabel = tk.Label(master=menuFrame, text="Click a square to begin", font=font.Font(size=24), fg="black", width=20, height=2)
turnLabel.pack()

gridFrame = tk.Frame(master=window)
gridFrame.pack()

buttonFrame = tk.Frame(master=window)
buttonFrame.pack()

#Handle player clicking a square
def Move(event, btnNum):
    
    buttonePressed = event.widget #Get the button that was pressed
    
    #Acces the global variables
    global playerTurn 
    global cells 
    
    #Check if the square has already been played
    if cells[btnNum] == "X" or cells[btnNum] == "O":
        return
        
    if playerTurn % 2 == 0:
        buttonePressed.config(text="X", bg="lightgreen", state="disabled")
        turnLabel.config(text="Player O turn!")
        cells[btnNum] = ("X")
        
    else:
        buttonePressed.config(text="O", bg="lightblue", state="disabled")
        turnLabel.config(text="Player X turn!")
        cells[btnNum] = ("O")
    
    winningMove = CheckWinner()
    
    #Check if there is a winner
    if winningMove == True:
        EndGame(playerTurn, winningMove)
    
    #Check if the game is tied
    if playerTurn >= 8:
        EndGame(playerTurn, winningMove)
    
    #Move to next players turn
    playerTurn += 1

def CheckWinner():
    
    if cells[0] == cells[1] == cells[2] \
        or cells[3] == cells[4] == cells[5] \
        or cells[6] == cells[7] == cells[8]:
        return True
    elif cells[0] == cells[3] == cells[6] \
        or cells[1] == cells[4] == cells[7] \
        or cells[2] == cells[5] == cells[8]:
        return True
    elif cells[0] == cells[4] == cells[8] \
        or cells[2] == cells[4] == cells[6]:
        return True
    else: return False

def EndGame(turn, win):
    
    if win == True:
        if turn % 2 == 0:
            turnLabel.config(text="Player X wins!")
        else: turnLabel.config(text="Player O wins!")
    elif turn >= 8:
        turnLabel.config(text="Stalemate!")
    
    #Disable all buttons
    for widget in gridFrame.winfo_children():
        widget.configure(state="disabled")
        widget.bind("<ButtonPress-1>", lambda event: None)
    
    #Create a button to restart the game
    restartButton = tk.Button(master=buttonFrame, text="Play again", font=font.Font(size=24), fg="black", width=10, relief="raised")
    restartButton.pack(padx=5, pady=5)
    restartButton.bind("<ButtonPress-1>", RestartGame) #Bind the button to a function that re-sets the game.

def RestartGame(event):
    
    global playerTurn
    global cells
    
    playerTurn = 0 #Reset the player turn
    cells = {} #Empty the cells dictionary
    
    for widget in gridFrame.winfo_children():
        widget.destroy()
    
    for widget in buttonFrame.winfo_children():
        widget.destroy()
    
    turnLabel.config(text="Click a square to begin")
    
    #Create game board again
    GameBoard()

#Create the game grid
def GameBoard():

    global cells
    btnNum = 0
    
    for row in range(3):
        
        gridFrame.rowconfigure(row, weight=1, minsize=50)
        gridFrame.columnconfigure(row, weight=1, minsize=100)

        for col in range(3):
            button = tk.Button(master=gridFrame, font=font.Font(size=36, weight="bold"), bg="grey", width=1, height=1)
            button.grid(row=row,column=col,padx=5,pady=5,sticky="nsew")
            button.bind("<ButtonPress-1>", lambda event, arg=btnNum:Move(event, arg))
            cells.update({btnNum:btnNum})
            btnNum += 1
            
    #Actually display the window
    window.mainloop()

#Create the game board
GameBoard()