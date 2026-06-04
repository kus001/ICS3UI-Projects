import random
import pygame as pg
import time
from itertools import product
from urllib.request import urlopen
from io import BytesIO

"""Please don't start this until you have:
    * submitted Exercises 4.1 to 4.8
    * completed the Planning for Tabletop Game
    * reviewed the Ethical Computer Use assignment
"""
    
# Start your code here
# graphics varibles
pg.init()
WIDTH = 500
HEIGHT = 375
screen = pg.display.set_mode((WIDTH, HEIGHT)) # 4:3 ratio

# sketch font
font_data = urlopen("https://codehs.com/uploads/3123933db00a5c494909eb3d9eb72e56")
font_file = BytesIO(font_data.read())
sketch_font = pg.font.Font(font_file, 18)
WHITE = (255, 255, 255)

# card dimensions
CARD_WIDTH = 60
CARD_HEIGHT = 90

class Menu:
    def __init__(self):
        """initialize the variables for the menu"""
        self.start_screen = pg.image.load("start_screen.png")
        self.start_screen = pg.transform.scale(self.start_screen, (WIDTH, HEIGHT))
        self.instructions = pg.image.load("blackjack_instructions.png")
        self.instructions = pg.transform.scale(self.instructions, (WIDTH, HEIGHT))
        self.state = "menu" # menu or instructions (got help)
        self.mouse_x = None
        self.mouse_y = None
        
    def show_menu(self):
        """menu logic for button-clicking and states"""
        while True:
            if self.state == "menu":
                screen.blit(self.start_screen, (0,0))
            elif self.state == "instructions":
                screen.blit(self.instructions, (0,0))
        
            for event in pg.event.get():
                # check for mouse location
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1: # only left click
                    menu_mouse_x, menu_mouse_y = pg.mouse.get_pos()
                    # if pg.mouse.get_pressed()[0]:
                    print(f"({menu_mouse_x}, {menu_mouse_y})") # (218, 218) to (282, 242) PLAY
                        #                                  # (218, 257) to (282, 282) CONTROLS
                    if 218 <= menu_mouse_x <= 282 and 218 <= menu_mouse_y <= 242:
                        """start the game"""
                        return "play" # exits menu AND game starts
                    elif 218 <= menu_mouse_x <= 282 and 257 <= menu_mouse_y <= 282:
                        self.state = "instructions"
                    # exit button on the instructions    
                    if self.state == "instructions":
                        if 449 <= menu_mouse_x <= 480 and 15 <= menu_mouse_y <= 45:
                            self.state = "menu"
                
                    
            pg.display.update()

