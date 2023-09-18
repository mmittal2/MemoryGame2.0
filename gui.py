from tkinter import *
import tkinter.font
from PIL import Image, ImageTk
from glob import glob
import os
import random


# create all necessary variables
CARD_ORDER = [] # stores card positions on board
CARDS_FLIPPED = [] # stores which cards are currently flipped over
PLAYER_SETS = [] # stores each player's sets
POINTS = [] # stores each player's points
NUM_PLAYERS = None # total number of players
CURR_PLAYER = 1 # value for current player
CARDS = [] # stores names for each card in specific order (same for each game)
RESPONSES_ENTERED = 0 # number of user responses entered when stealing a set
NUM_CARDS_TAKEN = 0 # number of cards taken by players from the board
CARDS_TAKEN = [] # list of card names taken by players from the board


# ask next player to pick a card
def begin_next_player_turn():
    user_input_box.insert('end', "\nIt's Player " + str(CURR_PLAYER) + "'s turn now!")
    user_input_box.insert('end', "\nPlayer " + str(CURR_PLAYER) + " please click the first card to flip over.")


# player keeps a card or set
def got_set():
    global buttons
    global CARDS_FLIPPED
    global CARDS_TAKEN
    # delete the cards that have been chosen
    for c in CARDS_FLIPPED:
        buttons[c].destroy()
        CARDS_TAKEN.append(c)
    CARDS_FLIPPED = []
    # print out the game results if there are no more buttons left (meaning all cards have been taken)
    if NUM_CARDS_TAKEN == 39:
        # create a window to display the results
        results_window = Toplevel(root, bd=20)
        results_window.geometry("700x500")
        results_window.title("Game Over!")
        # calculate the winner based on points
        winner = [1]
        for i in range(1, len(POINTS)):
            if POINTS[i] > POINTS[winner[0] - 1]:
                winner = [i + 1]
            elif POINTS[i] == POINTS[winner[0] - 1]:
                winner.append(i + 1)
        # display the winners in the window
        winners = ""
        for w in winner:
            winners += str(w) + " and "
        winners = winners[:-5]
        results = "THE GAME IS OVER! \nPLAYER " + winners + " WON!"
        results += "\n\nBelow are the number of sets that each player collected:"
        for i in range(len(POINTS)):
            results += "\n\tPlayer " + str(i + 1) + ": " + str(POINTS[i]) + " points"
        results_box = Text(results_window, font=font_tuple)
        results_box.pack()
        results_box.insert('end', results)
        # user can end the game by clicking a button
        end_game_btn = Button(results_window, text="End Game", font=font_tuple, command=root.destroy)
        end_game_btn.pack()
        
# flip cards back over after a turn is over and no cards were taken
def no_set():
    global CARDS_FLIPPED
    global buttons
    for c in CARDS_FLIPPED:
        buttons[c].config(image=card_back_img)
    CARDS_FLIPPED = []


# update current player
def update_curr_player():
    global CURR_PLAYER
    CURR_PLAYER += 1
    if CURR_PLAYER > NUM_PLAYERS:
        CURR_PLAYER = 1

        
# ask user for the number of players and store in NUM_PLAYERS
def submit_player_num(button):
    global NUM_PLAYERS
    global POINTS
    global PLAYER_SETS
    NUM_PLAYERS = user_input_box.get("1.0", "end-1c")
    NUM_PLAYERS = NUM_PLAYERS[29:]
    NUM_PLAYERS = NUM_PLAYERS.strip()
    # if no response is entered, default to 2 players
    if len(NUM_PLAYERS) == 0:
        NUM_PLAYERS = 2
    NUM_PLAYERS = int(NUM_PLAYERS)
    # update POINTS and PLAYER_SETS
    for num in range(NUM_PLAYERS):
        POINTS.append(0)
        PLAYER_SETS.append([])
    user_input_box.insert('end', "\nThere are " + str(NUM_PLAYERS) + " players.")
    submit_btn.destroy()
    buttons_normal()
    begin_next_player_turn()
    button.destroy()


