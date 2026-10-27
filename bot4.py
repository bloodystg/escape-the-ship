import random # for imagining random fire spread
import settings # gives us FLAMMABILITY
from cell import Cell # so we can look at every cell on the ship
from pathfinding import find_path # finds the shortest way to the button

SIMULATIONS = 50 # how many possible futures of the fire to imagine each turn

class Bot4:

    def __init__(self, start_cell): # runs when the bot is made
        self.cell = start_cell # the cell the bot is standing on
        self.cell.is_bot = True # mark the bot on this cell
        self.cell.refresh() # show the bot on screen
        self.rng = random.Random() # own random numbers, so it doesn't change the real fire

    def move(self): # take one step
        plans = [] # every plan we could follow, starting with each possible first step
        for step in self.cell.get_neighbors():
            if not step.is_open or step.is_fire:
                continue # can't step into walls or fire
            for avoid in (True, False): # Bot 3's safe plan and Bot 2's short plan from there
                rest = find_path(step, avoid_near_fire=avoid)
                if rest is not None:
                    plans.append([step] + rest)
        if not plans:
            return # fire has cut off every path, stay put

        turns = max(len(p) for p in plans) # only need to imagine as far as the longest plan
        futures = [self.imagine_fire(turns) for _ in range(SIMULATIONS)]

        # the plan that survives the most futures wins; if tied, the shorter plan wins
        best = max(plans, key=lambda p: (sum(self.survives(p, f) for f in futures), -len(p)))

        self.cell.is_bot = False # leave the old cell
        self.cell.refresh() # redraw the old cell without the bot
        self.cell = best[0] # take the first step of the best plan
        self.cell.is_bot = True # stand on the new cell
        self.cell.refresh() # draw the bot on the new cell

    def imagine_fire(self, turns): # one possible future: {cell: turn it catches fire}
        fire_turn = {c: 0 for c in Cell.all if c.is_fire} # cells burning now caught fire at turn 0
        for turn in range(1, turns + 1): # play the fire forward, same rules as Cell.spread_fire
            new_fires = []
            for cell in Cell.all:
                if cell in fire_turn or not cell.is_open:
                    continue # already burning, or a wall
                burning = sum(1 for n in cell.get_neighbors() if n in fire_turn)
                if self.rng.random() < 1 - (1 - settings.FLAMMABILITY) ** burning:
                    new_fires.append(cell)
            for cell in new_fires: # light them after checking, like the real fire
                fire_turn[cell] = turn
        return fire_turn

    def survives(self, plan, fire_turn): # True if the bot makes it in this imagined future
        for turn, cell in enumerate(plan, start=1): # the bot reaches plan[0] on turn 1, and so on
            catches = fire_turn.get(cell, float('inf')) # when this cell catches fire (never = infinity)
            if cell.is_button:
                return catches >= turn # just has to arrive before the fire spreads that turn
            if catches <= turn: # the fire reaches the bot's cell
                return False
        return True
