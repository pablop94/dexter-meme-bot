import os

from telegram import Bot, Update
from telegram.ext import Dispatcher
from bot import register_handlers
from log import logger

def dexter_meme(request):
    if request.method == "POST":
        if request.args.get('token') == os.environ["DEXTER_TOKEN"]:
            bot = Bot(token=os.environ["TELEGRAM_TOKEN"])
            dispatcher = Dispatcher(bot, None, workers=0)
            update = Update.de_json(request.get_json(force=True), bot)

            register_handlers(dispatcher)

            dispatcher.process_update(update)
        else:
            logger.error(f'Invalid token: {request.args.get("token")}')

    return "ok"