# arranges all cards at the beginning of the game
def arrange_cards(button):
    global CARDS
    global CARD_ORDER
    # create a list of card names and store in CARDS
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
    
    # ask for number of players
    user_input_box.insert('end', "How many players are there? : ")

    button.destroy()
    

# make all buttons clickable again
def buttons_normal(num=None):
    global buttons
    for x in range(0, len(buttons)):
        if not(x in CARDS_TAKEN):
            if num != None and x != num:
                buttons[x]["state"] = NORMAL
            elif num == None:
                buttons[x]["state"] = NORMAL


# close cards after cards flipped over but no set found
def close_cards(button):
    no_set()
    update_curr_player()
    user_input_box.delete('1.0', 'end')
    buttons_normal()
    begin_next_player_turn()
    button.destroy()
    

# what to do after a player clicks on a card
def show_card_when_clicked(num):
    global buttons
    global CARD_ORDER
    global CARDS_FLIPPED
    global CURR_PLAYER
    global POINTS
    global NUM_CARDS_TAKEN
    # show the face value of the card
    buttons[num].config(image=card_images[CARD_ORDER[num]])
    # prevent user from double-clicking a card or clicking another card
    for x in range(0, len(buttons)):
        if not(x in CARDS_TAKEN):
            buttons[x]["state"] = DISABLED
    # player flipped over their first card
    if len(CARDS_FLIPPED) == 0:
        CARDS_FLIPPED.append(num)
        decision_after_first_card_flip(num)
    # player flipped over their second card
    elif len(CARDS_FLIPPED) == 1:
        CARDS_FLIPPED.append(num)
        # player found a set
        if CARDS[CARD_ORDER[CARDS_FLIPPED[0]]][0] == CARDS[CARD_ORDER[CARDS_FLIPPED[1]]][0]:
            decision_after_second_card_flip(num)
        # player didn't find a set
        else:
            user_input_box.delete('1.0', 'end')
            user_input_box.insert('end', "You didn't get a set :(")
            close_cards_btn = Button(root, text="Close Cards", font=font_tuple, command=lambda: close_cards(close_cards_btn))
            close_cards_btn.pack()
            user_input_box.insert('end', "\nPlease click the close cards button.")
    # player flipped over their third card
    else:
        CARDS_FLIPPED.append(num)
        user_input_box.delete('1.0', 'end')
        # player got a set of 3 cards
        if CARDS[CARD_ORDER[CARDS_FLIPPED[2]]][0] == CARDS[CARD_ORDER[CARDS_FLIPPED[1]]][0]:
            user_input_box.insert('end', "You got the full set of three cards!")
            POINTS[CURR_PLAYER - 1] += 4
            PLAYER_SETS[CURR_PLAYER - 1].append(CARDS[CARD_ORDER[CARDS_FLIPPED[2]]][0])
            NUM_CARDS_TAKEN += 3
            got_set()
            user_input_box.insert('end', "\nYou get another chance since you got a set!")
            buttons_normal()
            user_input_box.insert('end', "\nPlayer " + str(CURR_PLAYER) + " please click the first card to flip over.")
        # third card doesn't match the first 2 cards
        else:
            user_input_box.insert('end', "This third card doesn't have the same value as your first two cards :(")
            user_input_box.insert('end', "\nYou didn't gain any sets or points this time.")
            close_cards_btn = Button(root, text="Close Cards", font=font_tuple, command=lambda: close_cards(close_cards_btn))
            close_cards_btn.pack()
            user_input_box.insert('end', "\nPlease click the close cards button.")


# user chooses to keep the first card they flipped over
def keep_card(window1):
    global CARDS_FLIPPED
    global CURR_PLAYER
    global CARDS
    global CARD_ORDER
    global NUM_CARDS_TAKEN
    user_input_box.delete('1.0', 'end')
    # player can keep the card (because they have the other 2 cards with the same value)
    if CARDS[CARD_ORDER[CARDS_FLIPPED[0]]][0] in PLAYER_SETS[CURR_PLAYER - 1]:
        update_curr_player()
        user_input_box.insert('end', "Congrats! You get to keep this card! Next player!")
        buttons_normal()
        NUM_CARDS_TAKEN += 1
        got_set()
        begin_next_player_turn() 
    # player can't keep the card (because they don't have the other 2 cards with the same value)
    else:
        user_input_box.insert('end', "You do not have the other 2 cards with the same value as the card you just chose :(")
        user_input_box.insert('end', "\nThis marks the end of your turn!")
        buttons_normal()
        no_set()
        update_curr_player()
        begin_next_player_turn()
    window1.destroy()  


