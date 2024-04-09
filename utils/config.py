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
            self.ROWS = int(config.get("ROWS", os.environ.get("ROWS")))
            self.COLUMNS = int(config.get("COLUMNS", os.environ.get("COLUMNS")))
            self.PROB_PER_MESSAGE = float(
                config.get("PROB_PER_MESSAGE", os.environ.get("PROB_PER_MESSAGE"))
            )
            self.NEW_ECO_PROB = float(
                config.get("NEW_ECO_PROB", os.environ.get("NEW_ECO_PROB"))
            )
            self.ECO_PROB_DIE = float(
                config.get("ECO_PROB_DIE", os.environ.get("ECO_PROB_DIE"))
            )
            self.ECO_PROB_ELD_FRACTION = float(
                config.get(
                    "ECO_PROB_ELD_FRACTION", os.environ.get("ECO_PROB_ELD_FRACTION")
                )
            )
            self.ORG_PROB_DIE = float(
                config.get("ORG_PROB_DIE", os.environ.get("ORG_PROB_DIE"))
            )
            self.ORG_PROB_ELD_FRACTION = float(
                config.get(
                    "ORG_PROB_ELD_FRACTION", os.environ.get("ORG_PROB_ELD_FRACTION")
                )
            )

        except Exception as e:
            exit(e)
