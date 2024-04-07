import json

import utils.logger as logger
from openai import OpenAI
from utils.config import Config

# from utils.my_utils import MyUtils

config = Config()
# utils = MyUtils()


class OpenAI:

    def __init__(self) -> None:
        if config.OPENAI_API_KEY == "":
            logger.info("OPENAI_API_KEY is not set")
            return None
        logger.info("Creating OpenAI client...")
        self._client = OpenAI(api_key=config.OPENAI_API_KEY)

    def generate_text(self, pre_prompt, prompt) -> json:
        messages = [
            {"role": "system", "content": pre_prompt},
            {"role": "user", "content": prompt},
        ]
        return {}
        response = self._client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=messages,
            # temperature=0,
            max_tokens=200,
        )
        logger.info(response.usage.total_tokens)
        return response.choices[0].message.content
        # return json.dumps(json.loads(response.model_dump_json()), indent=4)
