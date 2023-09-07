from tkinter import *
import tkinter.font
#from PIL import Image

# create window
root = Tk()
root.title("Memory Game 2.0")
root.geometry("900x600")

# set font
font_tuple = tkinter.font.Font(family="Comic Sans MS", size=12)

# add cards
# add frame
frame = Frame(root)
frame.pack()
# resize the pictures
"""
card_back_img = Image.open("back.png")
card_back_img = card_back_img.resize((50, 100))
"""
# add buttons for each card
card_1 = Button(frame, image="./AdvancedSoftwareProjects_Project1/back.png")
# add buttons
start_game_btn = Button(root, text="Start Game", font=font_tuple)
start_game_btn.pack()


root.mainloop()