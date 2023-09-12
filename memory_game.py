# import required libraries
import random
import time

# create necessary functions
# display the matrix of numbers
def display_user_matrix():
    print()
    for row in display_matrix:
        print(row)
# ask user for a number and get the card associated with that number
def get_card_from_user(card_num):
    card = int(input("Player " + str(n) + " pick a card you'd like to flip over (type in a number from the table above - each number represents a card): "))
    while (card < 0 or card > 25 or card in cards_taken):
        card = int(input("Invalid number. Please input a number that is valid: "))
    card_value = cards_matrix[int(card/6)][int(card%6)]
    display_matrix[int(card/6)][int(card%6)] = card_value
    print()
    print("Card " + card_num + " is " + card_value + ".")
    time.sleep(1)
    display_user_matrix()
    time.sleep(1)
    return (card, card_value)
# change matrix after a set of cards is chosen
def got_set(cards):
    for c in cards:
        display_matrix[int(c/6)][int(c%6)] = "X"
# change matrix after no set was chosen
def no_set(cards):
    for c in cards:
        display_matrix[int(c/6)][int(c%6)] = c
    
# create necessary variables
num_cards_taken = 0
cards_taken = []
player_sets = []
points = []

# create a list of cards
cards = []
cards.append("Ace of Hearts")
cards.append("Ace of Diamonds")
cards.append("Ace of Spades")
for i in range(2, 10):
    value = str(i)
    cards.append(value + " of Hearts")
    cards.append(value + " of Diamonds")
    cards.append(value + " of Spades")
cards.append("Jack of Hearts")
cards.append("Jack of Diamonds")
cards.append("Jack of Spades")
cards.append("Queen of Hearts")
cards.append("Queen of Diamonds")
cards.append("Queen of Spades")
cards.append("King of Hearts")
cards.append("King of Diamonds")
cards.append("King of Spades")

# shuffle the cards (so that each game has a different board)
random.shuffle(cards)

# create matrix containing the card positions
cards_matrix = []
for i in range(6):
    cards_matrix.append(cards[i*6:i*6+6])
cards_matrix.append(cards[-3:])

# create matrix with numbers representing cards (this is the matrix the user will see)
display_matrix = []
for i in range(6): 
    display_matrix.append(list(range(i*6, i*6+6)))
display_matrix.append([36, 37, 38])
    
# print instructions for game
print("Welcome to Memory Game 2.0! Your goal is to find cards with the same value\
 (ex: the Ace of Hearts and the Ace of Diamonds have the same value).")
print()
print("There are 13 sets of 3 cards each that have the same value. Players take turns flipping 2 cards each.\
 If they flip over 2 cards with the same value, they then have the option to try to find the third card with\
 the same value. If they choose not to, they get to keep the 2 cards they found.\
 On the other hand, if they choose to find the third card and are successful, they get to keep all 3 cards.\
 If they are unsuccessful, they must return the 2 cards they flipped over earlier. However, there's an additional twist.\
 If a player flips over their first card and remembers that the other player has the other 2 cards with that value,\
 they can steal those 2 cards from the other player. However, if they choose to steal the other player's card\
 when in fact the other player did not have those cards, their turn ends without them getting a chance to flip\
 over a second card. Additionally, if a player flips over their first card and remembers they have the other 2\
 cards with the same value, they can choose to keep that card (though they won't get any extra points by doing this).")
print()
print("The player with the greatest number of points wins! Sets of 2 cards are worth 2 points while sets of 3 cards\
 are worth 4 points.")
print()
print()
print("Let's start the game!")
print()

# keep track of number of players and set up player points and sets
num_players = int(input("How many players are there? : "))
for num in range(num_players):
    points.append(0)
    player_sets.append([])
        
