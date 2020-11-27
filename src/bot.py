import logging
import time

import telegram
from telegram.utils.request import Request

from src.commands import *
from src.constants import token
from src.utils import createCommand

# Main
if __name__ == '__main__':
    #  Initialize logger
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logging.getLogger('apscheduler.executors.default').propagate = False

    # Create bot
    request = Request(con_pool_size=8)
    bot = telegram.Bot(token=token, request=request)

    # Print bot info
    print("Bot created: ", bot.getMe())

    # Create updater
    updater = Updater(bot=bot, use_context=True)
    dispatcher = updater.dispatcher

    # Register commands
    commands = [start, ls, touch, rm, nano, test, interval, enable, disable]
    [dispatcher.add_handler(createCommand(cmd)) for cmd in commands]

    # Init commands
    init(bot, updater)

    # Start bot
    updater.start_polling()

    # Keep alive
    while True:
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            print("Exiting...")
            updater.stop()
            dispatcher.stop()
            exit(0)
