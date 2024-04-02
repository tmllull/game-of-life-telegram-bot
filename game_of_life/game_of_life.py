import ast
import random

import utils.messages as msgs
from database import models
from database.database import SessionLocal
from game_of_life.ecosystem import Ecosystem
from sqlalchemy import func
from telegram import Update
from telegram.ext import ContextTypes
from utils import logger as logger
from utils.config import Config
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
                user_db = (
                    db.query(models.User).filter(models.User.id == user_id).first()
                )
                ecosystems_db = db.query(func.count(models.Ecosystem.id)).scalar()
                ecosystem_died = (
                    db.query(models.Ecosystem)
                    .filter(
                        models.Ecosystem.born_date != None,
                        models.Ecosystem.extinction_date != None,
                    )
                    .first()
                )
                ecosystem_alive = (
                    db.query(models.Ecosystem)
                    .filter(
                        models.Ecosystem.born_date != None,
                        models.Ecosystem.extinction_date == None,
                    )
                    .first()
                )
                if ecosystem_died or ecosystems_db == 0:
                    # Check probability to create new ecosystem
                    if random.random() < config.NEW_ECOSYSTEM_PROBABILITY:
                        msg = msgs.ECOSYSTEM_CREATED + user_first_name
                        logger.info(msg)
                        new_ecosystem = ecosystem.new_ecosystem(username + str(message))
                        logger.info(new_ecosystem)
                        ecosystem_to_add = models.Ecosystem(
                            ecosystem=str(new_ecosystem),
                            messages=0,
                            evolutions=0,
                            born_date=utils.get_date(),
                        )
                        update_user = models.User(
                            id=user_id,
                            ecosystems_created=user_db.ecosystems_created + 1,
                        )
                        db.merge(ecosystem_to_add)
                        # db.commit()
                        db.merge(update_user)
                        # db.commit()
                        await utils.send_message(msg)
                        await utils.send_message(
                            ecosystem.format_ecosystem(new_ecosystem)
                        )
                else:
                    ecosystem_id = ecosystem_alive.id
                    messages = ecosystem_alive.messages
                    current_ecosystem = ast.literal_eval(ecosystem_alive.ecosystem)
                    evolutions = ecosystem_alive.evolutions
                    probability = messages * config.PROBABILITY_PER_MESSAGE
                    logger.info("Probability: " + str(probability))
                    if random.random() < probability:
                        logger.info(msgs.EVOLUTION)
                        new_ecosystem, died_by_epidemic = ecosystem.evolution(
                            current_ecosystem, evolutions
                        )
                        logger.info(str(new_ecosystem))
                        ecosystem_died = all(
                            all(elem == " " for elem in sublist)
                            for sublist in new_ecosystem
                        )
                        if ecosystem_died:
                            msg = user_first_name + msgs.ECOSYSTEM_KILLED
                            if died_by_epidemic:
                                msg += msgs.EPIDEMIC
                            logger.info(msg)
                            update_user = models.User(
                                id=user_id,
                                ecosystems_killed=user_db.ecosystems_killed + 1,
                            )
                            died_ecosystem = models.Ecosystem(
                                id=ecosystem_id,
                                messages=messages + 1,
                                extinction_date=utils.get_date(),
                            )
                            db.merge(died_ecosystem)
                            # db.commit()
                            db.merge(update_user)
                            # db.commit()
                            await utils.send_message(msg)
                            await utils.send_message(
                                ecosystem.format_ecosystem(ecosystem.died_ecosystem())
                            )
                        else:
                            msg = msgs.EVOLUTION
                            logger.info(msg)
                            evolutions += 1
                            ecosystem_alive = models.Ecosystem(
                                id=ecosystem_id,
                                ecosystem=str(new_ecosystem),
                                messages=0,
                                evolutions=evolutions,
                            )
                            update_user = models.User(
                                id=user_id,
                                ecosystems_evolved=user_db.ecosystems_evolved + 1,
                            )
                            db.merge(ecosystem_alive)
                            # db.commit()
                            db.merge(update_user)
                            # db.commit()
                            await utils.send_message(msg)
                            await utils.send_message(
                                ecosystem.format_ecosystem(new_ecosystem)
                            )
                    else:
                        ecosystem_alive = models.Ecosystem(
                            id=ecosystem_id,
                            # ecosystem=str(current_ecosystem),
                            messages=messages + 1,
                        )
                        db.merge(ecosystem_alive)
                        # db.commit()
                db.commit()
                db.close()
            except Exception as e:
                db.close()
                logger.error(e)
