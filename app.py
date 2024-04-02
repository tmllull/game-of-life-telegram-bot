from database import models
from database.database import engine
from game_of_life.game_of_life import GameOfLife
from telegram import Update
from telegram.ext import Application, ApplicationBuilder, ContextTypes, MessageHandler
from utils.config import Config

gol = GameOfLife()

config = Config()
models.Base.metadata.create_all(bind=engine)


async def post_init(application: Application):
    await application.bot.set_my_commands([])


def main() -> None:
    app = ApplicationBuilder().token(config.TELEGRAM_TOKEN).post_init(post_init).build()
    app.add_handler(MessageHandler(None, gol.check_evolution))
    app.run_polling()


if __name__ == "__main__":
    main()