# what to do after user inputs a valid other player number when stealing a set
def steal_valid_input(other_player):
    global CARDS
    global CARDS_FLIPPED
    global CARD_ORDER
    global PLAYER_SETS
    global POINTS
    global NUM_CARDS_TAKEN
    other_player = int(other_player)
    # user chooses the correct player and can steal that player's set
    if CARDS[CARD_ORDER[CARDS_FLIPPED[0]]][0] in PLAYER_SETS[other_player - 1]:
        user_input_box.delete('1.0', 'end')
        user_input_box.insert('end', "Congrats! You get to steal the other player's cards!")
        POINTS[CURR_PLAYER - 1] += 4
        POINTS[other_player - 1] -= 2
        NUM_CARDS_TAKEN += 1
        PLAYER_SETS[CURR_PLAYER - 1].append(CARDS[CARD_ORDER[CARDS_FLIPPED[0]]][0])
        PLAYER_SETS[other_player - 1].remove(CARDS[CARD_ORDER[CARDS_FLIPPED[0]]][0])
        got_set()
    # user chooses the wrong player and can't steal the set
    else:
        user_input_box.delete('1.0', 'end')
        user_input_box.insert('end', "Player " + str(other_player) + " doesn't have the other 2 cards with the same value as the card you just chose :(")
        user_input_box.insert('end', "\nYour turn is now over. Next player!")
        no_set()
    update_curr_player()
    buttons_normal()
    begin_next_player_turn()


# user chooses to try to steal a set from another player
def steal_response(user_input, window1):
    global CURR_PLAYER
    global RESPONSES_ENTERED
    global CARDS_FLIPPED
    global PLAYER_SETS
    global POINTS
    global NUM_CARDS_TAKEN
    user_input_box.delete('1.0', 'end')
    # user inputs the number of another player for the first time
    if RESPONSES_ENTERED == 0:
        # get the user input from the text widget
        other_player = user_input.get("1.0", "end-1c")
        other_player = other_player[70:]
        other_player = other_player.strip()
        # give the user another chance if they did not enter anything or did not put the number of another player
        if len(other_player) == 0 or (len(other_player) != 0 and (int(other_player) < 1 or int(other_player) > NUM_PLAYERS or int(other_player) == CURR_PLAYER)):
            user_input.insert('end', "\nThat was an invalid input.") 
            user_input.delete('1.0', 'end')
            user_input.insert('end', "Please input the number of another player: ")
            RESPONSES_ENTERED += 1
        # check if user can steal the set since they inputed a valid other player number
        else:
            steal_valid_input(other_player)
            RESPONSES_ENTERED = 0
            window1.destroy()
    # user inputs the number of another player for the second time
    elif RESPONSES_ENTERED == 1:
        # get the user input from the text widget
        other_player = user_input.get("1.0", "end-1c")
        other_player = other_player[43:]
        other_player = other_player.strip()
        window1.destroy()
        # end the user turn if they didn't enter anything again or entered another invalid number
        if len(other_player) == 0 or (len(other_player) != 0 and (int(other_player) < 1 or int(other_player) > NUM_PLAYERS or int(other_player) == CURR_PLAYER)):
            update_curr_player()
            user_input_box.insert('end', "You entered another incorrect input. Your turn is over now. Next player!")
            no_set()
            buttons_normal()
            begin_next_player_turn()
        # check if user can steal the set since they inputed a valid other player number
        else:
            steal_valid_input(other_player)
        RESPONSES_ENTERED = 0


# ask user which player they want to steal a card from
def steal_card(window1):
    user_input = Text(window1, width=90, height=5, font=font_tuple)
    user_input.pack()
    user_input.insert('end', "Which player do you wish to steal cards from (type in their number)?: ")
    submit_response_btn = Button(window1, text="Submit Response", font=font_tuple, command=lambda: steal_response(user_input, window1))
    submit_response_btn.pack()


