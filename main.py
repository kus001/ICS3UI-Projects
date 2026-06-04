import os
import time
import random
import re # got help (used for coloured characters)
from grid import make_grid

"""Please don't start this until you have:
    * submitted Exercises 2.1 to 2.8
    * completed the Planning for Human vs. Bot
    * reviewed the Ethical Computer Use assignment
"""

# Do not modify the code below since it's needed to run the autograder accurately

quit_now = input("Enter 'quit' to quit or anything else to begin: ")
if quit_now.lower().strip() == "quit":
    exit(0)

# Start your code here
# clear console function
def clear_console():  # got help
    os.system('cls' if os.name == 'nt' else 'clear')
# quit check 
def quit_check(user_input):
    if user_input.strip().lower() == 'quit':
        print("Thanks for playing!")
        exit()
        
# starting instructions
logo = """ __   __  ___       __        _______   
|"  |/  \\|  "|     /""\\      /"      \\  
|'  /    \\:  |    /    \\    |:        | 
|: /'        |   /' /\\  \\   |_____/   ) 
 \\//  /\\'    |  //  __'  \\   //      /  
 /   /   \\   | /   /  \\  \\ |:  __   \\  
|___/    \\___|(___/    \\___)|__|  \\___) 

=== ⚔️ WAR INSTRUCTIONS ⚔️  ===

🏠 Place your base (✪ ). It cannot be moved once placed.  
🪖 Deploy your soldiers (⊙). You have 2 soldiers to place.  

➡️ Each turn, move **one soldier** to an adjacent square (up/down/left/right).  
💥 Move onto an enemy soldier (⊙) to kill them.  
💥 Move onto the enemy base (⦷ ) to destroy it and **win instantly**.  

🟢 Your soldier's are GREEN.
🔴 Bot's soldier's are RED.

‼️ Do not have the same coordinates for any of your soldiers and the base. ‼️

🛡️ Enemy soldiers and base act after you each turn.  
🏁 If your base is destroyed, you lose.  
⏳ Game lasts a max of 20 turns. Tie if both bases survive.  

*Type "quit" anywhere to quit the game!*

💡 Tip: Use your coordinates wisely and try to trap enemy soldiers!

=============================
"""
print(logo)
start_prompt = input("Enter 'q' to quit or anything else to begin: ").lower()
if start_prompt == "q":
    quit()
else:
    print("Alright, let's begin!")
    time.sleep(0.5)
    clear_console()
# bot logic
class Bot:
    def __init__(self, rows, cols, grid):
        self.rows = rows
        self.cols = cols
        self.grid = grid
        self.base_coords = None
        self.soldier_coords = []
    # bot's base coordinates
    def bot_base(self):
        while True:
            bot_base_x = random.randint(0, self.cols - 1) # choose x-coord for bot
            bot_base_y = random.randint(0, self.rows - 1) # choose y-coord for bot
            if (bot_base_x, bot_base_y) != player.base_coords and (bot_base_x, bot_base_y) not in player.soldier_coords:
                self.grid[bot_base_y][bot_base_x] = '⦷'# add the bot coordinate to the grid
                self.base_coords = (bot_base_x, bot_base_y)
                break
        return bot_base_x, bot_base_y, grid
    # bot's soldier coordinates
    def bot_soldiers(self, num_soldiers=2):
        while len(self.soldier_coords) < num_soldiers: # until the number of bots has NOT been initiated
            x = random.randint(0, self.cols - 1)
            y = random.randint(0, self.rows - 1)
            if ( 
                (x,y) not in self.soldier_coords
                and (x,y) != self.base_coords
                and (x,y) != player.base_coords
                and (x,y) not in player.soldier_coords): # got help (if bot_soldier's coords are not on the base or already initiated)
                self.soldier_coords.append((x,y))
                self.grid[y][x] = '\033[31m⊙\033[0m'
    def bot_move(self):
        if not self.soldier_coords: # got help, the soldier_index went out of range at times
            return
        soldier_index = random.randint(0, len(self.soldier_coords) - 1) # choose which soldier to move
        x, y = self.soldier_coords[soldier_index]

        # targets to eliminate
        targets = player.soldier_coords + [player.base_coords]

        # find the nearest target using Manhattan Distance (got help)
        nearest_target = min(targets, key=lambda t: abs(t[0]-x) + abs(t[1]-y))
        tx, ty = nearest_target

        # decide which direction move (got help)
        if x < tx: # close in x-axis
            new_x = x + 1
        elif x > tx:
            new_x = x - 1
        else:
            new_x = x

        if y < ty: # close in y-axis
            new_y = y + 1
        elif y > ty:
            new_y = y - 1
        else:
            new_y = y

        # bot lands on player's soldier
        if (new_x, new_y) in player.soldier_coords:
            player.soldier_coords.remove((new_x, new_y))
            player.grid[new_y][new_x] = '.' # fixed slight error
            print("Bot killed one of your soldiers!")
        # bot lands on player base
        if (new_x, new_y) == player.base_coords:
            clear_console()
            print("You lost! Bot destroyed your base.")
            exit()
        
        # move bot
        self.grid[y][x] = '.'
        self.grid[new_y][new_x] = '\033[31m⊙\033[0m'
        self.soldier_coords[soldier_index] = (new_x, new_y) # fixed slight formatting error
    
