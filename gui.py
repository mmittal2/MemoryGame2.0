"""
NOTE: MUST INCORPORATE THE LOGIC FROM MEMORY_GAME INTO THE GUI
NOTE: MAINLY, DETERMINE HOW TO CHECK THE VALUE OF A CARD WHEN IT IS CLICKED
NOTE: ALSO FIGURE OUT HOW TO DETERMINE WHEN TO FLIP CARDS BACK OVER
NOTE: MAKE BUTTONS BLACK ONCE THE CARD HAS BEEN TAKEN BY A PLAYER
NOTE: ADD BUTTONS AND PROMPT REQUESTS FOR OTHER FUNCTIONALITY FOR THE GAME
"""


from tkinter import *
import tkinter.font
from PIL import Image, ImageTk
from glob import glob
import os
import random
import time


# define all variables used across multiple methods as global variables
global CARD_ORDER
CARD_ORDER = []
global CARDS_FLIPPED
CARDS_FLIPPED = []
global NUM_CARDS_TAKEN
NUM_CARDS_TAKEN = 0
global CARDS_TAKEN
CARDS_TAKEN = []
global PLAYER_SETS
PLAYER_SETS = []
global POINTS
POINTS = []
global NUM_PLAYERS
NUM_PLAYERS = None
global CURR_PLAYER
CURR_PLAYER = 1
global CARDS
CARDS = []
global USER_RESPONSE
USER_RESPONSE = None


# change matrix after a set of cards is chosen
def got_set():
    for c in CARDS_FLIPPED:
        buttons[c].destroy()
# change matrix after no set was chosen
def no_set():
    for c in CARDS_FLIPPED:
        buttons[c].config(image=card_back_img)
        
        
# get user input when they submit a response
def submit_response(num_players, points, player_sets):
    global NUM_PLAYERS
    NUM_PLAYERS = num_players
    global POINTS
    POINTS = points
    global PLAYER_SETS
    PLAYER_SETS = player_sets
    NUM_PLAYERS = user_input_box.get("1.0", "end-1c")
    NUM_PLAYERS = NUM_PLAYERS[29:]
    NUM_PLAYERS = NUM_PLAYERS.strip()
    NUM_PLAYERS = int(NUM_PLAYERS)
    # update points and player_sets
    for num in range(NUM_PLAYERS):
        POINTS.append(0)
        PLAYER_SETS.append([])


# arranges all cards at the beginning of the game
def arrange_cards(card_order, cards):
    global CARDS
    global CARD_ORDER
    CARD_ORDER = card_order
    # create a list of cards
    cards = []
    cards.append("Ace of Diamonds")
    cards.append("Ace of Hearts")
    cards.append("Ace of Spades")
    for i in range(2, 11):
        value = str(i)
        cards.append(value + " of Diamonds")
        cards.append(value + " of Hearts")
        cards.append(value + " of Spades")
    cards.append("Jack of Diamonds")
    cards.append("Jack of Hearts")
    cards.append("Jack of Spades")
    cards.append("King of Diamonds")
    cards.append("King of Hearts")
    cards.append("King of Spades")
    cards.append("Queen of Diamonds")
    cards.append("Queen of Hearts")
    cards.append("Queen of Spades")
    CARDS = cards
    
    # create a randomized order in which the cards should be placed on the board
    CARD_ORDER = list(range(39))
    random.shuffle(CARD_ORDER)
    
    """
    # create matrix containing the card positions
    cards_matrix = []
    for i in range(6):
        cards_matrix.append([])
        for x in range(i*6, i*6+6):
            cards_matrix[i].append(cards[CARD_ORDER[x]])
    cards_matrix.append([])
    for x in range(36, 39):
        cards_matrix[-1].append(cards[CARD_ORDER[x]])
    """


# show the card value when a player clicks on it
def show_card_when_clicked(num, card_order, cards_flipped, curr_player):
    global CARD_ORDER
    global CARDS_FLIPPED
    global CURR_PLAYER
    CARD_ORDER = card_order
    CARDS_FLIPPED = cards_flipped
    CURR_PLAYER = curr_player
    buttons[num].config(image=card_images[CARD_ORDER[num]])
    if len(CARDS_FLIPPED) == 0:
        CARDS_FLIPPED.append(num)
        decision_after_first_card_flip()


# let the user keep the card
def keep_card(window1, cards_flipped, curr_player, cards, card_order):
    global CARDS_FLIPPED
    CARDS_FLIPPED = cards_flipped
    global CURR_PLAYER
    CURR_PLAYER = curr_player
    global CARDS
    CARDS = cards
    global CARD_ORDER
    CARD_ORDER = card_order
    user_input_box.delete('1.0', 'end')
    if CARDS[CARD_ORDER[CARDS_FLIPPED[0]]] in PLAYER_SETS[CURR_PLAYER - 1]:
        got_set()
        user_input_box.insert('end', "Congrats! You get to keep this card! Next player!")
        CARDS_TAKEN.append(CARDS_FLIPPED[0])
    else:
        user_input_box.insert('end', "You do not have the other 2 cards with the same value as the card you just chose :(")
        time.sleep(1)
        user_input_box.insert('end', "This marks the end of your turn!")
        time.sleep(1)
        no_set()
    CURR_PLAYER += 1
    window1.destroy()      


