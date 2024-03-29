import random

from utils.config import Config

config = Config()


class Organisms:
    def __init__(self):
        pass

    def evolution(self, organism, evolutions):
        # Probability that organisms die
        if random.random() < config.ORGANISM_PROBABILITY_DIE + evolutions / 1000:
            return " "
        return organism

    def flora(self):
        return ["🌱", "🌳", "🌻", "🍄", "🌹", "🍀"]

    def fauna(self):
        return ["🐇", "🐦", "🐍", "🦠", "🐜", "🦋"]
