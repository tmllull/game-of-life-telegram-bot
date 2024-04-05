import random

import utils.logger as logger
from game_of_life.organisms import Organisms
from utils.config import Config

organisms = Organisms()
flora = organisms.Flora()
fauna = organisms.Fauna()
config = Config()


class Ecosystem:

    def __init__(self) -> None:
        pass

    def new_ecosystem(self, seed=None):
        if seed is None:
            random.seed()
        else:
            random.seed(seed)
        rows = config.ROWS
        columns = config.COLUMNS
        flora_list = flora.get_flora()
        fauna_list = fauna.get_fauna()
        ecosystem = [[" " for _ in range(columns)] for _ in range(rows)]

        # Puts up to three flora organisms
        for _ in range(3):
            x = random.randint(0, rows - 1)
            y = random.randint(0, columns - 1)
            organism = random.choice(flora_list)
            ecosystem[x][y] = organism

        # Puts up to three fauna organisms
        for _ in range(3):
            x = random.randint(0, rows - 1)
            y = random.randint(0, columns - 1)
            organism = random.choice(fauna_list)
            ecosystem[x][y] = organism

        return ecosystem

    def died_ecosystem(self):
        rows = config.ROWS
        columns = config.COLUMNS
        ecosystem = [["☠️" for _ in range(columns)] for _ in range(rows)]

        return ecosystem

    def evolution(self, ecosystem, evolutions):
        rows = len(ecosystem)
        columns = len(ecosystem[0])

        # Create a new empty ecosystem
        new_generation = [[" " for _ in range(columns)] for _ in range(rows)]

        # Probability that ecosystem die by epidemic or something similar,
        # based on basic probability and every evolution add 0.1%
        probability_to_die = config.ECOSYSTEM_PROBABILITY_DIE + evolutions / 1000
        logger.info("Probability that ecosystem die: " + str(probability_to_die))
        if random.random() < probability_to_die:
            logger.info("Ecosystem died because of pandemic or something similar")
            return new_generation, True

        for i in range(rows):  # Ecosystem evolution
            for j in range(columns):
                # Count the number of neighbors that are alive
                neighbors_alive = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        x = (i + dx) % rows
                        y = (j + dy) % columns
                        if (
                            ecosystem[x][y] in flora.get_flora()
                            or ecosystem[x][y] in fauna.get_fauna()
                        ):
                            neighbors_alive += 1

                if ecosystem[i][j] != " ":  # Alive cell. Check if it should die
                    if neighbors_alive < 2 or neighbors_alive > 3:
                        new_generation[i][j] = " "  # Die
                    else:
                        new_generation[i][j] = organisms.evolution(
                            ecosystem[i][j], evolutions
                        )  # Stay (if not die on evolution)
                else:  # Empty cell. Check if it should be born
                    if neighbors_alive == 3:  # New organism born
                        all_organisms = flora.get_flora() + fauna.get_fauna()
                        organism = random.choice(all_organisms)
                        new_generation[i][j] = organism
                    else:  # Stay empty
                        new_generation[i][j] = " "

        # Update the ecosystem
        return new_generation, False

    def format_ecosystem(self, ecosystem):
        msg = ""
        for row in ecosystem:
            msg += " ".join(row) + "\n"
        msg = msg.rstrip("\n")
        return msg
