import json

import telegram
from telegram.ext import CommandHandler
from telegram.ext import Updater
import logging
import os

from src.commands import *
from src.constants import dbPath, token
from src.database import Database
from src.utils import createCommand

database = Database()

# Main
if __name__ == '__main__':
    #  Initialize logger
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Check database
    if os.path.isfile(dbPath):
        f = open(dbPath, 'r')
        database = json.loads(f.read())
        f.close()

    # Create bot
    bot = telegram.Bot(token=token)

    # Print bot info
    print("Bot created: ", bot.getMe())

    # Create updater
    updater = Updater(bot=bot)
    dispatcher = updater.dispatcher

    # Register commands
    commands = [start, ls, touch, rm, mv, nano, interval, enable, disable]
    [dispatcher.add_handler(createCommand(cmd)) for cmd in commands]

    # Start bot
    updater.start_polling()
