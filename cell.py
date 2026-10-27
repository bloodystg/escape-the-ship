from tkinter import Button # each cell is shown as a button
import random # used to pick random cells and spread fire randomly
import settings # gives us FLAMMABILITY

class Cell: # one square on the ship's grid
    all = [] # a list of every cell that has been made
    grid = {} # (x, y) -> cell, for finding a cell instantly

    def __init__(self, x, y): # runs when a new cell is made
        self.x = x # which column the cell is in
        self.y = y # which row the cell is in
        self.is_open = False # every cell starts blocked
        self.is_fire = False # True if this cell is burning
        self.is_button = False # True if this is the exit button
        self.is_bot = False # True if the bot is standing here
        self.cell_btn_object = None # the button on screen (made later)
        Cell.all.append(self) # add this cell to the list of all cells
        Cell.grid[(x, y)] = self # remember where this cell is

    def create_btn_object(self, location): # make the button that shows this cell
        btn = Button(
            location, # which frame the button goes in
            width=6,
            height=2
        )

        btn.bind('<Button-1>', self.left_click_actions ) # run left_click_actions when left-clicked
        self.cell_btn_object = btn # save the button so we can change it later

    def left_click_actions(self, event): # what happens when you click a cell
        print(f"Clicked cell ({self.x}, {self.y})") # print where you clicked (for testing)

    def refresh(self): # update the color/text to match what's in this cell
        if not self.is_open: # blocked cell = black
            self.cell_btn_object.configure(bg='black', text='')
        elif self.is_bot: # bot = blue
            self.cell_btn_object.configure(bg='blue', fg='white', text='BOT')
        elif self.is_fire: # fire = red
            self.cell_btn_object.configure(bg='red', fg='white', text='FIRE')
        elif self.is_button: # exit button = green
            self.cell_btn_object.configure(bg='green', fg='white', text='EXIT')
        else: # empty open cell = gray
            self.cell_btn_object.configure(bg='gray', text='')

    def get_neighbors(self): # the cells up, down, left and right of this one
        neighbors = [
            Cell.get_cell(self.x - 1, self.y), # left
            Cell.get_cell(self.x + 1, self.y), # right
            Cell.get_cell(self.x, self.y - 1), # up
            Cell.get_cell(self.x, self.y + 1), # down
        ]
        return [c for c in neighbors if c is not None] # leave out spots that are off the grid

    @staticmethod
    def get_cell(x, y): # find the cell at (x, y)
        return Cell.grid.get((x, y)) # None if (x, y) is off the grid

    @staticmethod
    def reset_all(): # make every cell blocked and empty again, ready for a new game
        for cell in Cell.all:
            cell.is_open = False
            cell.is_fire = False
            cell.is_button = False
            cell.is_bot = False

    @staticmethod
    def setup_game(): # pick 3 different random open cells for fire, button and bot
        open_cells = [c for c in Cell.all if c.is_open] # only open cells can be picked
        fire_cell, button_cell, bot_cell = random.sample(open_cells, 3) # pick 3 different cells
        fire_cell.is_fire = True # start the fire
        button_cell.is_button = True # place the exit button
        for cell in Cell.all: # redraw every cell so the screen matches
            cell.refresh()
        return bot_cell, button_cell # send back where the bot starts and where the button is

    @staticmethod
    def spread_fire(): # let the fire grow by one turn
        new_fires = [] # cells that will catch fire this turn
        for cell in Cell.all:
            if cell.is_fire or not cell.is_open: # blocked cells can't burn
                continue # skip it
            burning = 0 # how many neighbors are on fire
            for neighbor in cell.get_neighbors():
                if neighbor.is_fire:
                    burning += 1
            # more burning neighbors = higher chance to catch fire
            chance = 1 - (1 - settings.FLAMMABILITY) ** burning
            if random.random() < chance: # roll the dice
                new_fires.append(cell)

        for cell in new_fires: # light them after checking, so fire moves 1 step per turn
            cell.is_fire = True
            cell.refresh() # turn the cell red on screen

    def __repr__(self): # how a cell looks when printed, e.g. Cell(2, 3)
        return f"Cell({self.x}, {self.y})"
