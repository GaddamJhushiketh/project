"""
Battleship Project
Name: G.Jhushiketh
Roll No:23AG1A67E4
"""

import battleship_test as test


project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###



from tkinter import *
import random

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4

'''
makeModel(data)
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):
    data["rows"], data["cols"] = GRID_SIZE, GRID_SIZE
    data["userBoard"] = emptyGrid(data["rows"], data["cols"])
    data["compBoard"] = emptyGrid(data["rows"], data["cols"])
    data["numShips"] = NUM_SHIPS
    data["userShips"] = []
    data["placingShips"] = True  # User is in ship placement phase
    data["compBoard"] = addShips(data["compBoard"], data["numShips"])
    data["gameOver"] = False
    # Initialize game data like rows, columns, boards, ships, and other parameters.
    pass

'''
makeView(data, userCanvas, compCanvas)
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    drawGrid(data, userCanvas, data["userBoard"], True)  # User's ships are visible
    drawGrid(data, compCanvas, data["compBoard"], False) # Computer's ships are hidden


    # Render both user and computer grids along with any temporary or final states.
    pass

'''
keyPressed(data, event)
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    if event.keysym == "r":
        makeModel(data)
    # Handle key events to restart the game or perform specific actions.
    pass

'''
mousePressed(data, event, board)
Parameters: dict mapping strs to values ; mouse event object ; 2D list of ints
Returns: None
'''
def mousePressed(data, event, board):
    row, col = getClickedCell(data, event)
    if board == "user":
        clickUserBoard(data, row, col)
    else:
        runGameTurn(data, row, col, "user")
    # Handle mouse events for ship placement or gameplay interactions.
    pass

'''

### STAGE 1 ###

emptyGrid(rows, cols)
Parameters: int ; int
Returns: 2D list of ints
'''
def emptyGrid(rows, cols):
    return [[EMPTY_UNCLICKED for _ in range(cols)] for _ in range(rows)]

    pass

'''
createShip()
Parameters: no parameters
Returns: 2D list of ints
'''
def createShip():
    while True:
        orientation = random.choice(["H", "V"])
        start_row, start_col = random.randint(0, 9), random.randint(0, 9)
        if orientation == "H" and start_col + 2 < 10:
            return [[start_row, start_col + i] for i in range(3)]
        elif orientation == "V" and start_row + 2 < 10:
            return [[start_row + i, start_col] for i in range(3)]

'''
checkShip(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):
    return all(0 <= r < 10 and 0 <= c < 10 and grid[r][c] == EMPTY_UNCLICKED for r, c in ship)
    # Validate whether the ship placement overlaps with existing ships.
    pass

'''
addShips(grid, numShips)
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShips):
    ships = 0
    while ships < numShips:
        ship = createShip()
        if checkShip(grid, ship):
            for r, c in ship:
                grid[r][c] = SHIP_UNCLICKED
            ships += 1
    return grid
    # Randomly add the specified number of ships to the grid.
    pass

'''
drawGrid(data, canvas, grid, showShips)
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''
def drawGrid(data, canvas, grid, showShips):
    cell_size = 50
    for r in range(data["rows"]):
        for c in range(data["cols"]):
            color = "blue" if grid[r][c] == EMPTY_UNCLICKED else "gray"
            if grid[r][c] == SHIP_UNCLICKED and showShips:
                color = "green"
            elif grid[r][c] == EMPTY_CLICKED:
                color = "white"
            elif grid[r][c] == SHIP_CLICKED:
                color = "red"
            canvas.create_rectangle(c * cell_size, r * cell_size, (c + 1) * cell_size, (r + 1) * cell_size, fill=color)
    # Render the grid on the canvas, showing or hiding ship placements based on the flag.
    pass

'''
### STAGE 2 ###



isVertical(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship):
    return all(ship[i][1] == ship[i + 1][1] for i in range(len(ship) - 1))

    # Check if the ship cells are vertically aligned.
    pass

'''
isHorizontal(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):
    return all(ship[i][0] == ship[i + 1][0] for i in range(len(ship) - 1))

    # Check if the ship cells are horizontally aligned.
    pass