class Player:
    def __init__(self, rows, cols, grid):
        self.rows = rows
        self.cols = cols
        self.grid = grid
        self.base_coords = None
        self.soldier_coords = []
        self.symbols = ['\033[32m①\033[0m', '\033[32m②\033[0m'] # used to make the symbols of the soldiers numbered (easier to understand)
    def player_base(self):
        while True:
            player_base = input("Enter the coordinate for your base seperated by commas: ")
            quit_check(player_base)
                      
            if "," not in player_base: # invalid format
                print("Invalid format. Use x, y.")
                continue
            try:
                base_coord_list = [int(x.strip()) for x in player_base.split(',')] # split input into a list
            except ValueError:
                print("Invalid value(s). Try again.")
                continue
            if len(base_coord_list) != 2: # invalid format (2+ numbers)
                print("Invalid format. Enter only 2 numbers")
                continue

            base_coord = tuple(base_coord_list) # convert the input_list into a tuple
            x, y = base_coord # unpack the coordinates
            if 0 <= x < self.cols and 0 <= y < self.rows: # error detection (can't exceed grid size)
                self.grid[y][x] = '✪' # add player base to grid
                self.base_coords = (x, y) # save player base coords
                break
            else: # player base coords exceed the grid (ERROR)
                print("Invalid coordinates. Try again.")
                time.sleep(0.5)
    def player_soldier(self, num_player_soldiers=2):
        while len(self.soldier_coords) < num_player_soldiers: # until the number of bots has NOT been initiated
            player_soldier = input("Enter the coordinate for your soldier seperated by commas: ")
            quit_check(player_soldier) 
            
            if "," not in player_soldier: # invalid format
                print("Invalid format. Use x, y.")
                continue
            try: # handles input errors
                player_soldier_list = [int(x.strip()) for x in player_soldier.split(',')]
            except ValueError:
                print("Invalid value(s). Try again.")
                continue
                
            if len(player_soldier_list) != 2: # invalid format (2+ numbers)
                print("Invalid format. Enter only 2 numbers")
                continue
        
            player_soldier_coord = tuple(player_soldier_list)
            x, y = player_soldier_coord
            if 0 <= x < self.cols and 0 <= y < self.rows:
                self.grid[y][x] = self.symbols[len(self.soldier_coords)] # got help for the indexing 
                self.soldier_coords.append((x,y)) # got help (adds the soldier coordinates to the lift)
            else: # soldier coordinates exceed the grid (ERROR)
                print("Invalid ccoordinates. Try again.")
                time.sleep(0.5)
                
    def player_move(self):
        print("Soldier Coordinates:", ", ".join(str(coord) for coord in self.soldier_coords)) # got help (helps the user choose what soldier to move)
        while True: # error detection (check for valid index)
            try:
                ask_soldier_index = input("What soldier do you want to move (1 or 2): ")
                quit_check(ask_soldier_index)
            
            except ValueError:
                print("Invalid input. Enter a proper value.")
                continue
                
            soldier_index = None

            if int(ask_soldier_index) == 1:
                soldier_index = 0
                break
            elif int(ask_soldier_index) == 2:
                soldier_index = 1
                break
            else:
                print("Invalid coordinate. Try again.")
        x, y = self.soldier_coords[soldier_index]

        while True:
            new_soldier_coord = input("Enter the new coordinate for your soldier seperated by commas: ")
            quit_check(new_soldier_coord)
            
            try: 
                new_soldier_coord_list = [int(x.strip()) for x in new_soldier_coord.split(',')]
                new_x, new_y = new_soldier_coord_list
            except ValueError:
                print("Invalid input. Enter a proper value.")
                continue
            
            if (abs(new_x - x) == 1 and new_y == y) or (abs(new_y - y) == 1 and new_x == x): # got help (checks for the absolute value of the new position change)
                # valid input (only moved one spot)
                self.grid[y][x] = '.' # replace the old coordinate with a blank symbol
                self.grid[new_y][new_x] =  self.symbols[soldier_index] # add the soldier symbol to the new position  # got help with indexing
                self.soldier_coords[soldier_index] = (new_x, new_y)
                break # valid coordinates auquired
            else:
                print("Invalid coordinate. You can only move one spot.")

        # player kills bot
        if (new_x, new_y) in bot.soldier_coords:
            bot.soldier_coords.remove((new_x, new_y))
            print("You killed bot soldier!")
        # player kills bot base
        if (new_x, new_y) == bot.base_coords:
            clear_console()
            print("You win! You destroyed the enermy base.")
            exit()

