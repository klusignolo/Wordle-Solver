from wordle_solver.app import App
from wordle_solver.utils.file_utils import file_path

def main() -> None:
    filepath = file_path('five_letter_words.txt')
    file = open(filepath)
    five_letter_words_string = file.read().lower()
    words_list = five_letter_words_string.split()
    file.close()

    app = App(words_list)
    app.iconbitmap(file_path("wordle.ico"))
    app.mainloop()

if __name__ == "__main__":
    main()
