import random # used to build a different ship each time
import settings # gives us GRID_SIZE
from cell import Cell # the squares of the grid

def count_open_neighbors(cell): # how many cells next to this one are open
    count = 0
    for neighbor in cell.get_neighbors():
        if neighbor.is_open:
            count += 1
    return count

def get_dead_ends(): # open cells with exactly one open neighbor
    return [c for c in Cell.all if c.is_open and count_open_neighbors(c) == 1]

def generate_ship(): # carve open paths through the ship
    
    x = random.randint(1, settings.GRID_SIZE - 2)
    y = random.randint(1, settings.GRID_SIZE - 2)
    Cell.get_cell(x, y).is_open = True

    
    while True:
        candidates = [c for c in Cell.all if not c.is_open and count_open_neighbors(c) == 1]
        if not candidates: # nothing left to open, so stop
            break
        random.choice(candidates).is_open = True # open one of them at random

    
    starting_dead_ends = len(get_dead_ends()) # how many dead ends we started with
    dead_ends = get_dead_ends()
    while dead_ends and len(dead_ends) > starting_dead_ends / 2: # keep going until half are gone
        dead_end = random.choice(dead_ends) # pick a random dead end
        closed_neighbors = [n for n in dead_end.get_neighbors() if not n.is_open]
        random.choice(closed_neighbors).is_open = True # open a wall next to it
        dead_ends = get_dead_ends() # count the dead ends again
