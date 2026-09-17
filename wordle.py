import os
import sys

# next to this file, or the temporary folder PyInstaller unpacks the .exe into
BASE_DIR = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))


def load(name):
    with open(os.path.join(BASE_DIR, name)) as f:
        return f.read().split()

# words that can be the answer of the day, and words Wordle only accepts as a guess
ANSWERS = load("words_answers.txt")
GUESSES = load("words_guesses.txt")

# count code from the GUI -> check how often a yellow letter appears in the word
COUNT_CHECKS = {
    ">0": lambda n: n >= 1,
    "=1": lambda n: n == 1,
    ">1": lambda n: n >= 2,
    "=2": lambda n: n == 2,
    ">2": lambda n: n >= 3,
    "=3": lambda n: n == 3,
}


def extract(gui_data):
    green = gui_data["green"]
    yellow = gui_data["yellow"]

    # letters allowed at positions without a green letter
    letters = set(gui_data["available_letters"]) | set(green) | {ch for col in yellow for ch in col}
    for ch, can_repeat in zip(green, gui_data["green_more_than_once"]):
        if ch and not can_repeat:
            letters.discard(ch)

    # yellow letter -> count check (a later field for the same letter wins)
    counts = {}
    for col, amounts in zip(yellow, gui_data["yellow_more_than_once"]):
        for ch, amount in zip(col, amounts):
            if ch:
                counts[ch] = COUNT_CHECKS[amount]

    def matches(word):
        for pos, ch in enumerate(word):
            if green[pos]:
                if ch != green[pos]:
                    return False
            elif ch not in letters or ch in yellow[pos]:
                return False
        # every yellow letter has to appear the given number of times
        return all(check(word.count(ch)) for ch, check in counts.items())

    def hits(words):
        # most distinct letters first, they reveal the most information
        return sorted((w for w in words if matches(w)), key=lambda w: len(set(w)), reverse=True)

    return hits(ANSWERS), hits(GUESSES)
