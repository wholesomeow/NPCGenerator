import csv
import random

# Based on the Markov Chain from The Coding Trains YT video
# Future improvements should be based on the advanced MC from RougeBasin
# LINK: http://www.roguebasin.com/index.php?title=Names_from_a_high_order_Markov_Process_and_a_simplified_Katz_back-off_scheme


class MarkovChain:
    def __init__(self):
        self.attempts = 6
        self.order = 1
        self.n_grams = {}
        self.csv = "csv/FantasyNames.csv"
        self.input = self._processCSV()

    def _processCSV(self):
        output = ""
        with open(self.csv, newline='', encoding='utf8') as infile:
            reader = csv.reader(infile)
            i = 0
            for row in reader:
                for cell in row:
                    if cell == '':
                        continue
                    output += f"{cell} "

        for i, v in enumerate(output):
            j = i + self.order
            if v == " ":
                continue

            if v not in self.n_grams:
                self.n_grams[v] = []
            self.n_grams[v].append(output[i + 1])

        return output

    def _getStartPoint(self):
        r = random.randint(0, len(self.input))
        current_gram = self.input[r]
        result = current_gram

        return result, current_gram

    def _makeName(self):
        result, current_gram = self._getStartPoint()

        for i in range(self.attempts):
            try:
                poss = self.n_grams[current_gram]
            except KeyError:
                break
            current_gram = random.choice(poss)
            if i < self.attempts and current_gram == " ":
                break
            result += current_gram

        return result.capitalize()

    def getName(self):
        makeName = True
        while makeName:
            name = self._makeName()

            if len(name) <= 3:
                continue
            else:
                makeName = False

        return name
