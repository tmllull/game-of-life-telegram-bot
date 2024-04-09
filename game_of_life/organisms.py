import random

import utils.logger as logger
from utils.config import Config

config = Config()


class Organisms:
    def __init__(self):
        pass

    def evolution(self, organism, evolutions):
        # Probability that organisms die
        current_probability_to_die = config.ORG_PROB_DIE * evolutions
        # logger.info("Organism probability to die: " + str(current_probability_to_die))
        if random.random() < current_probability_to_die:
            return " "
        return organism

    class Flora:
        def __init__(self):
            pass

        def get_flora(self):
            return ["🌱", "🌳", "🌻", "🍄", "🌹", "🍀"]

    class Fauna:
        def __init__(self):
            pass

        def get_fauna(self):
            return ["🐇", "🐦", "🐍", "🦠", "🐜", "🦋"]
