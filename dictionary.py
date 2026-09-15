from pathlib import Path


class Dictionary:

    def __init__(self, filename="english3.txt"):
        self.words = set()

        path = Path(filename)

        if path.exists():
            with open(path, "r", encoding="utf-8") as file:
                for line in file:
                    word = line.strip().upper()

                    if word:
                        self.words.add(word)

    def contains(self, word):
        return word.upper() in self.words