# let user flip over their second card
def continue_playing(window1, num):
    window1.destroy()
    user_input_box.delete('1.0', 'end')
    buttons_normal(num)
    user_input_box.insert('end', "Player " + str(CURR_PLAYER) + " please click the second card to flip over.") 


# let user keep a set of 2 cards
def keep_set(window2):
    global POINTS
    global PLAYER_SETS
    global NUM_CARDS_TAKEN
    window2.destroy()
    user_input_box.delete('1.0', 'end')
    POINTS[CURR_PLAYER - 1] += 2
    PLAYER_SETS[CURR_PLAYER - 1].append(CARDS[CARD_ORDER[CARDS_FLIPPED[0]]][0])
    NUM_CARDS_TAKEN += 2
    got_set()
    # give the current player another turn since they got a set
    user_input_box.insert('end', "You get another chance since you got a set!")
    buttons_normal()
    user_input_box.insert('end', "\nPlayer " + str(CURR_PLAYER) + " please click the first card to flip over.")
    
    
# let user flip over a third card after finding a set of 2 cards
def flip_third_card(window2, num):
    window2.destroy()
    user_input_box.delete('1.0', 'end')
    buttons_normal(num)
    user_input_box.insert('end', "Player " + str(CURR_PLAYER) + " please click on the third card to flip over.")
    

# create window where cards will be displayed
root = Tk()
root.title("Memory Game 2.0")
root.geometry("1200x800")


# set font
font_tuple = tkinter.font.Font(family="Comic Sans MS", size=12)


# add frame
frame = Frame(root)
frame.pack()


# list of file paths for card jpg pictures
card_pictures_paths = glob(os.path.join("Cards", "*.jpg"))


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
    buttons[n] = Button(frame, image=card_back_img, command=lambda num=n: show_card_when_clicked(num))
    buttons[n].grid(row=x, column=y)
    buttons[n]["state"] = DISABLED
    y += 1
    if y == 13:
        y = 0
        x += 1


# add button to start the game
start_game_btn = Button(root, text="Start Game", font=font_tuple, command=lambda: arrange_cards(start_game_btn))
start_game_btn.pack()


# add text box to ask for user input
user_input_box = Text(root, height=8, width=100, font=font_tuple)
user_input_box.pack(pady=10)


# add button that collects/gets user input
submit_btn = Button(root, text="Submit Response", font=font_tuple, command=lambda: submit_player_num(submit_btn))
submit_btn.pack()


# create instructions pop-up window
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
words.insert('end', instructions)


# add 2 pop-up windows to ask for user input after they flip over a card
def decision_after_first_card_flip(num):
    window1 = Toplevel(root, bd=20)
    window1.geometry("700x500")
    window1.title("Decision after 1st Card Flip")
    text_instructions = Text(window1, height=4, width=70, font=font_tuple)
    text_instructions.insert('end', "Do you wish to keep this card (if you have the other 2 cards with the same value)\
 or steal another player's set (if another player has the other 2 cards with the same value)? Please refer to the instructions for clarification on what each option does.")
    text_instructions.pack()
    keep_btn = Button(window1, text="Keep Card", font=font_tuple, command=lambda: keep_card(window1))
    keep_btn.pack()
    steal_btn = Button(window1, text="Steal Card from Another Player", font=font_tuple, command=lambda: steal_card(window1))
    steal_btn.pack()
    keep_playing_btn = Button(window1, text="Flip Over Next Card", font=font_tuple, command=lambda: continue_playing(window1, num))
    keep_playing_btn.pack()
def decision_after_second_card_flip(num):
    window2 = Toplevel(root, bd=20)
    window2.geometry("700x500")
    window2.title("Decision after Getting a 2 Card Set")
    keep_set_btn = Button(window2, text="Keep Current Set of 2 Cards", font=font_tuple, command=lambda: keep_set(window2))
    keep_set_btn.pack()
    find_third_card_btn = Button(window2, text="Flip Over a Third Card", font=font_tuple, command=lambda: flip_third_card(window2, num))
    find_third_card_btn.pack()


root.mainloop()
