import json
import os

import utils.logger as logger
from openai import AzureOpenAI
from utils.config import Config

config = Config()


class AzureOAI:
    def __init__(self):
        if config.AZURE_API_KEY == "":
            logger.info("AZURE_API_KEY is not set")
            return None
        logger.info("Creating Azure OpenAI client...")
        self._client = AzureOpenAI(
            api_key=config.AZURE_API_KEY,
            api_version=config.AZURE_API_VERSION,
            azure_endpoint=config.AZURE_API_ENDPOINT,
        )
        self.AZURE_API_MODEL = config.AZURE_MODEL_NAME

    def generate_text(self, pre_prompt, prompt):
        # Send a completion call to generate an answer
        print("Sending a test completion job")
        messages = [
            {
                "role": "system",
                "content": pre_prompt,
            },
            {"role": "user", "content": prompt},
        ]
        response = self._client.chat.completions.create(
            model=self.AZURE_API_MODEL,
            messages=messages,
            max_tokens=200,
        )
        logger.info(response.usage.total_tokens)
        return response.choices[0].message.content
        # return json.dumps(json.loads(response.model_dump_json()), indent=4)
        # print(start_phrase + response.choices[0].text)
