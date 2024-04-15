import random

import utils.logger as logger
from utils.config import Config

config = Config()


import random


class Organisms:
    def __init__(self):
        pass

    def evolution(self, organism, evolutions, neighbors):
        # Probability that organisms die
        current_probability_to_die = config.ORG_PROB_DIE * evolutions
        # Check if organisms is devored by neighbors
        if self.is_devoured(organism, neighbors):
            logger.info("Organism " + organism + " devoured by " + str(neighbors))
            return " "
        if random.random() < current_probability_to_die:
            logger.info(
                "Organism "
                + organism
                + " died accidentally ("
                + str(current_probability_to_die)
                + ")"
            )
            return " "
        return organism

    def get_organism_type(self, organism):
        if organism in self.Flora().get_organisms():
            return self.Flora
        if organism in self.Fauna().TrophicLevel2().get_organisms():
            return self.Fauna.TrophicLevel2
        if organism in self.Fauna.TrophicLevel3().get_organisms():
            return self.Fauna.TrophicLevel3
        if organism in self.Fauna.TrophicLevel4().get_organisms():
            return self.Fauna.TrophicLevel4

    def get_survival(self, organism):
        if organism in self.Flora().get_organisms():
            return self.Flora().survival
        if organism in self.Fauna().TrophicLevel1().get_organisms():
            return self.Fauna.TrophicLevel1().survival
        if organism in self.Fauna().TrophicLevel2().get_organisms():
            return self.Fauna.TrophicLevel2().survival
        if organism in self.Fauna.TrophicLevel3().get_organisms():
            return self.Fauna.TrophicLevel3().survival
        if organism in self.Fauna.TrophicLevel4().get_organisms():
            return self.Fauna.TrophicLevel4().survival

    def is_devoured(self, organism, neighbors):
        organism_survival = self.get_survival(organism)
        neighbors_survival = 0
        for neighbor in neighbors:
            if organism_survival <= self.get_survival(neighbor):
                neighbors_survival += self.get_survival(neighbor)
        if neighbors_survival != 0:
            neighbors_survival = neighbors_survival / len(neighbors)
            survival_probability = (
                (organism_survival * 100) / neighbors_survival
            ) / 100
        else:
            survival_probability = 1
        logger.info(
            organism
            + " ("
            + str(organism_survival * len(neighbors))
            + ")"
            + " vs "
            + str(neighbors)
            + " ("
            + str(neighbors_survival)
            + ") => "
            + str(survival_probability)
        )
        if random.random() > survival_probability:
            return True
        return False

    class Flora:
        def __init__(self):
            self.survival = 1
            self.organisms = [
                "🌱",
                "🌳",
                "🌻",
                "🍄",
                "🌹",
                "🍀",
                "🌺",
                "🌷",
                "🌸",
                "🌼",
                "🌾",
                "🎍",
                "🌴",
                "🌵",
                "🌲",
                "🌰",
            ]

        def get_organisms(self):
            return self.organisms

    class Fauna:
        def __init__(self):
            pass

        def get_organisms(self):
            return (
                self.TrophicLevel1().get_organisms()
                + self.TrophicLevel2().get_organisms()
                + self.TrophicLevel3().get_organisms()
                + self.TrophicLevel4().get_organisms()
            )

        class TrophicLevel1:
            def __init__(self):
                super().__init__()
                self.survival = 1
                self.organisms = [
                    "🐞",
                    "🐛",
                    "🦗",
                    "🐜",
                    "🦟",
                    "🐝",
                    "🦋",
                    "🪰",
                    "🐌",
                    "🪲",
                ]

            def get_organisms(self):
                return self.organisms

        class TrophicLevel2:
            def __init__(self):
                # super().__init__()
                self.survival = 2
                self.organisms = [
                    "🐰",
                    "🦌",
                    "🐄",
                    "🐿️",
                    "🦡",
                    "🦔",
                    "🦙",
                    "🐫",
                    "🦘",
                    "🐏",
                    "🐐",
                    "🐦",
                    "🦜",
                    "🐤",
                    "🐦",
                ]

            def get_organisms(self):
                return self.organisms

        class TrophicLevel3:
            def __init__(self):
                # super().__init__()
                self.survival = 3
                self.organisms = [
                    "🐷",
                    "🐒",
                    "🦝",
                    "🐴",
                    "🐖",
                    "🦓",
                    "🦒",
                    "🦥",
                    "🦦",
                    "🦊",
                    "🐘",
                ]

            def get_organisms(self):
                return self.organisms

        class TrophicLevel4:
            def __init__(self):
                # super().__init__()
                self.survival = 4
                self.organisms = [
                    "🐺",
                    "🦁",
                    "🐅",
                    "🐆",
                    "🐊",
                    "🐻",
                    "🐯",
                    "🐍",
                    "🦍",
                    "🐗",
                    "🦛",
                    "🐃",
                    "🦏",
                ]

            def get_organisms(self):
                return self.organisms
