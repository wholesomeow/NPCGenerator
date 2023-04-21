import csv
import random

# Based on the Markov Chain from The Coding Trains YT video
# Future improvements should be based on the advanced MC from RougeBasin
# LINK: http://www.roguebasin.com/index.php?title=Names_from_a_high_order_Markov_Process_and_a_simplified_Katz_back-off_scheme


class MarkovChain:
    def __init__(self, csv_path="csv/FantasyNames.csv", max_attempts=6):
        # General amount of times to match characters for the name
        self.attempts = max_attempts
        self.n_grams = {}
        self.csv = csv_path
        self.vowels = ["a", "e", "i", "o", "u"]
        self.accepted_bigrams = set(['br', 'dr', 'fr', 'gr', 'kr', 'pr', 'tr', 'cr', 'sn', 'sw', 'th',
                                     'sh', 'ch', 'cl', 'sl', 'sm', 'sn', 'sp', 'st', 'sk', 'bl', 'fl',
                                     'gl', 'pl', 'sl', 'll', 'yl', 'yv', 'gh'])
        self.n_grams = self._buildNGram(csv_path)

    def _buildNGram(self, csv_path):
        with open(csv_path, newline='', encoding='utf8') as infile:
            input = " ".join(cell for row in csv.reader(infile)
                             for cell in row if cell)
        n_grams = {}

        for i, val in enumerate(input):
            if i == len(input) - 1:
                break
            elif val == " ":  # Checks if data from output is a space between the names or not
                continue

            if val not in n_grams and val != ' ':
                n_grams[val] = []
            n_grams[val].append(input[i + 1])

        return n_grams

    def _getStartPoint(self):
        current_gram = random.choice(list(self.n_grams.keys()))
        return current_gram, current_gram

    def _makeName(self):
        result, current_gram = self._getStartPoint()  # What a clever trick

        for i in range(self.attempts):
            try:
                poss = self.n_grams[current_gram]
            except KeyError:
                break
            current_gram = random.choice(poss)
            if i < self.attempts and current_gram == " ":
                break
            result += current_gram

        return result.strip()  # Just incase

    def _checkQuality(self, name):
        if len(name) <= 3:
            return False

        # letters = [x for x in name]
        for letter in range(len(name) - 1):
            bigram = name[letter:letter + 2].lower()
            if bigram[0] in self.vowels or bigram[1] in self.vowels:
                continue
            elif bigram not in self.accepted_bigrams:
                return False

        return True

    def getName(self):
        # Build the name and then check name meets quality requirements
        make_name = True
        while make_name:
            name = self._makeName()

            if self._checkQuality(name):
                return name.capitalize()


# NOTE: For testing the name creation functionality
# (Comment out when not working on the generator)
# for i in range(10):
#     new_name = MarkovChain().getName()
#     print(new_name)