def strip_ansi(text): # got help from AI (entire function)
    """Removes ANSI color codes so spacing works properly."""
    return re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', text) # regex prompt 

def show_grid(grid):
     # grid coordinates
      header = [" "] + [str(col).ljust(4) for col in range(cols)] # got help with the (ljust(2)) part; which makes sure no shifting happens
      print("  ".join(header))

      for i, row in enumerate(grid): # keeps the numberings of the grid while saving data, w/enumerate() (got help)
          visible_cells = [c + " " * (4 - len(strip_ansi(c))) for c in row] # got help
          row_header = f"{i:2} " + "  ".join(visible_cells) # got help for the .join() part (makes sure no shifting happens)
          print(row_header)
          print()
        
# achievements (make them turn-based, if the player does something within a number of turns, give them an achievement. Make it so that if the user gets an achievement, they gain access to an ability that allows them to take 2 turns back to back one time.)

# global variable(s)
grid, rows, cols = make_grid() # got help (need to unpack the values from grid.py module to use)
player = Player(rows, cols, grid)
bot = Bot(rows, cols, grid)
# player presets
player.player_base()
show_grid(grid)
clear_console()
show_grid(grid)
player.player_soldier()
show_grid(grid)
clear_console()
show_grid(grid)

# bot presets
clear_console()
bot.bot_base()
show_grid(grid)
clear_console()
bot.bot_soldiers()
show_grid(grid)

# turns
turns = 0
max_turns = 20

while turns < max_turns:
    clear_console()
    print(f"Turns: {turns}")
    print()
    show_grid(grid)

    # player turn
    print("Player's turn")
    player.player_move()
    # check if player destroyed enemy base
    if bot.base_coords in player.soldier_coords:
        clear_console()
        print("You win!")
        break

    # bot turn
    print("Bot's turn")
    bot.bot_move()
    # check if bot destroyed enemy base
    if len(player.soldier_coords) == 0:
        print("You lost! Bot killed all your soldiers!")
        break

    if turns == max_turns:
        clear_console()
        print("Tie!")
        exit()
    
    turns += 1
    time.sleep(0.4)

else: # tie game
    clear_console()
    print("Tie, no one wins.")