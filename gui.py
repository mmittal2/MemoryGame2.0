from tkinter import *
import tkinter.font
from PIL import Image, ImageTk

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
card_back_img = Image.open("back.png")
card_back_img = card_back_img.resize((60, 100))
card_back_img = ImageTk.PhotoImage(card_back_img)

# add buttons for each card
nums = list(range(0, 39))
x = 0
y = 0
buttons = dict()
for n in nums:
    buttons[n] = Button(frame, image=card_back_img)
    buttons[n].grid(row=x, column=y)
    y += 1
    if y == 13:
        y = 0
        x += 1

# add game functionality buttons
start_game_btn = Button(root, text="Start Game", font=font_tuple)
start_game_btn.pack()


root.mainloop()