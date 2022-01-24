import tkinter as tk
from tkinter.ttk import Separator
from wordle_solver.models import KnownLetter, SearchModel
from wordle_solver.search_utility import SearchUtility
from wordle_solver.utils.tkinter_utils import update_widget_text

class KnownLetterFrame(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master=master)
        self.letter_lbl = tk.Label(self, text="Character:")
        self.correct_indices_lbl = tk.Label(self, text="Indices In Word:")
        self.incorrect_indices_lbl = tk.Label(self, text="Indices Not In Word:")

        self.letter_entry = tk.Entry(self, width=10)
        self.correct_indices_entry = tk.Entry(self, width=10)
        self.incorrect_indices_entry = tk.Entry(self, width=10)

        self.letter_lbl.grid(row=0, column=0, sticky='e')
        self.letter_entry.grid(row=0, column=1, sticky='w')
        self.correct_indices_lbl.grid(row=1, column=0, sticky='e')
        self.correct_indices_entry.grid(row=1, column=1, sticky='w')
        self.incorrect_indices_lbl.grid(row=2, column=0, sticky='e')
        self.incorrect_indices_entry.grid(row=2, column=1, sticky='w')

    def error_text(self) -> str:
        if self.letter_entry.get() != '':
            if self.correct_indices_entry.get() == '' and self.incorrect_indices_entry.get() == '':
                return "Must indicate indices of " + self.letter_entry.get()
        if self.correct_indices_entry.get() != '':
            if self.letter_entry.get() == '':
                return "Must indicate letter for indices " + self.correct_indices_entry.get()
        if self.incorrect_indices_entry.get() != '':
            if self.letter_entry.get() == '':
                return "Must indicate letter for indices " + self.incorrect_indices_entry.get()
        return ""

    def validate(self) -> bool:
        return self.error_text() == ""

    def has_letter(self):
        return self.letter_entry.get() != "" and self.correct_indices_entry.get() != "" and self.incorrect_indices_entry.get() != ""

    def get_known_letter_object(self) -> KnownLetter:
        character = self.letter_entry.get().lower()
        correct_indices = [int(x) for x in self.correct_indices_entry.get().replace(' ', '').split(',') if x.isnumeric()]
        incorrect_indices = [int(x) for x in self.incorrect_indices_entry.get().replace(' ', '').split(',') if x.isnumeric()]
        return KnownLetter(character, correct_indices, incorrect_indices)

class MainFrame(tk.Frame):
    known_letter_frames: "list[KnownLetterFrame]"
    search_utility: SearchUtility
    def __init__(self, master, search_utility: SearchUtility):
        tk.Frame.__init__(self, master=master)
        self.search_utility = search_utility
        wrong_letters_lbl = tk.Label(self, text="Wrong Character(s):")
        known_lbl = tk.Label(self, text="Known Character(s):")

        known_letter_1 = KnownLetterFrame(self)
        known_letter_2 = KnownLetterFrame(self)
        known_letter_3 = KnownLetterFrame(self)
        known_letter_4 = KnownLetterFrame(self)
        known_letter_5 = KnownLetterFrame(self)
        self.known_letter_frames = [known_letter_1, known_letter_2, known_letter_3, known_letter_4, known_letter_5]

        self.wrong_letters_entry = tk.Entry(self, width=10)
        self.output_text_widget = tk.Text(self, width=45, state='disabled')

        wrong_letters_lbl.grid(row=0, column=1)
        self.wrong_letters_entry.grid(row=0, column=2, pady=5)
        Separator(self, orient="horizontal").grid(row=1, column=1, columnspan=2, sticky="ew", padx=2)
        known_lbl.grid(row=2, column=1)

        known_letter_1.grid(row=4, column=1, columnspan=2, rowspan=2, padx=5)
        known_letter_2.grid(row=6, column=1, columnspan=2, rowspan=2, padx=5, pady=5)
        known_letter_3.grid(row=8, column=1, columnspan=2, rowspan=2, padx=5, pady=5)
        known_letter_4.grid(row=10, column=1, columnspan=2, rowspan=2, padx=5, pady=5)
        known_letter_5.grid(row=12, column=1, columnspan=2, rowspan=2, padx=5, pady=5)

        self.search_btn = tk.Button(self, width=35, text="Search", command=self.search)

        self.search_btn.grid(row=14, column=0, columnspan=3, padx=10, pady=5)
        self.output_text_widget.grid(row=0, column=0, rowspan=14, padx=5, pady=5)

        self.wrong_letters_entry.focus()
        
        instructions = "Welcome to Wordle Solver!\n" + \
            "Yes. This is cheating.\n\n" + \
            "Enter any search criteria on the right.\n" + \
            "Then click Search to list possibilities.\n" + \
            "Separate indices with a comma.\n" + \
            "Indices are zero-based."
        update_widget_text(self.output_text_widget, instructions)

    def search(self):
        if not self.validate_input():
            return
        wrong_letters = [char for char in self.wrong_letters_entry.get().lower()]
        known_letters = [x.get_known_letter_object() for x in self.known_letter_frames if x.letter_entry.get() != '']
        search_model = SearchModel(known_letters, wrong_letters)
        word_list: list[str] = self.search_utility.search(search_model)
        suggested_word = self.search_utility.get_suggested_elimination_word(search_model)

        output = ""
        if len(word_list) > 0:
            output = f"Suggested Elimination Word: {suggested_word}\n"
            output += f"Possible Words ({str(len(word_list))}):\n" + "\n".join(word_list)
        else:
            output = "Results: None"
        update_widget_text(self.output_text_widget, output)

    def validate_input(self):
        for known_letter_frame in self.known_letter_frames:
            if not known_letter_frame.validate():
                update_widget_text(self.output_text_widget, known_letter_frame.error_text())
                return False
        return True