'''
getClickedCell(data, event)
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
def getClickedCell(data, event):
    cell_size = 50
    return [event.y // cell_size, event.x // cell_size]
    # Determine the cell clicked based on the event coordinates.
    pass

'''
drawShip(data, canvas, ship)
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    cell_size = 50
    for r, c in ship:
        canvas.create_rectangle(
            c * cell_size, r * cell_size, 
            (c + 1) * cell_size, (r + 1) * cell_size, 
            fill="green"
        )
    # Visualize a temporary or placed ship on the grid.
    pass

'''
shipIsValid(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
    return len(ship) == 3 and (isVertical(ship) or isHorizontal(ship)) and checkShip(grid, ship)
    # Ensure the ship is valid in terms of placement rules and alignment.
    pass

'''
placeShip(data)
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    if len(data["userShips"]) < data["numShips"]:
        ship = createShip()
        if shipIsValid(data["userBoard"], ship):
            for r, c in ship:
                data["userBoard"][r][c] = SHIP_UNCLICKED
            data["userShips"].append(ship)
    # Place a ship on the user board if it meets validity criteria.
    pass

'''
clickUserBoard(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
    placeShip(data)
    # Manage user interaction for ship placement.
    pass



### STAGE 3 ###

'''
updateBoard(data, board, row, col, player)
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
    if board[row][col] == SHIP_UNCLICKED:
        board[row][col] = SHIP_CLICKED
    elif board[row][col] == EMPTY_UNCLICKED:
        board[row][col] = EMPTY_CLICKED
    # Update the board state after a user's or computer's turn.
    pass

'''
runGameTurn(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col, player):
    if player == "user":
        updateBoard(data, data["compBoard"], row, col, "user")
        if isGameOver(data["compBoard"]):
            drawGameOver(data, userCanvas)
            return
        comp_guess = getComputerGuess(data["userBoard"])
        updateBoard(data, data["userBoard"], comp_guess[0], comp_guess[1], "comp")
        if isGameOver(data["userBoard"]):
            drawGameOver(data, userCanvas)
    
    updateView(data, userCanvas, compCanvas)
    # Execute a single turn for the user and the computer.
    pass

'''
getComputerGuess(board)
Parameters: 2D list of ints
Returns: list of ints
'''
def getComputerGuess(board):
    while True:
        row, col = random.randint(0, 9), random.randint(0, 9)
        if board[row][col] in (EMPTY_UNCLICKED, SHIP_UNCLICKED):
            return [row, col]
    # Generate a random valid guess for the computer's turn.
    pass

'''
isGameOver(board)
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    for row in board:
        if SHIP_UNCLICKED in row:
            return False  # Game continues if any ship remains
    return True  # Game over if no ships remain


    # Check if all ships on the board have been sunk.
    pass

'''
drawGameOver(data, canvas)
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
    canvas.delete(ALL)  # Clear the board
    canvas.create_text(
        250, 250,  # Center of the canvas
        text="You Win!" if isGameOver(data["compBoard"]) else "Computer Wins!",
        font=("Arial", 24, "bold"),
        fill="red"
    )
    # Display the game-over message based on the winner.
    pass

### SIMULATION FRAMEWORK ###

from tkinter import *

def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()

def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)

def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)

def runSimulation(w, h):
    data = { }
    makeModel(data)

    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window

    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()

    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()

    makeView(data, userCanvas, compCanvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))

    updateView(data, userCanvas, compCanvas)

    root.mainloop()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":

    # print("\n" + "#"*15 + " STAGE 1 TESTS " +  "#" * 16 + "\n")
    # test.stage1Tests()
    # test.testEmptyGrid()
    # test.testCreateShip()
    # test.testCheckShip()
    # test.testAddShips()
    # test.testGrid()


    ## Uncomment these for STAGE 2 ##

    # print("\n" + "#"*15 + " STAGE 2 TESTS " +  "#" * 16 + "\n")
    # test.stage2Tests()
    # test.testIsVertical()
    # test.testIsHorizontal()

    # test.testGetClickedCell()
    # test.testShipIsValid()
    

    ## Uncomment these for STAGE 3 ##
    
    # print("\n" + "#"*15 + " STAGE 3 TESTS " +  "#" * 16 + "\n")
    # test.stage3Tests()
    # test.testUpdateBoard()
    # test.testGetComputerGuess()
    # test.testIsGameOver()
    # test.testDrawGameOver()
    

    ## Finally, run the simulation to test it manually ##
    runSimulation(500, 500)