class Blackjack:
    def __init__(self):
        """initialize the variables in the game screen"""
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []
        self.game_over = False
        self.chips = 100 # starting chips for the player
        # cards
        self.card_images = {}
        
        self.card_images["QH"] = pg.transform.scale(pg.image.load("queen_of_hearts2.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["KS"] = pg.transform.scale(pg.image.load("king_of_spades2.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["QS"] = pg.transform.scale(pg.image.load("queen_of_spades2.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["QD"] = pg.transform.scale(pg.image.load("queen_of_diamonds2.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["QC"] = pg.transform.scale(pg.image.load("queen_of_clubs2.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["KH"] = pg.transform.scale(pg.image.load("king_of_hearts2.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["KD"] = pg.transform.scale(pg.image.load("king_of_diamonds2.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["KC"] = pg.transform.scale(pg.image.load("king_of_clubs2.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["JS"] = pg.transform.scale(pg.image.load("jack_of_spades2.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["JH"] = pg.transform.scale(pg.image.load("jack_of_hearts2.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["JD"] = pg.transform.scale(pg.image.load("jack_of_diamonds2.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["JC"] = pg.transform.scale(pg.image.load("jack_of_clubs2.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["AS"] = pg.transform.scale(pg.image.load("ace_of_spades2.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["10D"] = pg.transform.scale(pg.image.load("10_of_diamonds.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["9D"] = pg.transform.scale(pg.image.load("9_of_diamonds.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["8D"] = pg.transform.scale(pg.image.load("8_of_diamonds.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["7D"] = pg.transform.scale(pg.image.load("7_of_diamonds.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["6D"] = pg.transform.scale(pg.image.load("6_of_diamonds.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["5D"] = pg.transform.scale(pg.image.load("5_of_diamonds.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["4D"] = pg.transform.scale(pg.image.load("4_of_diamonds.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["3D"] = pg.transform.scale(pg.image.load("3_of_diamonds.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["2D"] = pg.transform.scale(pg.image.load("2_of_diamonds.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["2H"] = pg.transform.scale(pg.image.load("2_of_hearts.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["3H"] = pg.transform.scale(pg.image.load("3_of_hearts.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["4H"] = pg.transform.scale(pg.image.load("4_of_hearts.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["5H"] = pg.transform.scale(pg.image.load("5_of_hearts.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["6H"] = pg.transform.scale(pg.image.load("6_of_hearts.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["7H"] = pg.transform.scale(pg.image.load("7_of_hearts.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["8H"] = pg.transform.scale(pg.image.load("8_of_hearts.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["9H"] = pg.transform.scale(pg.image.load("9_of_hearts.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["10H"] = pg.transform.scale(pg.image.load("10_of_hearts.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["AH"] = pg.transform.scale(pg.image.load("ace_of_hearts.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["AD"] = pg.transform.scale(pg.image.load("ace_of_diamonds.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["2C"] = pg.transform.scale(pg.image.load("2_of_clubs.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["3C"] = pg.transform.scale(pg.image.load("3_of_clubs.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["4C"] = pg.transform.scale(pg.image.load("4_of_clubs.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["5C"] = pg.transform.scale(pg.image.load("5_of_clubs.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["6C"] = pg.transform.scale(pg.image.load("6_of_clubs.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["7C"] = pg.transform.scale(pg.image.load("7_of_clubs.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["8C"] = pg.transform.scale(pg.image.load("8_of_clubs.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["9C"] = pg.transform.scale(pg.image.load("9_of_clubs.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["10C"] = pg.transform.scale(pg.image.load("10_of_clubs.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["AC"] = pg.transform.scale(pg.image.load("ace_of_clubs.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["10S"] = pg.transform.scale(pg.image.load("10_of_spades.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["9S"] = pg.transform.scale(pg.image.load("9_of_spades.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["8S"] = pg.transform.scale(pg.image.load("8_of_spades.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["7S"] = pg.transform.scale(pg.image.load("7_of_spades.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["6S"] = pg.transform.scale(pg.image.load("6_of_spades.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["5S"] = pg.transform.scale(pg.image.load("5_of_spades.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["4S"] = pg.transform.scale(pg.image.load("4_of_spades.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["3S"] = pg.transform.scale(pg.image.load("3_of_spades.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        self.card_images["2S"] = pg.transform.scale(pg.image.load("2_of_spades.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
    
    def create_deck(self):
        """make a list of the 52 cards deck"""
        suits = ["C", "H", "D", "S"]
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.deck = list(product(ranks, suits)) # create deck

        # shuffle deck
        random.shuffle(self.deck)

        # test
        for i in range(4):
            print(f"{self.deck[i][0]} of {self.deck[i][1]}")
        
    def deal_card(self):
        """deal a random card from the deck"""
        return self.deck.pop() # removes the card from the deck
        
    def hand_value(self, hand): # use either player or dealer hand
        """determine the hand value of the card"""
        total = 0
        aces = 0 # worth 11 points
        for card, suit in hand: # no need for the suit, only the value is needed
            if card in ["J", "Q", "K"]: # king/queen/joker is worth 10 points
                total += 10 
            elif card == "A": # aces are worth 11 points
                total += 11 
                aces += 1
            else:
                total += int(card) # all the other numbered cards are added to the total
        """add an input section for the player to choose if they want the ace to be worth 11 points or 1 point"""
        while total > 21 and aces > 0: # blackjack logic (got help; since the player can either choose if the ace is worth 11 OR 1 point(s))
            total -= 10
            aces -= 1
            
        return total

    def get_bet(self):
        """ask the user to enter the bet"""
        self.bet = 0
        while self.bet == 0:
            screen.fill((0, 81, 44))
            
            # display betting menu
            chips_text = sketch_font.render(f"Chips: {self.chips}", True, WHITE)
            screen.blit(chips_text, (30, 50))
            
            bet_instructions = sketch_font.render("Press 1 for 10 chips, 2 for 20 chips, 3 for 50 chips.", True, WHITE)
            screen.blit(bet_instructions, (30, 100))
            
            pg.display.update()
            
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        self.bet = 10
                    elif event.key == pg.K_2:
                        self.bet = 20
                    elif event.key == pg.K_3:
                        self.bet = 50
                    else:
                        self.bet = 0 # invalid input

    def draw(self):
        """draw a prototype green board, and for the cards, have a ▯ symbol 
           with the value of the card beside it. A proper card display with 
           the suits will be added later. Think about having either a seperate play(self)
           function to keep it less cluttered, or just draw the visuals AND have the logic
           in the same loop (a bit easier, but messy)."""
        screen.fill((0, 81, 44))

        # player hand (will show on top)
        for i, (rank, suit) in enumerate(self.player_hand):
            """for the later versions, add a better font"""
            key = f"{rank}{suit}" 
            card_img = self.card_images[key]
            screen.blit(card_img, (20 + i*80, 250))

        # dealer hand (will show on bottom)
        for i, (rank, suit) in enumerate(self.dealer_hand):
            """for the later versions, add a better font"""
            key = f"{rank}{suit}" 
            card_img = self.card_images[key]
            screen.blit(card_img, (20 + i*80, 120))
        
    def play(self):
        """draw everything and call all the functions into the game"""
        # call all the functions
        self.game_over = False # restart the game
        self.create_deck()
        self.get_bet() # ask the user for any bets
        self.player_hand = [self.deal_card(), self.deal_card()] # the player starts with 2 cards
        self.dealer_hand = [self.deal_card(), self.deal_card()] # the dealer starts with 2 cards
        self.exit = pg.image.load("exit_symbol.png")
        self.exit = pg.transform.scale(self.exit, (20,20))
        self.restart = pg.image.load("restart_button.png")
        self.restart = pg.transform.scale(self.restart, (20,20))
        self.instructions_button = pg.image.load("instructions_button.png")
        self.instructions_button = pg.transform.scale(self.instructions_button, (20,20))
        self.instructions = pg.image.load("blackjack_instructions.png")
        self.instructions = pg.transform.scale(self.instructions, (WIDTH, HEIGHT))

        winner_displayed = False
        # graphics
        while True:
            screen.fill((0, 81, 44))
            self.draw()
            # buttons
            screen.blit(self.exit, (260, HEIGHT-30)) 
            screen.blit(self.instructions_button, (205, HEIGHT-30))
            
            # hit/stay logic
            """the player must press the 'h' key to hit, and the 's' key to stay"""
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_h: # player hits
                        self.player_hand.append(self.deal_card())
                        self.draw() # draw new card
                        pg.display.update() # blit new card
                        pg.time.delay(250) # delay animation to actually show the card
                        if self.hand_value(self.player_hand) > 21:
                            self.game_over = True
                        """display the pop-up menu where the player can either click to
                           rematch OR to quit"""
                    elif event.key == pg.K_s: # player stands
                        while self.hand_value(self.dealer_hand) < 17: # BLACKJACK RULE: the dealer must keep taking cards UNTIL they reach atleast 17
                            self.dealer_hand.append(self.deal_card())
                            """if the player stands, the they cannot take any more cards
                               until the next round. There, the scores of the dealer and 
                               the player are compared."""
                            self.draw() # draw new card
                            pg.display.update() # blit new card
                            pg.time.delay(250) # delay animation to actually show the card
                        self.game_over = True
                        
                if event.type == pg.MOUSEBUTTONDOWN:
                    game_mouse_x, game_mouse_y = pg.mouse.get_pos()
                    if 250 <= game_mouse_x <= 270 and HEIGHT-40 <= game_mouse_y <= HEIGHT-20: # exit button clicked
                        quit()
                    elif 195 <= game_mouse_x <= 215 and HEIGHT-50 <= game_mouse_y <= HEIGHT-10: # instructions button clicked
                        instructions_game_text = sketch_font.render("Controls: 'h' to hit & 's' to stay.", True, WHITE)
                        screen.blit(instructions_game_text, (WIDTH-250, HEIGHT/2))
                        pg.display.update()
                        pg.time.delay(3000) # delay for 3 seconds

            # decide the winner
            """to find the total value of either hands, use the hand value function with the desired hand for the parameter"""
            player_total = self.hand_value(self.player_hand)
            dealer_total = self.hand_value(self.dealer_hand)
            
            if self.game_over and not winner_displayed:
                # check if player busts
                if player_total > 21:
                    player_lost = sketch_font.render(f"BUST! Dealer wins 😂 with a {dealer_total}", True, WHITE)
                    screen.blit(player_lost, ((WIDTH/2)+20, HEIGHT/2))
                    self.chips -= self.bet # player loses bet
                    pg.display.update()
                    time.sleep(2) # wait 
                    winner_displayed = True 
                    return "menu" # return to menu
                elif dealer_total > 21:
                    player_won = sketch_font.render(f"Player wins with a {player_total} hand!", True, WHITE)
                    screen.blit(player_won, ((WIDTH/2)+20, HEIGHT/2))
                    self.chips += self.bet # player wins bet
                    pg.display.update()
                    time.sleep(2) # wait 
                    winner_displayed = True 
                    return "menu" # return to menu
                elif player_total > dealer_total and dealer_total >= 17:
                    player_lost = sketch_font.render(f"Player wins with a {player_total} hand!", True, WHITE)
                    screen.blit(player_lost, ((WIDTH/2)+20, HEIGHT/2))
                    self.chips += self.bet # player wins bet
                    pg.display.update()
                    time.sleep(2) # wait 
                    winner_displayed = True 
                    return "menu" # return to menu
                elif dealer_total > player_total and dealer_total >= 17:
                    player_lost = sketch_font.render(f"BUST! Dealer wins 😂 with a {dealer_total}", True, WHITE)
                    screen.blit(player_lost, ((WIDTH/2)+20, HEIGHT/2))
                    self.chips -= self.bet # player loses bet
                    pg.display.update()
                    time.sleep(2) # wait 
                    winner_displayed = True 
                    return "menu" # ret urn to menu
                else:
                    tie_text = sketch_font.render(f"TIE!", True, WHITE)
                    screen.blit(tie_text, ((WIDTH/2)+20, HEIGHT/2))
                    pg.display.update()
                    time.sleep(2) # wait 
                    winner_displayed = True 
                    return "menu" # return to menu
        
            # player/dealer totals
            # hand
            if not self.game_over:
                player_total = self.hand_value(self.player_hand)
                player_score = sketch_font.render(f"Player: {player_total}", True, WHITE)
                player_score_rect = (25, 30)
                screen.blit(player_score, player_score_rect)
                # dealer
                dealer_total = self.hand_value(self.dealer_hand)
                dealer_score = sketch_font.render(f"Dealer: {dealer_total}", True, WHITE)
                dealer_score_rect = (WIDTH-100, 30)
                screen.blit(dealer_score, dealer_score_rect)
            
            # chips
            player_chips = sketch_font.render(f"Chips: {self.chips}", True, WHITE)
            player_chips_rect = (WIDTH-100, HEIGHT-50)
            screen.blit(player_chips, player_chips_rect)
            
            pg.display.update()
            # pg.time.delay(4000)
        
game = Blackjack()
menu = Menu()

state = "menu"

while True:
    if state == "menu":
        state = menu.show_menu()
    elif state == "play":
        state = game.play()