# let user steal a set from another player
def steal_card(window1, cards_flipped):
    global CARDS_FLIPPED
    CARDS_FLIPPED = cards_flipped
    window1.destroy()


# let the user flip over the next card after their 1st one
def continue_playing(window1, cards_flipped):
    global CARDS_FLIPPED
    CARDS_FLIPPED = cards_flipped
    window1.destroy()
    

# let user keep 2 card set after flipping over 2nd card
def keep_set(window2, cards_flipped):
    global CARDS_FLIPPED
    CARDS_FLIPPED = cards_flipped
    window2.destroy()
    
    
# let user flip over a third card after finding a 2 card set
def flip_third_card(window2, cards_flipped):
    global CARDS_FLIPPED
    CARDS_FLIPPED = cards_flipped
    window2.destroy()


# create window
root = Tk()
root.title("Memory Game 2.0")
root.geometry("1200x600")


# set font
font_tuple = tkinter.font.Font(family="Comic Sans MS", size=12)


# list of file paths for all cards
card_pictures_paths = glob(os.path.join("Cards", "*.jpg"))


# add frame
frame = Frame(root)
frame.pack()


# resize the card pictures
card_back_img = Image.open("back.png")
card_back_img = card_back_img.resize((80, 120))
card_back_img = ImageTk.PhotoImage(card_back_img)
card_images = []
for c in card_pictures_paths:
    card_img = Image.open(c)
    card_img = card_img.resize((80, 120))
    card_img = ImageTk.PhotoImage(card_img)
    card_images.append(card_img)


# add buttons for each card
nums = list(range(0, 39))
x = 0
y = 0
buttons = dict()
for n in nums:
    buttons[n] = Button(frame, image=card_back_img, command=lambda num=n: show_card_when_clicked(num, CARD_ORDER, CARDS_FLIPPED, CURR_PLAYER))
    buttons[n].grid(row=x, column=y)
    y += 1
    if y == 13:
        y = 0
        x += 1


# add game functionality buttons
start_game_btn = Button(root, text="Start Game", font=font_tuple, command=lambda: arrange_cards(CARD_ORDER, CARDS))
start_game_btn.pack()


# add text box to ask for user input
user_input_box = Text(root, height=50, width=100, font=font_tuple)
user_input_box.pack(pady=10)


# ask for number of players
user_input_box.insert('end', "How many players are there? :")
# add submit button for user input
submit_btn = Button(root, text="Submit Response", font=font_tuple, command=submit_response(NUM_PLAYERS, POINTS, PLAYER_SETS))
submit_btn.pack()


# instructions pop-up window
pop_up_window = Toplevel(root, bd=20)
pop_up_window.geometry("700x500")
pop_up_window.title("Game Instructions")
instructions = "Welcome to Memory Game 2.0! Your goal is to find cards with the same value\
 (ex: the Ace of Hearts and the Ace of Diamonds have the same value).\n\n\
There are 13 sets of 3 cards each that have the same value. Players take turns flipping 2 cards each.\
 If they flip over 2 cards with the same value, they then have the option to try to find the third card with\
 the same value. If they choose not to, they get to keep the 2 cards they found.\
 On the other hand, if they choose to find the third card and are successful, they get to keep all 3 cards.\
 If they are unsuccessful, they must return the 2 cards they flipped over earlier. However, there's an additional twist.\
 If a player flips over their first card and remembers that the other player has the other 2 cards with that value,\
 they can steal those 2 cards from the other player. However, if they choose to steal the other player's card\
 when in fact the other player did not have those cards, their turn ends without them getting a chance to flip\
 over a second card. Additionally, if a player flips over their first card and remembers they have the other 2\
 cards with the same value, they can choose to keep that card (though they won't get any extra points by doing this).\n\n\
The player with the greatest number of points wins! Sets of 2 cards are worth 2 points while sets of 3 cards\
 are worth 4 points."
words = Text(pop_up_window, font=font_tuple)
words.pack()
words.insert(END, instructions)


# add 2 pop-up windows to ask for user input after they flip over a card
def decision_after_first_card_flip():
    global CARDS_FLIPPED
    window1 = Toplevel(root, bd=20)
    window1.geometry("700x500")
    window1.title("Decision after 1st Card Flip")
    keep_btn = Button(window1, text="Keep Card", command=lambda: keep_card(window1, CARDS_FLIPPED, CURR_PLAYER, CARDS, CARD_ORDER))
    steal_btn = Button(window1, text="Steal Card from Another Player", command=lambda: steal_card(window1, CARDS_FLIPPED))
    keep_playing_btn = Button(window1, text="Flip Over Next Card", command=lambda: continue_playing(window1, CARDS_FLIPPED))

def decision_after_second_card_flip():
    global CARDS_FLIPPED
    window2 = Toplevel(root, bd=20)
    window2.geometry("700x500")
    window2.title("Decision after Getting a 2 Card Set")
    keep_set_btn = Button(window2, text="Keep Current Set of 2 Cards", command=lambda: keep_set(window2, CARDS_FLIPPED))
    find_third_card_btn = Button(window2, text="Flip Over a Third Card", command=lambda: flip_third_card(window2, CARDS_FLIPPED))


root.mainloop()
