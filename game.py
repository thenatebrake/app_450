from collections import Counter, defaultdict


class SpellingGame:

    MIN_WORD_LENGTH = 4

    def __init__(self, letters, center, dictionary):
        self.letters = set(letter.upper() for letter in letters)
        self.center = center.upper()
        self.dictionary = dictionary

    def validate_word(self, word):
        word = word.upper().strip()

        if not word:
            return False, "Enter a word."

        if len(word) < self.MIN_WORD_LENGTH:
            return False, "Words must contain at least 4 letters."

        if self.center not in word:
            return False, f"Word must contain the center letter {self.center}."

        if not set(word).issubset(self.letters):
            return False, "Word contains a letter outside the hive."

        if not self.dictionary.contains(word):
            return False, "That word is not in the dictionary."

        return True, "Valid word!"

    def score_word(self, word):
        word = word.upper()

        if len(word) == 4:
            score = 1
        else:
            score = len(word)

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


def score_word(word, puzzle):
    word = word.upper()

    if len(word) == 4:
        score = 1
    else:
        score = len(word)

    if set(word) == set(puzzle["letters"]):
        score += 7

    return score


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


def is_queen_bee(found_words, valid_words):
    return found_words == valid_words


def word_distribution(valid_words):
    distribution = defaultdict(Counter)

    for word in valid_words:
        first_letter = word[0]
        length = len(word)

        distribution[first_letter][length] += 1

    return distribution


def first_two_combinations(valid_words):
    return Counter(
        word[:2]
        for word in valid_words
        if len(word) >= 2
    )