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
        if utils.check_valid_chat(update):
            try:
                user_id = update.message.from_user.id
                user_first_name = update.message.from_user.first_name
                username = update.message.from_user.username
                message = update.message.text
                user_db = (
                    db.query(models.User).filter(models.User.id == user_id).first()
                )
                if not user_db:
                    new_user = models.User(
                        id=user_id,
                        ecosystems_created=0,
                        ecosystems_killed=0,
                        ecosystems_evolved=0,
                    )
                    db.merge(new_user)
                    db.commit()
                    # db.refresh(new_user)
                game_of_life = db.query(models.GameOfLife).first()
                user_db = (
                    db.query(models.User).filter(models.User.id == user_id).first()
                )
                if not game_of_life:
                    # Check probability to create new ecosystem
                    if random.random() < config.NEW_ECOSYSTEM_PROBABILITY:
                        msg = msgs.ECOSYSTEM_CREATED + user_first_name
                        logger.info(msg)
                        new_ecosystem = ecosystem.new_ecosystem(username + str(message))
                        logger.info(new_ecosystem)
                        game_of_life = models.GameOfLife(
                            id=1, ecosystem=str(new_ecosystem), messages=0, evolutions=0
                        )
                        update_user = models.User(
                            id=user_id,
                            ecosystems_created=user_db.ecosystems_created + 1,
                        )
                        db.merge(game_of_life)
                        db.commit()
                        db.merge(update_user)
                        db.commit()
                        await utils.send_message(msg)
                        await utils.send_message(
                            ecosystem.format_ecosystem(new_ecosystem)
                        )
                else:
                    messages = game_of_life.messages
                    current_ecosystem = ast.literal_eval(game_of_life.ecosystem)
                    evolutions = game_of_life.evolutions
                    probability = messages * config.PROBABILITY_EVOLVE_PER_MESSAGE / 100
                    if random.random() < probability:
                        logger.info(msgs.EVOLUTION)
                        messages = 0
                        new_ecosystem = ecosystem.evolution(
                            current_ecosystem, evolutions
                        )
                        logger.info(str(new_ecosystem))
                        ecosystem_died = all(
                            all(elem == " " for elem in sublist)
                            for sublist in new_ecosystem
                        )
                        if ecosystem_died:
                            msg = user_first_name + msgs.ECOSYSTEM_KILLED
                            logger.info(msg)
                            update_user = models.User(
                                id=user_id,
                                ecosystems_killed=user_db.ecosystems_killed + 1,
                            )
                            db.delete(game_of_life)
                            db.commit()
                            db.merge(update_user)
                            db.commit()
                            await utils.send_message(msg)
                            await utils.send_message(
                                ecosystem.format_ecosystem(ecosystem.died_ecosystem())
                            )
                        else:
                            msg = msgs.EVOLUTION
                            logger.info(msg)
                            evolutions += 1
                            game_of_life = models.GameOfLife(
                                id=1,
                                ecosystem=str(new_ecosystem),
                                messages=0,
                                evolutions=evolutions,
                            )
                            update_user = models.User(
                                id=user_id,
                                ecosystems_evolved=user_db.ecosystems_evolved + 1,
                            )
                            db.merge(game_of_life)
                            db.commit()
                            db.merge(update_user)
                            db.commit()
                            await utils.send_message(msg)
                            await utils.send_message(
                                ecosystem.format_ecosystem(new_ecosystem)
                            )
                    else:
                        game_of_life = models.GameOfLife(
                            id=1,
                            ecosystem=str(current_ecosystem),
                            messages=messages + 1,
                        )
                        db.merge(game_of_life)
                        db.commit()
                db.commit()
                db.close()
            except Exception as e:
                db.close()
                logger.error(e)
