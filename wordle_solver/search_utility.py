from wordle_solver.models import SearchModel

class SearchUtility:
    def __init__(self, five_letter_words: list) -> None:
        self._five_letter_words = five_letter_words
    
    def search(self, search_model: SearchModel) -> "list[str]":
        """Returns a list of matching words"""
        filtered_words = []
        for word in self._five_letter_words:
            is_valid_word = True
            for wrong_letter in search_model.wrong_letters:
                if wrong_letter in word:
                    is_valid_word = False
                    break
            if not is_valid_word:
                continue
            for known_letter in search_model.known_letters:
                letter = known_letter.letter
                if letter not in word:
                    is_valid_word = False
                    break
                indexes_of_letter_in_word = set([index for index in range(len(word)) if word[index] == letter])
                correct_intersections = set(known_letter.known_correct_indices).intersection(indexes_of_letter_in_word)
                incorrect_intersections = set(known_letter.known_incorrect_indices).intersection(indexes_of_letter_in_word)
                if len(correct_intersections) != len(known_letter.known_correct_indices):
                    is_valid_word = False
                    break
                if len(incorrect_intersections) > 0:
                    is_valid_word = False
                    break
            if is_valid_word:
                filtered_words.append(word)
        return filtered_words

    def get_suggested_elimination_word(self, search_model: SearchModel) -> str:
        words_array = self._five_letter_words.copy()
        char_map = SearchUtility.get_ordered_char_map(words_array)
        for known_letter in search_model.known_letters:
            if known_letter.letter in char_map.keys():
                char_map.pop(known_letter.letter)
        for wrong_letter in search_model.wrong_letters:
            if wrong_letter in char_map.keys():
                char_map.pop(wrong_letter)
        target = 5
        while target < len(char_map):
            most_common_chars = set([key for key in char_map][0:target])
            for word in words_array:
                word_set = set(word)

                if len(word_set) == 5 and word_set.issubset(most_common_chars):
                    return word
            target += 1
        return ""

    @staticmethod
    def get_ordered_char_map(words: "list[str]") -> "dict[chr, int]":
        char_dict = {}
        full_string = "".join(words)
        for char in full_string:
            if char in char_dict.keys():
                char_dict[char] += 1
            else:
                char_dict[char] = 1
        return {k: v for k, v in sorted(char_dict.items(), key=lambda item: item[1], reverse=True)}
