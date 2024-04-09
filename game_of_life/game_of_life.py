import ast
import random

import utils.messages as msgs
import utils.prompts as prompts
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
        logger.info("Starting game of life...")

    async def check_evolution(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not utils.check_valid_chat(update):
            logger.info("Invalid chat")
            return

        try:
            user_id, user_first_name, username, message = self.extract_user_info(
                update.message
            )
            user_db = self.get_user_from_db(user_id)
            ecosystems_db = self.get_ecosystems_count()
            ecosystem_alive = self.get_alive_ecosystem()

            if ecosystem_alive is None or ecosystems_db == 0:
                await self.handle_new_ecosystem(user_id, user_db, username, message)
            else:
                await self.handle_ecosystem_evolution(
                    username, user_id, user_db, ecosystem_alive
                )
            db.commit()
            db.close()

        except Exception as e:
            db.close()
            logger.error(e)

    def extract_user_info(self, message):
        return (
            message.from_user.id,
            message.from_user.first_name,
            message.from_user.username,
            message.text,
        )

    def get_user_from_db(self, user_id):
        user_db = db.query(models.User).filter(models.User.id == user_id).first()
        if not user_db:
            new_user = models.User(
                id=user_id,
                ecosystems_created=0,
                ecosystems_killed=0,
                ecosystems_evolved=0,
            )
            db.merge(new_user)
            db.commit()
            user_db = db.query(models.User).filter(models.User.id == user_id).first()
        return user_db

    def get_ecosystems_count(self):
        return db.query(func.count(models.Ecosystem.id)).scalar()

    def get_alive_ecosystem(self):
        return (
            db.query(models.Ecosystem)
            .filter(
                models.Ecosystem.born_date != None,
                models.Ecosystem.extinction_date == None,
            )
            .first()
        )

    async def handle_new_ecosystem(self, user_id, user_db, username, message):
        if random.random() < config.NEW_ECO_PROB:
            await self.create_new_ecosystem(user_id, user_db, username, message)

    async def handle_ecosystem_evolution(
        self, username, user_id, user_db, ecosystem_alive
    ):
        ecosystem_id = ecosystem_alive.id
        messages = ecosystem_alive.messages
        current_ecosystem = ast.literal_eval(ecosystem_alive.ecosystem)
        evolutions = ecosystem_alive.evolutions
        probability = messages * config.PROB_PER_MESSAGE

        if random.random() < probability:
            new_ecosystem, died_by_epidemic = ecosystem.evolution(
                current_ecosystem, evolutions
            )
            logger.info(new_ecosystem)
            ecosystem_died = all(
                all(elem == " " for elem in sublist) for sublist in new_ecosystem
            )
            if ecosystem_died:
                await self.kill_ecosystem(
                    user_id,
                    user_db,
                    ecosystem_id,
                    died_by_epidemic,
                    messages,
                    username,
                )
            else:
                await self.evolution(
                    user_id,
                    user_db,
                    ecosystem_id,
                    new_ecosystem,
                    evolutions,
                )
        else:
            ecosystem_alive.messages += 1
            db.merge(ecosystem_alive)

    async def create_new_ecosystem(self, user_id, user_db, username: str, message: str):
        logger.info("Creating new ecosystem...")
        msg = msgs.ECOSYSTEM_CREATED
        logger.info(msg)
        new_ecosystem = ecosystem.new_ecosystem(username + str(message))
        logger.info(new_ecosystem)
        ecosystem_to_add = models.Ecosystem(
            ecosystem=str(new_ecosystem),
            messages=0,
            evolutions=0,
            born_date=utils.get_date(),
            creator=username,
        )
        update_user = models.User(
            id=user_id,
            ecosystems_created=user_db.ecosystems_created + 1,
        )
        db.merge(ecosystem_to_add)
        # db.commit()
        db.merge(update_user)
        # db.commit()
        await utils.send_message(
            msg,
            pre_prompt=prompts.INSTRUCTION,
            prompt=prompts.ECOSYSTEM_BORN,
        )
        await utils.send_message(ecosystem.format_ecosystem(new_ecosystem))

    async def kill_ecosystem(
        self, user_id, user_db, ecosystem_id, died_by_epidemic, messages, username
    ):
        prompt = prompts.ECOSYSTEM_DIE
        if died_by_epidemic:
            msg = msgs.EPIDEMIC
            prompt = prompts.ECOSYSTEM_DIE_EPIDEMIC
        else:
            msg = msgs.ECOSYSTEM_DIED
        logger.info(msg)
        update_user = models.User(
            id=user_id,
            ecosystems_killed=user_db.ecosystems_killed + 1,
        )
        died_ecosystem = models.Ecosystem(
            id=ecosystem_id,
            messages=messages + 1,
            extinction_date=utils.get_date(),
            killer=username,
        )
        db.merge(died_ecosystem)
        # db.commit()
        db.merge(update_user)
        # db.commit()
        await utils.send_message(
            msg,
            pre_prompt=prompts.INSTRUCTION,
            prompt=prompt,
        )
        await utils.send_message(ecosystem.format_ecosystem(ecosystem.died_ecosystem()))

    async def evolution(
        self, user_id, user_db, ecosystem_id, new_ecosystem, evolutions
    ):
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
        await utils.send_message(
            msg,
            pre_prompt=prompts.INSTRUCTION,
            prompt=prompts.ECOSYSTEM_EVOLUTION,
        )
        await utils.send_message(ecosystem.format_ecosystem(new_ecosystem))
