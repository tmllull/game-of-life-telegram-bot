import datetime
import os

import telegram
import tiktoken
import utils.logger as logger
from clients.ai_controller import AIController
from database.database import SessionLocal
from dotenv import dotenv_values
from telegram import Bot, Update
from utils.config import Config

config = Config()
ai_controller = AIController()
db = SessionLocal()


class MyUtils:
    """_summary_"""

    def __init__(self):
        pass
        self.bot = Bot(config.TELEGRAM_TOKEN)
        # if config.AI_SERVICE == "openai":
        #     self._ai_service = open_ai
        # elif config.AI_SERVICE == "azure":
        #     self._ai_service = azure_openai
        # else:
        #     self._ai_service = None
        # self.chat_id = self.TELEGRAM_CHAT_ID

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

    async def send_message(self, msg=None, pre_prompt=None, prompt=None):
        if pre_prompt and prompt is not None and ai_controller.has_service:
            try:
                msg = ai_controller.generate_text(pre_prompt, prompt)
            except Exception as e:
                logger.info(e)
                msg = msg

        async with self.bot:
            # msg = self.format_text_for_md2(msg)
            await self.bot.send_message(
                chat_id=config.TELEGRAM_CHAT_ID,
                text=msg,
                parse_mode=telegram.constants.ParseMode.MARKDOWN_V2,
            )

    def get_date(self) -> datetime.date:
        return datetime.datetime.now().date()

    def num_tokens_from_messages(self, messages, model):
        """Return the number of tokens used by a list of messages."""
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            print("Warning: model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")
        if model in {
            "gpt-3.5-turbo-0613",
            "gpt-3.5-turbo-16k-0613",
            "gpt-4-0314",
            "gpt-4-32k-0314",
            "gpt-4-0613",
            "gpt-4-32k-0613",
        }:
            tokens_per_message = 3
            tokens_per_name = 1
        elif model == "gpt-3.5-turbo-0301":
            tokens_per_message = (
                4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
            )
            tokens_per_name = -1  # if there's a name, the role is omitted
        elif "gpt-3.5-turbo" in model:
            print(
                "Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613."
            )
            return self.num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
        elif "gpt-4" in model:
            print(
                "Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613."
            )
            return self.num_tokens_from_messages(messages, model="gpt-4-0613")
        else:
            raise NotImplementedError(
                f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
            )
        num_tokens = 0
        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
        return num_tokens
