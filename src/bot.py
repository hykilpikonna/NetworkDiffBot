import json

import telegram
from telegram.ext import CommandHandler
from telegram.ext import Updater
import logging
import os

from src.commands import *
from src.constants import dbPath, token
from src.database import Database


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
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('ls', ls))
    dispatcher.add_handler(CommandHandler('touch', touch))
    dispatcher.add_handler(CommandHandler('rm', rm))
    dispatcher.add_handler(CommandHandler('mv', mv))
    dispatcher.add_handler(CommandHandler('nano', nano))
    dispatcher.add_handler(CommandHandler('interval', interval))
    dispatcher.add_handler(CommandHandler('enable', enable))
    dispatcher.add_handler(CommandHandler('disable', disable))

    # Start bot
    updater.start_polling()