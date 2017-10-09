from Tkinter import *
import random, time, string

VOWELS = "AEIOU"
CONSONANTS = "".join(set(string.uppercase) - set(VOWELS))

master = Tk()

def generator():
    choice = random.choice(["vowels", "consonants"])
    if choice == "vowels":
        letter = random.choice(VOWELS)
    elif choice == "consonants":
        letter = random.choice(CONSONANTS)
    return letter

def add_letter():
    w.pack()
    new_letter = generator()
    position_x = random.randint(0, 1000)
    position_y = random.randint(0, 500)
    w.create_text(position_x, position_y, text=new_letter, font=("Comic", "18"))
    master.after(500, add_letter)  # <== start the repeating process

w = Canvas(master, width=1000, height=500)

e = Entry(master)
e.pack()

e.focus_set()

def callback():
    print e.get()

b = Button(master, text='get', width=10, command=callback)
b.pack()

master.after(500, add_letter)  # <== start the repeating process
mainloop()