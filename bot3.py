from pathfinding import find_path # finds the shortest way to the button

class Bot3:
    
    def __init__(self, start_cell): # runs when the bot is made
        self.cell = start_cell # the cell the bot is standing on
        self.cell.is_bot = True # mark the bot on this cell
        self.cell.refresh() # show the bot on screen

    def move(self): # take one step
        plan = find_path(self.cell, avoid_near_fire=True) # the safer plan
        if not plan:
            plan = find_path(self.cell) # backup plan: only avoid the fire itself
        if not plan:
            return # fire has cut off every path, stay put

        self.cell.is_bot = False # leave the old cell
        self.cell.refresh() # redraw the old cell without the bot
        self.cell = plan[0] # take the first step of the new plan
        self.cell.is_bot = True # stand on the new cell
        self.cell.refresh() # draw the bot on the new cell
