import logging
import sys

# from src.database.database import SessionLocal

# db = SessionLocal()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
if not logger.handlers:
    logger.propagate = False
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)

    file_handler = logging.FileHandler("logs.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)


def info(msg):
    # print(msg)
    logger.info(msg)


def debug(msg):
    logger.debug(msg)


def warning(msg):
    logger.warning(msg)


def exception(msg):
    logger.exception(msg)


def error(msg):
    logger.error(msg)
