# Use the "Import Code From Assignment" feature under the More tab
# to transfer your Beta Version into here
import os
import time
import random
# from re import L
# global money

"""Please don't start this until you have:
    * submitted Exercises 1.1 to 1.8
    * completed the Planning for Solo Game
    * reviewed the Ethical Computer Use assignment
"""

# Do not modify the code below since it's needed to run the autograder accurately

quit_now = input("Enter 'quit' to quit or anything else to begin: ")

if quit_now.lower().strip() == "quit":
    exit(0)

# Start your code here

# clear console function
def clear_console(): # got help
    os.system('cls' if os.name == 'nt' else 'clear')  # clear the console, resulting in a neater playing environment

# welcome variables
username = input("Enter your username: ")
welcome_instructons = """ 
====================================================
            ___ _____ ___   ___ _  _____ 
           / __|_   _/ _ \\ / __| |/ / __|
           \\__ \\ | || (_) | (__| ' <\\__ \\
           |___/ |_| \\___/ \\___|_|\\_\\___/
        

            W E L C O M E   T O   T H E
    S T O C K   M A R K E T   S I M U L A T O R    
====================================================

📈 HOW TO PLAY:
- You start with $1000 in cash.
- Each day, stock prices will change randomly.
- On your turn, you can:
    • BUY shares of a company (if you have enough cash).
    • SELL shares you own (to take profit or cut losses).
    • skip to the next day.
- Random events may occur: booms, crashes, or market news.

🎯 GOAL:
Grow your wealth and finish with the highest net worth possible!
Can you beat the market and become a stock market legend; or will you lose everything?

====================================================
""" # AI was used to format the appearance of the introduction.
print(welcome_instructons)
ask_to_start = input(f"{username}, type any key to start or 'q' to quit. ").lower()
if ask_to_start == 'n': # user does not want to play
    print(f"Thank you {username} for playing!")
    time.sleep(2)
    clear_console() 
    exit(0) 
else: # user wants to play
    print(f"Great, let's begin {username}!")
    time.sleep(2)
    clear_console()

# IMP variables
day = 1 # current day
random_event_day = random.randint(0, 50) # if the actual day = random
money = 1000 # the money in the bank
portfolio = {}
market = { # market
    "APPL": 180,
    "TSLA": 250,
    "MSFT": 330,
    "AMZN": 140,
    "NVDA": 450,
    "KO": 60,
    "META": 300
}

# achievements/game endings
# achievement storage
achievements = []
achievement_count = 0

def show_achievements():
    global achievement_count # got help
    
    if money <= 0 and "📉 Dead Broke 📉" not in achievements: # cannot trade anymore
        print("""
        🏆 ACHIEVEMENT UNLOCKED 🏆
        ━━━━━━━━━━━━━━━━━━━━━━━━━━
        📉 Dead Broke 📉 
        You are now bankrupt!
        ━━━━━━━━━━━━━━━━━━━━━━━━━━
        """)
        print("Thank you for playing, be better with your money next time.")
        achievements.append("📉 Dead Broke 📉")
        achievement_count += 1
        time.sleep(1.2)
        exit()
    elif money > 1000 and "📈 Wall Street Rookie 📈" not in achievements: # made more money than you started with
        print("""
        🏆 ACHIEVEMENT UNLOCKED 🏆
        ━━━━━━━━━━━━━━━━━━━━━━━━━━
        📈 Wall Street Rookie 📈 
        You made more money than you started with!
        ━━━━━━━━━━━━━━━━━━━━━━━━━━
        """)
        achievements.append("📈 Wall Street Rookie 📈")
        achievement_count += 1
        time.sleep(1.2)
        clear_console()
    elif money > 2000 and "📈 Double Up 📈" not in achievements: # doubled the money you started with
        print("""
        🏆 ACHIEVEMENT UNLOCKED 🏆
        ━━━━━━━━━━━━━━━━━━━━━━━━━━
        📈 Double Up 📈 
        You doubled the money you started with!
        ━━━━━━━━━━━━━━━━━━━━━━━━━━
        """)
        achievements.append("📈 Double Up 📈")
        achievement_count += 1
        time.sleep(1.2)
        clear_console()
        
# functions

# show current market
def show_market(): # insert main input variable
    for stock, price in market.items():
        print(f"{stock}: ${price}")
    
        
# show portfolio
def show_portfolio():
    if not portfolio: # got help
        print("You don't own stocks.")
    else:
        total_value = 0 # got help
        for stock, shares in portfolio.items(): # got help for this for loop
            stock_value = shares * market[stock]
            total_value += stock_value
            print(f"{stock}: {shares} shares | Price: ${market[stock]} | Value: ${stock_value}")
        print(f"Portfolio Net Worth: ${total_value}")
    print()
    
# updated prices (daily)
def update_prices(): # insert main input variable
    for stock, price in market.items():
        new_price = price * (1 + random.uniform(-0.10, 0.175)) # ± stock value change daily 
        market[stock] = round(new_price)
        
