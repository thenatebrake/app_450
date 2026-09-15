class SpellingGame:

    MIN_WORD_LENGTH = 4

    def __init__(self, letters, center, dictionary):
        self.letters = set(letters)
        self.center = center.upper()
        self.dictionary = dictionary

    def validate_word(self, word):
        word = word.upper().strip()

        # Empty input
        if not word:
            return False, "Enter a word."

        # Minimum length
        if len(word) < self.MIN_WORD_LENGTH:
            return False, "Words must contain at least 4 letters."

        # Center letter
        if self.center not in word:
            return False, f"Word must contain the center letter {self.center}."

        # Allowed letters
        if not set(word).issubset(self.letters):
            return False, "Word contains a letter outside the hive."

        # Dictionary
        if not self.dictionary.contains(word):
            return False, "That word is not in the dictionary."

        return True, "Valid word!"

    def score_word(self, word):
        word = word.upper()

        if len(word) == 4:
            score = 1
        else:
            score = len(word)

        # Pangram
        if set(word) == self.letters:
            score += 7

        return score