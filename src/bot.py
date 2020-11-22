import json

import telegram
from telegram.ext import CommandHandler
from telegram.ext import Updater
import logging
import os

from src.commands import start
from src.database import Database

token = os.environ['TG_TOKEN']
dbPath = 'database.json'
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
    bot = telegram.Bot(token=os.environ['TG_TOKEN'])

    # Print bot info
    print("Bot created: ", bot.getMe())

    # Create updater
    updater = Updater(bot=bot)
    dispatcher = updater.dispatcher

    # Register commands
    dispatcher.add_handler(CommandHandler('start', start))

    # Start bot
    updater.start_polling()
