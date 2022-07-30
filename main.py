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
        # Variables
        self.time = 0
        self.time_limit = 60
        self.cpm_score = 0
        self.wpm_score = 0
        self.position = 0

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
        self.cpm = Entry(self.body, width=5, justify="center")
        self.cpm.insert(0, "?")
        self.cpm.grid(row=0, column=1)

        self.wpm_label = Label(self.body, text="WPM: ")
        self.wpm_label.grid(row=0, column=2)
        self.wpm = Entry(self.body, width=5, justify="center")
        self.wpm.insert(0, "?")
        self.wpm.grid(row=0, column=3)

        self.timer_label = Label(self.body, text="Time left: ")
        self.timer_label.grid(row=0, column=4)
        self.timer = Entry(self.body, width=5, justify="center")
        self.timer.insert(0, "60")
        self.timer.grid(row=0, column=5)

        # Words
        self.words = tk.Text(self.body, width=50, height=5, wrap="word")
        self.words.grid(row=1, column=0, columnspan=6, pady=5)

        for word in word_list:
            word = word.lower()
            self.words.insert("end", f"{word} ")

        self.string_of_words = self.words.get("1.0", "end")

        # Typing Zone
        self.typer = Entry(self.body, width=66, justify="center")
        self.typer.grid(row=2, column=0, columnspan=6)
        self.typer.focus()
        self.typer.bind("<KeyRelease>", self.start)

        # Buttons
        self.quit_btn = Button(root, text="Quit", command=root.destroy)
        self.quit_btn.grid(row=3, column=0)

        self.restart_btn = Button(root, text="Restart", command=self.reset)
        self.restart_btn.grid(row=3, column=1)

    # ----------- LOGIC -------------- #

    def start(self, event):
        self.time = 0
        self.position = 0
        self.countdown()
        self.input_handler(event)
        self.typer.bind("<KeyRelease>", self.input_handler)

    def countdown(self):
        if self.time == self.time_limit:
            self.typer.config(state="disabled")
        elif self.time > self.time_limit:
            self.typer.config(state="normal")
        else:
            self.time += 1
            time_remaining = self.time_limit - self.time
            self.timer.delete(0, "end")
            self.timer.insert(0, f"{time_remaining}")
            # After 1 second, start again
            self.body.after(1000, self.countdown)

    def reset(self):
        # Delete Entries
        self.time = self.time_limit * 2
        self.timer.delete(0, "end")
        self.wpm.delete(0, "end")
        self.cpm.delete(0, "end")
        self.typer.delete(0, "end")
        self.words.tag_delete("correct_char", "incorrect_char")

        # Back to starting values
        self.timer.insert(0, f"{self.time_limit}")
        self.wpm.insert(0, "?")
        self.cpm.insert(0, "?")
        self.typer.focus()
        self.typer.bind("<KeyRelease>", self.start)

    def input_handler(self, event):
        if event.char:
            self.check_char(event)
        elif event.keysym == "BackSpace":
            self.backspace()

    def check_char(self, event):
        char_typed = event.char
        if char_typed == self.string_of_words[self.position]:
            self.words.tag_add("correct_char", f"1.{self.position}", f"1.{self.position + 1}")
            self.words.tag_config("correct_char", background="blue")
            print(f"{char_typed} - Correct")
        else:
            print(f"{char_typed} - Incorrect")
            self.words.tag_add("incorrect_char", f"1.{self.position}", f"1.{self.position + 1}")
            self.words.tag_config("incorrect_char", background="red")
        self.position += 1

    def backspace(self):
        self.position -= 1
        self.words.tag_remove("correct_char", f"1.{self.position}", f"1.{self.position + 1}")
        self.words.tag_remove("incorrect_char", f"1.{self.position}", f"1.{self.position + 1}")

typing = TypingTest()
root.mainloop()

#TODO 2. Get a set of random words

#TODO 4. Matching thing (on space)

#TODO 5. Count score