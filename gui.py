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


global CARD_ORDER
CARD_ORDER = []


# arranges all cards at the beginning of the game
def arrange_cards(card_order):
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
    
    # create a randomized order in which the cards should be placed on the board
    CARD_ORDER = list(range(39))
    random.shuffle(CARD_ORDER)

    # create matrix containing the card positions
    cards_matrix = []
    for i in range(6):
        cards_matrix.append([])
        for x in range(i*6, i*6+6):
            cards_matrix[i].append(cards[CARD_ORDER[x]])
    cards_matrix.append([])
    for x in range(36, 39):
        cards_matrix[-1].append(cards[CARD_ORDER[x]])


# show the card value when a player clicks on it
def show_card_when_clicked(num, card_order):
    global CARD_ORDER
    CARD_ORDER = card_order
    buttons[num].config(image=card_images[CARD_ORDER[num]])


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
    buttons[n] = Button(frame, image=card_back_img, command=lambda num=n: show_card_when_clicked(num, CARD_ORDER))
    buttons[n].grid(row=x, column=y)
    y += 1
    if y == 13:
        y = 0
        x += 1


# add game functionality buttons
start_game_btn = Button(root, text="Start Game", font=font_tuple, command=lambda: arrange_cards(CARD_ORDER))
start_game_btn.pack()


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


root.mainloop()
