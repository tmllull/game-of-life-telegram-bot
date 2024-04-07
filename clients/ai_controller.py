from clients.azure_openai import AzureOAI
from clients.openai import OpenAI
from utils import logger as logger
from utils.config import Config

open_ai = OpenAI()
azure_openai = AzureOAI()
config = Config()


class AIController:
    def __init__(self):
        if config.AI_SERVICE is None or (
            config.AI_SERVICE != "openai" and config.AI_SERVICE != "azure"
        ):
            self.has_service = False
        else:
            self.has_service = True

    def generate_text(self, pre_prompt, prompt) -> str:
        if config.AI_SERVICE == "openai":
            return open_ai.generate_text(pre_prompt, prompt)
        elif config.AI_SERVICE == "azure":
            return azure_openai.generate_text(pre_prompt, prompt)
