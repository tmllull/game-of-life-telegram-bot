import datetime
import os

import telegram
import utils.logger as logger
from database.database import SessionLocal
from dotenv import dotenv_values
from telegram import Bot, Update
from utils.config import Config

config = Config()

db = SessionLocal()


class MyUtils:
    """_summary_"""

    def __init__(self):
        try:
            self.TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
            self.TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
            self.TELEGRAM_ADMIN_CHAT_ID = os.environ["TELEGRAM_ADMIN_CHAT_ID"]

        except Exception:
            # Load .env
            config = dotenv_values(".env")
            self.TELEGRAM_TOKEN = config["TELEGRAM_TOKEN"]
            self.TELEGRAM_CHAT_ID = config["TELEGRAM_CHAT_ID"]
            self.TELEGRAM_ADMIN_CHAT_ID = config["TELEGRAM_ADMIN_CHAT_ID"]
        self.bot = Bot(self.TELEGRAM_TOKEN)
        self.chat_id = self.TELEGRAM_CHAT_ID

    def check_valid_chat(self, update: Update) -> bool:
        try:
            username = update.message.from_user.username
            user_id = update.message.from_user.id
            chat_id = update.message.chat_id
            if chat_id < 0:
                if chat_id != int(config.TELEGRAM_CHAT_ID):
                    return False
                return True
            return False
        except Exception as e:
            logger.info("Error checking valid chat: " + str(e))

    async def send_message(self, msg):
        async with self.bot:
            # msg = self.format_text_for_md2(msg)
            await self.bot.send_message(
                chat_id=config.TELEGRAM_CHAT_ID,
                text=msg,
                parse_mode=telegram.constants.ParseMode.MARKDOWN_V2,
            )

    def get_date(self) -> datetime.date:
        return datetime.datetime.now().date()
