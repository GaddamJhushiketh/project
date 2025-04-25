"""
Battleship Project
Name: G.Jhushiketh
Roll No:23AG1A67E4
"""
from tkinter import *
import random
from tkinter import messagebox

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4
GRID_SIZE = 10
SHIP_LENGTH = 3
NUM_SHIPS = 5

def makeModel(data):
    data["rows"], data["cols"] = GRID_SIZE, GRID_SIZE
    data["userBoard"] = emptyGrid(data["rows"], data["cols"])
    data["compBoard"] = emptyGrid(data["rows"], data["cols"])
    data["numShips"] = NUM_SHIPS
    data["userShips"] = []
    data["placingShips"] = True  # User is in ship placement phase
    data["compBoard"] = addShips(data["compBoard"], data["numShips"])
    data["gameOver"] = False

def makeView(data, userCanvas, compCanvas):
    drawGrid(data, userCanvas, data["userBoard"], True)
    drawGrid(data, compCanvas, data["compBoard"], False)

def emptyGrid(rows, cols):
    return [[EMPTY_UNCLICKED for _ in range(cols)] for _ in range(rows)]

def createShip(start_row, start_col, horizontal=True):
    if horizontal:
        return [[start_row, start_col + i] for i in range(SHIP_LENGTH)]
    else:
        return [[start_row + i, start_col] for i in range(SHIP_LENGTH)]

def checkShip(grid, ship):
    return all(0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and grid[r][c] == EMPTY_UNCLICKED for r, c in ship)

def addShips(grid, numShips):
    ships = 0
    while ships < numShips:
        horizontal = random.choice([True, False])
        start_row, start_col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        ship = createShip(start_row, start_col, horizontal)
        if checkShip(grid, ship):
            for r, c in ship:
                grid[r][c] = SHIP_UNCLICKED
            ships += 1
    return grid

def drawGrid(data, canvas, grid, showShips):
    cell_size = 50
    canvas.delete("all")
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == EMPTY_UNCLICKED or (grid[r][c] == SHIP_UNCLICKED and not showShips):
                color = "blue"
            elif grid[r][c] == SHIP_UNCLICKED and showShips:
                color = "green"
            elif grid[r][c] == EMPTY_CLICKED:
                color = "gray"
            elif grid[r][c] == SHIP_CLICKED:
                color = "red"
            canvas.create_rectangle(
                c * cell_size, r * cell_size, 
                (c + 1) * cell_size, (r + 1) * cell_size, 
                fill=color, outline="black"
            )

def getClickedCell(event):
    cell_size = 50
    return event.y // cell_size, event.x // cell_size

def placeShip(data, row, col):
    if len(data["userShips"]) < data["numShips"]:
        ship = createShip(row, col, horizontal=True)
        if checkShip(data["userBoard"], ship):
            for r, c in ship:
                data["userBoard"][r][c] = SHIP_UNCLICKED
            data["userShips"].append(ship)
        if len(data["userShips"]) == data["numShips"]:
            data["placingShips"] = False  # Move to gameplay phase

def updateBoard(board, row, col):
    if board[row][col] == SHIP_UNCLICKED:
        board[row][col] = SHIP_CLICKED
    elif board[row][col] == EMPTY_UNCLICKED:
        board[row][col] = EMPTY_CLICKED

def runGameTurn(data, row, col):
    if data["gameOver"] or data["placingShips"]:
        return
    updateBoard(data["compBoard"], row, col)
    if isGameOver(data["compBoard"]):
        data["gameOver"] = True
        return drawGameOver("User")
    comp_guess = getComputerGuess(data["userBoard"])
    updateBoard(data["userBoard"], *comp_guess)
    if isGameOver(data["userBoard"]):
        data["gameOver"] = True
        return drawGameOver("Computer")

def getComputerGuess(board):
    while True:
        row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if board[row][col] in (EMPTY_UNCLICKED, SHIP_UNCLICKED):
            return row, col

def isGameOver(board):
    return all(cell != SHIP_UNCLICKED for row in board for cell in row)

def drawGameOver(winner):
    messagebox.showinfo("Game Over", f"{winner} Wins!")

def mousePressed(data, event, board):
    row, col = getClickedCell(event)
    if board == "user":
        if data["placingShips"]:
            placeShip(data, row, col)
    else:
        if not data["placingShips"]:
            runGameTurn(data, row, col)
    makeView(data, userCanvas, compCanvas)  # Refresh view after action

def runSimulation(w, h):
    global userCanvas, compCanvas
    data = {}
    makeModel(data)
    root = Tk()
    root.resizable(width=False, height=False)
    Label(root, text="USER BOARD").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.pack()
    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False)
    Label(compWindow, text="COMPUTER BOARD").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.pack()
    makeView(data, userCanvas, compCanvas)
    userCanvas.bind("<Button-1>", lambda event: mousePressed(data, event, "user"))
    compCanvas.bind("<Button-1>", lambda event: mousePressed(data, event, "comp"))
    root.mainloop()

if __name__ == "__main__":
    runSimulation(500, 500)