# control manual
def controls(): # lists the appropriate prompts the user can enter
    control = """
=== STOCK SIMULATOR CONTROLS ===
    day     → Advance to the next day (prices update)
    show    → Show your portfolio (stocks + money)
    buy     → Buy shares of a stock
    sell    → Sell shares of a stock
    quit    → Exit the simulator
    clear   → Clear the console
    achieve → Show achievements
    ================================
    """
    print(control)
    exit_controls = input('Press any key to exit controls: ')
    if exit_controls:
        clear_console()
    
# buy stock
def buy_stock(): # buy stocks (got help)
    choose_stock_buy = input("What stock do you want to buy: ").upper()
    
    if choose_stock_buy in market:
        shares = input(f"How many shares of {choose_stock_buy} do you want to buy? ")
        if shares.isdigit():
            shares = int(shares)
            cost = market[choose_stock_buy] * shares
            global money # set money to be usable globally (got help)
            if cost <= money:
                money -= cost
                portfolio[choose_stock_buy] = portfolio.get(choose_stock_buy, 0) + shares # if the stock is already present, the price is added on top of it (got help)
                print(f"✅ Bought {shares} shares of {choose_stock_buy} for ${cost}!")
                print(f"💰 Money left: ${money}")
            else:
                print("❌ not enough money!")
        else:
            print("❌ Invalid input. Try again. ")
            return
    else:
        print("❌ Invalid stock name. Try again.")
            
# sell stock
def sell_stock():
    choose_stock_sell = input("What stock do you want to sell: ").upper()

    if choose_stock_sell in portfolio:
        shares = input(f"How many shares of {choose_stock_sell} do you want to sell? ")
        if shares.isdigit():
            shares = int(shares)
            repay = market[choose_stock_sell] * shares # the money from selling stock
            if shares > portfolio[choose_stock_sell]:
                print("❌ You don't own that many shares!")
                return
            
            global money
            money += repay # add the money back to your account
            portfolio[choose_stock_sell] -= shares 
            
            # if shares drop to 0, remove stock from portfolio
            if portfolio[choose_stock_sell] <= 0:
                del portfolio[choose_stock_sell]
            
            print(f"✅ Sold {shares} shares of {choose_stock_sell} for ${repay}!")
            print(f"💰 Money left: ${money}")
        else:
            print("❌ Invalid input. Try again. ")
            return
    else:
            print("❌ You don't own that stock.")

        
# random event functions 
# every certain number of days, a random function is executed
def prices_spike():
    price_spike_prompts = [
        "Wow, the companies launched new products! Stocks have gone up.",
        "The government gave the companies some funds! Stocks have gone up.",
        "Shocker, the companies have had great earnings! Stocks have gone up."
    ]
    
    for stock, price in market.items():
        new_price = price * (1 + random.uniform(0.25, 0.40)) # 25-40% stock value increase
        market[stock] = round(new_price) # stocks have a huge surplus

    print(random.choice(price_spike_prompts)) 

def prices_crash(): 
    price_crash_prompts = [
        "Oh no, the companies have had VERY subpar earnings. Stocks have started to crash.",
        "The government has placed HEAVY regulation on the companies. Stocks have started to crash.",
        "Oh no! The companies are tangled up in scandals. Stocks have started to crash."
    ]
    
    for stock, price in market.items():
        new_price = price * (1 + random.uniform(-0.4, -0.25)) # -25--40% stock value change daily 
        market[stock] = round(new_price) # stocks have a huge crash

    print(random.choice(price_crash_prompts))
    
# call the functions
while True:
    # preset visual elements
    print("Market: ")
    show_market()
    print()
    print("Your Portfolio: ")
    show_portfolio()
    print(f"Bank: ${money} | Day: {day} | Achievements: {achievement_count}")
    print()
    print("Type 'help' to show the controls!")
    print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
    stock_input = input("What do you want to do: ").lower() # main input
    
    if stock_input == "day":
        update_prices() 
        day += 1
        clear_console()
        if day == random_event_day:
            random_functions = [prices_spike, prices_crash]
            random.choice(random_functions)() 
            update_prices() 
            day += 1
            clear_console()
    elif stock_input == "show":
        show_portfolio()
        print()
        print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
        time.sleep(2)
        clear_console()
    elif stock_input == "buy":
        buy_stock()
        print()
        show_achievements()
        clear_console()
    elif stock_input == "sell":
        sell_stock()
        print()
        show_achievements()
        clear_console()
    elif stock_input == "help":
        controls()
        print()
    elif stock_input == 'achieve':
        for achievement in achievements:
            print(f"- {achievement}")
        exit_achievements = input("Press any key to exit achievements: ")
        if exit_achievements:
            clear_console()
    elif stock_input == 'clear':
        clear_console()
    elif stock_input == "quit":
        print(f"Thank you for playing {username}!")
        exit()
    else:
        # entered invalid input
        clear_console()