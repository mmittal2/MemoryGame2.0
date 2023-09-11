import random

# create a list of cards
cards = []
cards.append("Ace of Hearts")
cards.append("Ace of Diamonds")
for i in range(2, 10):
    value = str(i)
    cards.append(value + "of Hearts")
    cards.append(value + "of Diamonds")
cards.append("Jack of Hearts")
cards.append("Jack of Diamonds")
cards.append("Queen of Hearts")
cards.append("Queen of Diamonds")
cards.append("King of Hearts")
cards.append("King of Diamonds")

# shuffle the cards
random.shuffle(cards)

# create the matrix of cards
cards_matrix = []
for i in range(4):
    cards_matrix.append(cards[i*6:i*6+6])
cards_matrix.append([cards[-2:]])

# create matrix with numbers representing cards (this is the matrix the user will see)
display_matrix = []
for i in range(4): 
    display_matrix.append(list(range(i*6, i*6+6)))
display_matrix.append([25, 26])

    
# print instructions for game
print("This is a basic version of the Memory Game! Your goal is to find 2 cards with the same value (ex: the Ace of Hearts and the Ace of Diamonds have the same value).")
print("The player to find the greatest number of sets of cards with the same value wins!")
print("Let's start the game!")

num_sets_taken = 0

num_players = input("How many players are there? : ")

# display the matrix of numbers
for row in display_matrix:
    print(row)
    
while num_sets_taken < 13:
    for n in num_players:
        first_card = input("Player", str(n) ,"pick the first card you'd like to flip over (type in a number from the table above - each number represents a card): ")
        first_card_value = 
    
    
