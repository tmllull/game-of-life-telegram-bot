import ast
import random

import utils.messages as msgs
from database import models
from database.database import SessionLocal
from telegram import Update
from telegram.ext import ContextTypes
from utils import logger as logger
from utils.config import Config
from utils.ecosystem import Ecosystem
from utils.my_utils import MyUtils

utils = MyUtils()
config = Config()
db = SessionLocal()
ecosystem = Ecosystem()


class GameOfLife:
    def __init__(self):
        pass

    async def check_evolution(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.message.from_user.first_name
        if utils.check_valid_chat(update):
            game_of_life = db.query(models.GameOfLife).first()
            if not game_of_life:
                # Check probability to create new ecosystem
                if random.random() < config.NEW_ECOSYSTEM_PROBABILITY:
                    msg = msgs.ECOSYSTEM_CREATED + user
                    logger.info(msg)
                    new_ecosystem = ecosystem.new_ecosystem(user)
                    logger.info(new_ecosystem)
                    game_of_life = models.GameOfLife(
                        id=1, ecosystem=str(new_ecosystem), messages=0, evolutions=0
                    )
                    db.merge(game_of_life)
                    db.commit()
                    await utils.send_message(msg)
                    await utils.send_message(ecosystem.format_ecosystem(new_ecosystem))
            else:
                messages = game_of_life.messages
                current_ecosystem = ast.literal_eval(game_of_life.ecosystem)
                evolutions = game_of_life.evolutions
                probability = messages / 100
                if random.random() < probability:
                    logger.info(msgs.EVOLUTION)
                    messages = 0
                    new_ecosystem = ecosystem.evolution(current_ecosystem, evolutions)
                    logger.info(str(new_ecosystem))
                    ecosystem_died = all(
                        all(elem == " " for elem in sublist)
                        for sublist in new_ecosystem
                    )
                    if ecosystem_died:
                        msg = user + msgs.ECOSYSTEM_DIED
                        logger.info(msg)
                        db.delete(game_of_life)
                        db.commit()
                        await utils.send_message(msg)
                        await utils.send_message(
                            ecosystem.format_ecosystem(ecosystem.died_ecosystem())
                        )
                    else:
                        msg = msgs.EVOLUTION
                        messages += 1
                        evolutions += 1
                        game_of_life = models.GameOfLife(
                            id=1,
                            ecosystem=str(new_ecosystem),
                            messages=messages,
                            evolutions=evolutions,
                        )
                        db.merge(game_of_life)
                        db.commit()
                        await utils.send_message(msg)
                        await utils.send_message(
                            ecosystem.format_ecosystem(new_ecosystem)
                        )
                else:
                    game_of_life = models.GameOfLife(
                        id=1, ecosystem=str(current_ecosystem), messages=messages + 1
                    )
                    db.merge(game_of_life)
                    db.commit()
            pass
