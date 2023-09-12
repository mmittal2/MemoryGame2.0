"""
NOTE: HAVEN'T ADDED THE TWIST - currently working on figuring out alternative to num_sets_taken
"""




import random
import time

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

# shuffle the cards
random.shuffle(cards)

# create the matrix of cards
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
print("This is a basic version of the Memory Game! Your goal is to find 2 cards with the same value (ex: the Ace of Hearts and the Ace of Diamonds have the same value).")
print("The player to find the greatest number of sets of cards with the same value wins!")
print("Let's start the game!")

num_sets_taken = 0
cards_taken = []

# keep track of number of players and set up player points
num_players = int(input("How many players are there? : "))
points = []
for num in range(num_players):
    points.append(0)

# display the matrix of numbers
def display_user_matrix():
    for row in display_matrix:
        print(row)
        
# play the game
while num_sets_taken < 13:
    n = 1
    while n <= num_players:
        display_user_matrix()
        first_card = int(input("Player " + str(n) + " pick the first card you'd like to flip over (type in a number from the table above - each number represents a card): "))
        while (first_card < 0 or first_card > 25 or first_card[0] in cards_taken):
            first_card = int(input("Invalid number. Please input a number that is valid: "))
        first_card_value = cards_matrix[int(first_card/6)][int(first_card%6)]
        display_matrix[int(first_card/6)][int(first_card%6)] = first_card_value
        print("Card one is " + first_card_value + ".")
        time.sleep(1)
        display_user_matrix()
        second_card = int(input("Player " + str(n) + " pick the second card you'd like to flip over (type in a number from the table above - each number represents a card): "))
        while (second_card < 0 or second_card > 25 or second_card[0] in cards_taken):
            second_card = int(input("Invalid number. Please input a number that is valid: "))
        second_card_value = cards_matrix[int(second_card/6)][int(second_card%6)]
        display_matrix[int(second_card/6)][int(second_card%6)] = second_card_value
        print("Card two is " + second_card_value + ".")
        time.sleep(1)
        display_user_matrix()
        # check if the 2 cards have the same value
        if first_card_value[0] == second_card_value[0]:
            print("You got a set!")
            points[n - 1] += 1
            num_sets_taken += 1
            cards_taken.append(first_card_value[0])
            print("You get another chance since you got a set!")
        else:
            print("That's not a set :(")
            display_matrix[int(first_card/6)][int(first_card%6)] = first_card
            display_matrix[int(second_card/6)][int(second_card%6)] = second_card 
            n += 1
        time.sleep(2)

# print out result
winner = [1]
for i in range(1, len(points)):
    if points[i] > points[winner[0]]:
        winner = [i + 1]
    elif points[i] == points[winner[0]]:
        winner.append(i + 1)
winners = ""
for w in winner:
    winners += str(w) + " and "
winners = winners[:-5]
print("The game is over! Player " + winners + " won!")
print("Below are the number of sets that each player collected:")
for i in range(len(points)):
    print("Player " + str(i + 1) + ": " + points[i] + " points")
    