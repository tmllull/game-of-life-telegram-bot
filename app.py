from src.database import models
from src.database.database import engine
from src.game_of_life.game_of_life import GameOfLife
from src.utils.config import Config
from telegram.ext import Application, ApplicationBuilder, MessageHandler

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
