import os

from dotenv import dotenv_values


class Config:
    def __init__(self):
        try:
            # Load .env
            config = dotenv_values(".env")
            self.TELEGRAM_TOKEN = config.get(
                "TELEGRAM_TOKEN", os.environ.get("TELEGRAM_TOKEN")
            )
            self.TELEGRAM_CHAT_ID = config.get(
                "TELEGRAM_CHAT_ID", os.environ.get("TELEGRAM_CHAT_ID")
            )
            self.TELEGRAM_ADMIN_CHAT_ID = config.get(
                "TELEGRAM_ADMIN_CHAT_ID", os.environ.get("TELEGRAM_ADMIN_CHAT_ID")
            )
            self.AI_SERVICE = config.get("AI_SERVICE", os.environ.get("AI_SERVICE"))
            self.OPENAI_API_KEY = config.get(
                "OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY")
            )
            self.OPENAI_MODEL = config.get(
                "OPENAI_MODEL", os.environ.get("OPENAI_MODEL")
            )
            self.AZURE_API_KEY = config.get(
                "AZURE_API_KEY", os.environ.get("AZURE_API_KEY")
            )
            self.AZURE_API_ENDPOINT = config.get(
                "AZURE_API_ENDPOINT", os.environ.get("AZURE_API_ENDPOINT")
            )
            self.AZURE_API_VERSION = config.get(
                "AZURE_API_VERSION", os.environ.get("AZURE_API_VERSION")
            )
            self.AZURE_MODEL_NAME = config.get(
                "AZURE_MODEL_NAME", os.environ.get("AZURE_MODEL_NAME")
            )
            self.ROWS = 5
            self.COLUMNS = 5
            self.PROBABILITY_PER_MESSAGE = 0.1  # 1%
            self.NEW_ECOSYSTEM_PROBABILITY = 0.2  # 20%
            self.ECOSYSTEM_PROBABILITY_DIE = 0.02  # 2%
            self.ECOSYSTEM_PROBABILITY_DIE_ELD_FRACTION = 1000  # 0.1%
            self.ORGANISM_PROBABILITY_DIE = 0.05  # 5%
            self.ORGANISM_PROBABILITY_DIE_ELD_FRACTION = 1000  # 0.1%

        except Exception as e:
            exit(e)
