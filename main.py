import tkinter as tk
from tkinter.ttk import *
import sv_ttk
import random

# ------- Tkinter Setup -------- #

root = tk.Tk()
root.title("Typing Speed Test")
root.geometry("510x500+0+0")
root.config(padx=40, pady=40, background="#DDD2E6")
sv_ttk.use_light_theme()
background = Style()
background.configure("P.TButton", highlightcolor="#DDD2E6")

# ------- Getting words ------- #

with open("random-words.txt") as random_words:
    word_list = random_words.read().split(",")
word_list.pop(0)


# ------- Class Setup --------- #

class TypingTest:
    def __init__(self):
        # Variables
        self.time = 0
        self.time_limit = 60
        self.cpm_score = 0
        self.wpm_score = 0
        self.position = 0
        self.word_number = 0
        self.cpm_correct_total = 0
        self.milestone = 0

        # Title
        self.title = Label(root, text="Typing Speed Test", padding=5)
        self.title.grid(row=0, column=0, columnspan=5)
        self.title.config(font=('Calibri', 20, "bold"), background="#DDD2E6")

        # Most Recent Scores
        self.recent_frame = Frame(root)
        self.recent_frame.grid(row=1, column=0, columnspan=5, pady=20, padx=20)

        self.recent_body = Frame(self.recent_frame, padding=5)
        self.recent_body.grid(row=0, column=0)
        self.recent_body.config(borderwidth=2, relief="solid")

        self.recent_scores = Label(self.recent_body, text="Most recent score:")
        self.recent_scores.grid(row=0, column=0, columnspan=2, pady=5, sticky="W", padx=(5, 0))

        self.recent_cpm_label = Label(self.recent_body, text="Corrected CPM: ")
        self.recent_cpm_label.grid(row=1, column=0, padx=(20, 0))
        self.recent_cpm = Entry(self.recent_body, width=5, justify="center")
        self.recent_cpm.grid(row=1, column=1, padx=(0, 20))

        self.recent_wpm_label = Label(self.recent_body, text="Corrected WPM: ")
        self.recent_wpm_label.grid(row=1, column=3, padx=(14, 0))
        self.recent_wpm = Entry(self.recent_body, width=5, justify="center")
        self.recent_wpm.grid(row=1, column=5, padx=(0, 20))

        # Body
        self.body = Frame(root)
        self.body.grid(row=2, column=0, columnspan=5)
        self.body.config(borderwidth=4, relief='solid')

        # Stats
        self.cpm_label = Label(self.body, text="Corrected CPM: ")
        self.cpm_label.grid(row=0, column=0, padx=(10, 0))
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
        self.timer.grid(row=0, column=5, pady=10, padx=(0, 10))

        # Words
        self.words = tk.Text(self.body, width=50, height=3, wrap="word")
        self.words.grid(row=1, column=0, columnspan=6, pady=5)
        random.shuffle(word_list)

        for word in word_list:
            word = word.lower()
            self.words.insert("end", f"{word} ")

        self.string_of_words = self.words.get("1.0", "end")

        # Typing Zone
        self.typer = Entry(self.body, width=49, justify="center")
        self.typer.grid(row=2, column=0, columnspan=6, pady=(15, 20), padx=10)
        self.typer.focus()
        self.typer.bind("<KeyPress>", self.start)

        # Buttons
        self.quit_btn = Button(root, text="Quit", command=root.destroy, style="P.TButton")
        self.quit_btn.grid(row=3, column=0, pady=20)

        self.restart_btn = Button(root, text="Restart", command=self.reset, style="P.TButton")
        self.restart_btn.grid(row=3, column=4, pady=20)

    # ----------- LOGIC -------------- #

    def start(self, event):
        self.milestone = 0
        self.time = 0
        self.position = 0
        self.word_number = 0
        self.cpm_correct_total = 0
        self.countdown()
        # This checks the first key pressed
        self.input_handler(event)
        # This turns on the checking for the subsequent keys pressed
        self.typer.bind("<KeyPress>", self.input_handler)

    def countdown(self):
        if self.time == self.time_limit:
            # When the game is over, prevent the user from typing and save the score
            self.typer.config(state="disabled")
            self.typer.unbind("<KeyPress>")
            self.save_score()
        elif self.time > self.time_limit:
            # This sets things to normal when the restart button is pressed
            self.typer.config(state="normal")
        else:
            # This is the normal countdown
            self.time += 1
            time_remaining = self.time_limit - self.time
            # This displays the time left
            self.timer.delete(0, "end")
            self.timer.insert(0, f"{time_remaining}")
            # After 1 second, start again
            self.body.after(1000, self.countdown)

    def reset(self):
        # Delete Entries
        self.typer.config(state="normal")
        self.time = self.time_limit * 2
        self.timer.delete(0, "end")
        self.wpm.delete(0, "end")
        self.cpm.delete(0, "end")
        self.typer.delete(0, "end")
        self.words.tag_delete("correct_char", "incorrect_char")
        self.words.delete("1.0", "end")

        # Back to starting values
        self.timer.insert(0, f"{self.time_limit}")
        self.wpm.insert(0, "?")
        self.cpm.insert(0, "?")
        self.typer.focus()
        self.typer.config(state="normal")
        self.typer.bind("<KeyPress>", self.start)
        self.words.config(state="normal")
        # Creating a random word list and string of all words put together.
        # You need both forms to do different functions.
        random.shuffle(word_list)
        # The 'words' object is useful for word to word gameplay
        for word in word_list:
            word = word.lower()
            self.words.insert("end", f"{word} ")

        # String of words is useful for the character to character gameplay
        self.string_of_words = self.words.get("1.0", "end")
        self.words.config(state="disabled")

    def input_handler(self, event):
        if event.keysym == "BackSpace":
            self.backspace()
        elif event.char:
            self.check_char(event)
        else:
            # This deals if someone tries to press non-character keys
            return

    def check_char(self, event):
        char_typed = event.char.lower()
        if char_typed == " ":
            self.check_word()

        elif char_typed == self.string_of_words[self.position]:
            # Compares the character typed to the particular character in the string of words
            # If it is the same, it highlights the character blue
            self.words.tag_add("correct_char", f"1.{self.position}", f"1.{self.position + 1}")
            self.words.tag_config("correct_char", background="#7C9BE8", foreground="white")
        else:
            # If it is different, it highlights the character red
            self.words.tag_add("incorrect_char", f"1.{self.position}", f"1.{self.position + 1}")
            self.words.tag_config("incorrect_char", background="#B7583D", foreground="white")
        self.position += 1

    def backspace(self):
        # Conditions for backspace: When you typed the first character in a word
        # The second condition accounts for the very first word
        if self.position > self.milestone + 1 or self.position == 1:
            self.position -= 1
            self.words.tag_remove("correct_char", f"1.{self.position}", f"1.{self.position + 1}")
            self.words.tag_remove("incorrect_char", f"1.{self.position}", f"1.{self.position + 1}")

    def check_word(self):
        # Grabs the correct answer
        word_to_check_against = word_list[self.word_number].lower()
        # Grabs the attempt
        input_word = self.typer.get().removeprefix(" ").lower()

        if input_word != word_to_check_against:
            # Removes all highlights of the word attempted, even if they wrote a word longer than it should be
            self.words.tag_remove("correct_char", f"1.{self.position - len(input_word)}", f"1.{self.position}")
            self.words.tag_remove("incorrect_char", f"1.{self.position - len(input_word)}", f"1.{self.position}")

        # Go back one because of the space
        self.position = -1

        # Calculate new position based on how many words have been attempted
        for i in range(self.word_number + 1):
            self.position += len(word_list[i]) + 1

        # self.milestone is purely for the backspace method
        self.milestone = self.position * 1

        if input_word == word_to_check_against:
            # Highlight the correct word blue (by highlighting the characters
            # from beginning of word to current position)
            self.words.tag_add("correct_char", f"1.{self.position - len(word_list[self.word_number])}",
                               f"1.{self.position}")
            self.words.tag_config("correct_char", background="#7C9BE8", foreground="white")
            self.update_score()

        else:
            self.words.tag_add("incorrect_char", f"1.{self.position - len(word_list[self.word_number])}",
                               f"1.{self.position}")
            self.words.tag_config("incorrect_char", background="#B7583D", foreground="white")

        self.words.see(f"1.{self.position + 50}")
        self.typer.delete(0, "end")

        self.word_number += 1

    def update_score(self):
        self.cpm_correct_total += len(word_list[self.word_number])
        self.cpm_score = self.cpm_correct_total / (self.time_limit / 60)
        self.cpm.delete(0, "end")
        self.cpm.insert(0, f"{'{:.1f}'.format(self.cpm_score)}")

        self.wpm_score = self.cpm_score / 5
        self.wpm.delete(0, "end")
        self.wpm.insert(0, f"{'{:.1f}'.format(self.wpm_score)}")

    def save_score(self):
        self.recent_cpm.delete(0, "end")
        self.recent_cpm.insert(0, f"{'{:.1f}'.format(self.cpm_score)}")

        self.recent_wpm.delete(0, "end")
        self.recent_wpm.insert(0, f"{'{:.1f}'.format(self.wpm_score)}")


typing = TypingTest()
root.mainloop()
