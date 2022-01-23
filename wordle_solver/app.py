import tkinter as tk
from wordle_solver.view import MainFrame
from wordle_solver.search_utility import SearchUtility

class App(tk.Tk):
    def __init__(self, words_list: "list[str]", *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Wordle Solver v1.0")

        search_utility = SearchUtility(words_list)

        MainFrame(self, search_utility).grid()