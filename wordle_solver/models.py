from dataclasses import dataclass

@dataclass
class KnownLetter:
    letter: chr
    known_correct_indices: "list[int]"
    known_incorrect_indices: "list[int]"
    def __init__(self, letter: str, known_correct_indices: "list[int]", known_incorrect_indices: "list[int]") -> None:
        self.letter = letter
        self.known_correct_indices = known_correct_indices
        self.known_correct_indices.sort()
        self.known_incorrect_indices = known_incorrect_indices
        self.known_incorrect_indices.sort()

@dataclass
class SearchModel:
    known_letters: "list[KnownLetter]"
    wrong_letters: "list[chr]"
