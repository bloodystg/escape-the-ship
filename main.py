from tkinter import * # tkinter lets us make windows, buttons and labels
import random # used to make random ships
from cell import Cell # one square on the grid
from bot1 import Bot1 # the four different bots
from bot2 import Bot2
from bot3 import Bot3
from bot4 import Bot4
from ship import generate_ship # builds the walls and open paths of the ship
import settings # numbers like window size and grid size
import utilities # helpers that turn a percent into pixels


root = Tk() # make the game window
root.configure(bg="black") # make the window background black
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}') # set the size of the window
root.title (" Escape the Ship") # text shown at the top of the window
root.resizable (False, False) # stop the player from resizing the window

top_frame = Frame( # top area: holds the status text
    root,
    bg='black',
    width=1440,
    height=utilities.height_prct(25) # takes up the top 25% of the window
)
top_frame.place(x=0, y=0) # put it in the top-left corner

left_frame = Frame ( # left area: holds the bot buttons
    root,
    bg='black',
    width=utilities.width_prct(25), # 25% of the window wide
    height=utilities.height_prct(75) # the bottom 75% of the window tall
)
left_frame.place(x=0, y=utilities.height_prct(25)) # put it just under the top area


center_frame = Frame( # center area: holds the ship grid
    root,
    bg='black',
    width=utilities.width_prct(75),
    height=utilities.height_prct(75)
)
center_frame.place( # put it to the right of the left area, under the top area
    x=utilities.width_prct(25),
    y=utilities.height_prct(25),

)

for x in range (settings.GRID_SIZE): # go through every column
    for y in range (settings.GRID_SIZE): # go through every row
        c = Cell(x, y) # make a cell at this spot
        c.create_btn_object(center_frame) # give the cell a button to show it on screen
        c.cell_btn_object.grid( # line the button up in the grid
            column=x, row=y
        )

status_label = Label( # text at the top that tells you what's happening
    top_frame,
    bg='black',
    fg='white', # white text
    text='Escape the Ship!',
    font=('', 30) # big text
)
status_label.place(x=utilities.width_prct(25), y=50)


bots = {1: Bot1, 2: Bot2, 3: Bot3, 4: Bot4} # bot number -> which bot to use
bot_descriptions = { # short text shown on each bot's button
    1: 'Plans once',
    2: 'Re-plans every turn',
    3: 'Keeps away from fire',
    4: 'Predicts the fire',
}
ship_seed = 0 # same seed = same ship, same start cells and same fire, so bots can be compared fairly
bot = None # the bot that is playing right now
bot_number = None # which bot number is playing (1-4)
button_cell = None # the cell the bot needs to reach to escape
turn = 0 # how many turns have passed
next_turn = None # the scheduled next turn, so it can be cancelled


def stop_game(): # cancel the next turn of a game that's still running
    global next_turn
    if next_turn is not None: # only cancel if a turn is waiting to happen
        root.after_cancel(next_turn)
        next_turn = None

def build_ship(): # rebuild the ship from ship_seed and place the fire and button
    global button_cell
    random.seed(ship_seed) # same seed makes the same "random" ship every time
    Cell.reset_all() # clear every cell back to normal
    generate_ship() # make the walls and paths
    bot_start, button_cell = Cell.setup_game() # pick where the bot starts and where the button is
    return bot_start # send back the bot's starting cell

def new_ship(): # make a brand new random ship
    global ship_seed
    stop_game() # stop any game that's still going
    ship_seed = random.Random().randrange(1_000_000) # a fresh random seed
    build_ship()
    status_label.configure(text='New ship! Choose a bot to test')

def start_game(number): # start a game with the chosen bot
    global bot, bot_number, turn, next_turn
    stop_game() # stop any game that's still going
    bot_start = build_ship() # reset the ship so every bot gets the same start
    bot_number = number
    bot = bots[number](bot_start) # make the chosen bot at the start cell
    turn = 0
    status_label.configure(text=f'Bot {number} is trying to escape...')
    next_turn = root.after(settings.TICK_MS, game_turn) # wait a moment, then play the first turn

def game_turn(): # one turn: bot moves, then fire spreads
    global turn, next_turn
    next_turn = None
    turn += 1 # count this turn
    status_label.configure(text=f'Bot {bot_number}: turn {turn}')

    bot.move() # the bot takes one step
    if bot.cell.is_fire: # a bot that ignores fire (like Bot 1) can walk right into it
        status_label.configure(text=f'Bot {bot_number} walked into fire on turn {turn}!')
        return # game over
    if bot.cell.is_button: # the bot reached the button
        status_label.configure(text=f'Bot {bot_number} escaped in {turn} turns!')
        return # the bot wins

    Cell.spread_fire() # the fire grows
    if bot.cell.is_fire or button_cell.is_fire: # fire caught the bot or burned the button
        status_label.configure(text=f'Bot {bot_number} burned on turn {turn}!')
        return # game over

    next_turn = root.after(settings.TICK_MS, game_turn) # run the next turn later


choose_label = Label( # bot menu on the left side
    left_frame,
    bg='black',
    fg='white',
    text='Choose a bot:',
    font=('', 18)
)
choose_label.place(x=30, y=10)

for number in bots: # make one button for each bot
    bot_btn = Button(
        left_frame,
        text=f'Bot {number}: {bot_descriptions[number]}',
        width=24,
        font=('', 12),
        command=lambda n=number: start_game(n) # n=number remembers which bot this button is for
    )
    bot_btn.place(x=30, y=60 + (number - 1) * 50) # stack the buttons 50 pixels apart

new_ship_btn = Button( # button to make a new random ship
    left_frame,
    text='New ship',
    width=24,
    font=('', 12),
    command=new_ship # run new_ship() when clicked
)
new_ship_btn.place(x=30, y=290) # put it under the bot buttons

new_ship() # show a ship when the game opens

root.mainloop() # keep the window open until the player closes it
