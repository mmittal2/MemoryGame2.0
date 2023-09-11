# AdvancedSoftwareProjects_Project1
First project for Advanced Software Projects class.




DESIGN DOC:

Overview: 
The goal of this project is to create a new version of the memory card game. In this game, 2 players compete against each other on the same graphical user interface. The interface will display 39 cards that are face down and once the users click on a card, it will turn over to reveal its value. The goal of the game is to find sets of 2 cards that have the same value. 

Tools: 
Python (Tkinter is used to create the graphical user interface) 

Design Decisions:
A unique twist is added to the game. Instead of using the full deck of cards, only 3 suits are used. This way, there are 3 cards with the same value. When a player picks 2 cards with the same value, they have an option to try to find the 3rd card or keep their 2 cards. If they choose to try to find the 3rd card and they pick a card that doesn’t have the value they were looking for, they lose the 2 cards they found. Additionally, if a player picks a card that has the same value as one of the other player’s sets, they can steal that set from the other player. At the end, the winner is determined by who has the most points. A set of 2 cards with the same value is worth 2 points while a set of three cards with the same value is worth 4 points.

Procedure:
1. Create basic graphical user interface displaying 26 cards that are clickable.
2. Write the logic for the code so that people can play the memory game without the twist.
3. If time, add code to enable players to play the version with the twist if they wish.
4. If time, add design elements to enhance the graphical user interface.
