import tkinter as tk
from tkinter.ttk import *
import sv_ttk
import pandas

#TODO 1. Set out GUI

# ------- Tkinter Setup -------- #

root = tk.Tk()
root.title("Typing Speed Test")
root.geometry("800x600+0+0")
root.config(padx=50, pady=50)
sv_ttk.use_light_theme()

# ------- Class Setup --------- #

nato_df = pandas.read_csv("nato_phonetic_alphabet.csv")
word_list = [row.code for (index, row) in nato_df.iterrows()]


class TypingTest:
    def __init__(self):
        # Title
        self.title = Label(root, text="Typing Speed Test")
        self.title.grid(row=0, column=0, columnspan=2)

        # Body
        self.body = Frame(root)
        self.body.grid(row=1, column=0, columnspan=2)
        self.body.config(padding=4)
        self.body["borderwidth"]=10

        # Stats
        self.cpm_label = Label(self.body, text="Corrected CPM: ")
        self.cpm_label.grid(row=0, column=0)
        self.cpm = Entry(self.body, width=5)
        self.cpm.insert(0, "?")
        self.cpm.grid(row=0, column=1)

        self.wpm_label = Label(self.body, text="WPM: ")
        self.wpm_label.grid(row=0, column=2)
        self.wpm = Entry(self.body, width=5)
        self.wpm.insert(0, "?")
        self.wpm.grid(row=0, column=3)

        self.timer_label = Label(self.body, text="Time left: ")
        self.timer_label.grid(row=0, column=4)
        self.timer = Entry(self.body, width=5)
        self.timer.insert(0, "60")
        self.timer.grid(row=0, column=5)

        # Words
        self.words = tk.Text(self.body, width=50, height=5, wrap="word")
        self.words.grid(row=1, column=0, columnspan=6, pady=5)

        for word in word_list:
            self.words.insert("end", f"{word} ")

        # Typing Zone
        self.typer = Entry(self.body, width=66, justify="center")
        self.typer.grid(row=2, column=0, columnspan=6)
        self.typer.focus()

        # Buttons
        self.quit_btn = Button(root, text="Quit", command=root.destroy)
        self.quit_btn.grid(row=3, column=0)

        self.restart_btn = Button(root, text="Restart")
        self.restart_btn.grid(row=3, column=1)


typing = TypingTest()
root.mainloop()

#TODO 2. Get a set of random words




#TODO 3. Have a timer

#TODO 4. Matching thing (on space)

#TODO 5. Count score