# play the game until all cards have been chosen
while num_cards_taken < 39:
    n = 1
    # cycle through all the players each round
    while n <= num_players:
        display_user_matrix()
        # ask user to flip over first card
        first_card, first_card_value = get_card_from_user("one")
        twist_decision = input("Do you wish to keep this card (if you have the other 2 cards with the same value)\
 or steal another player's set (if another player has the other 2 cards with the same value)? (keep/steal/no): ")
        time.sleep(1)
        while twist_decision.lower() != "keep" and twist_decision.lower() != "steal" and twist_decision.lower() != "no":
            twist_decision = input("That was an invalid input. Please type either keep, steal, or no: ")
        if twist_decision == "keep":
            if first_card_value[0] in player_sets[n - 1]:
                got_set([first_card])
                print("Congrats! You get to keep this card! Next player!")
                cards_taken.append(first_card)
            else:
                print("You do not have the other 2 cards with the same value as the card you just chose :(")
                time.sleep(1)
                print("This marks the end of your turn!")
                time.sleep(1)
                no_set([first_card])
            n += 1
        elif twist_decision == "steal":
            other_player = int(input("Which player do you wish to steal cards from (type in their number)?: "))
            time.sleep(1)
            while other_player < 1 or other_player >= n:
                other_player = int(input("That was an invalid input. Please input the number of another player: "))
            if first_card_value[0] in player_sets[other_player - 1]:
                print("Congrats! You get to steal the other player's cards!")
                time.sleep(1)
                print("Next player!")
                points[n - 1] += 3
                points[other_player - 1] -= 2
                got_set([first_card])
                cards_taken.append(first_card)
                player_sets[n - 1].append(first_card_value[0])
                player_sets[other_player - 1].remove(first_card_value[0])
            else:
                print("Player " + str(other_player) + " doesn't have the other 2 cards with the same value as the card you just chose :(")
                time.sleep(1)
                print("Your turn is now over. Next player!")
                time.sleep(1)
                no_set([first_card])
            n += 1
        else:
            second_card, second_card_value = get_card_from_user("two")
            # check if the 2 cards have the same value
            if first_card_value[0] == second_card_value[0]:
                print("You got a set of two cards!")
                time.sleep(1)
                third_card_decision = input(print("Do you want to try to find the third card? (yes/no): "))
                time.sleep(1)
                if third_card_decision.lower() == "yes":
                    third_card, third_card_value = get_card_from_user("three")
                    if third_card_value[0] == first_card_value[0]:
                        print("You got the full set of three cards!")
                        time.sleep(1)
                        points[n - 1] += 4
                        num_cards_taken += 3
                        cards_taken.append(first_card)
                        print("You get another chance since you got a set!")
                        time.sleep(1)
                        got_set([first_card, second_card, third_card])
                        player_sets[n - 1].append(first_card_value[0])
                    else:
                        print("This third card doesn't have the same value as your first two cards :(")
                        time.sleep(1)
                        print("You didn't gain any sets or points this time.")
                        time.sleep(1)
                        no_set([first_card, second_card, third_card])
                        n += 1
                else:
                    points[n - 1] += 2
                    num_cards_taken += 2
                    cards_taken.append(first_card)
                    print("You get another chance since you got a set!")
                    time.sleep(1)
                    got_set([first_card, second_card])
                    player_sets[n - 1].append(first_card_value[0])
            else:
                print("That's not a set :(")
                time.sleep(1)
                display_matrix[int(first_card/6)][int(first_card%6)] = first_card
                display_matrix[int(second_card/6)][int(second_card%6)] = second_card 
                n += 1
                no_set([first_card, second_card])
            time.sleep(2)

# determine the winner(s) by determining who has the most points
winner = [1]
for i in range(1, len(points)):
    if points[i] > points[winner[0]]:
        winner = [i + 1]
    elif points[i] == points[winner[0]]:
        winner.append(i + 1)
# print out the results of the game (winner(s) and points each player got)
winners = ""
for w in winner:
    winners += str(w) + " and "
winners = winners[:-5]
print("The game is over! Player " + winners + " won!")
time.sleep(1)
print("Below are the number of sets that each player collected:")
time.sleep(1)
for i in range(len(points)):
    print("Player " + str(i + 1) + ": " + points[i] + " points")
    