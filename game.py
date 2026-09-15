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
def generate_valid_words(words, letters, center):
    letters = set(letter.upper() for letter in letters)
    center = center.upper()

    valid_words = set()

    for word in words:
        word = word.strip().upper()

        if len(word) < 4:
            continue

        if center not in word:
            continue

        if not set(word).issubset(letters):
            continue

        valid_words.add(word)

    return valid_words

def get_level(score, max_score):
    if max_score == 0:
        return "Beginner"

    percentage = score / max_score

    if percentage >= 1.0:
        return "Queen Bee"
    elif percentage >= 0.80:
        return "Genius"
    elif percentage >= 0.65:
        return "Amazing"
    elif percentage >= 0.50:
        return "Great"
    elif percentage >= 0.35:
        return "Good"
    elif percentage >= 0.20:
        return "Moving Up"
    elif percentage >= 0.10:
        return "Good Start"
    else:
        return "Beginner"   