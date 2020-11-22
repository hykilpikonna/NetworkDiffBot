import telegram
import logging
import os

helpMsg = """
Welcome! This bot monitors http changes!

/start - Start the bot

**Management Commands**
/ls - List the http requests you've created
/touch - Create a http request
/rm - Delete a http request
/mv - Rename a http request

**Configuration Commands**
/nano - Edit a http request
/interval - Change the interval between the updates of a http request

**Start/Stop Commands**
/enable - Start listening to a http request
/stop - Stop listening to a http request
"""

# Main
if __name__ == '__main__':

    #  Initialize logger
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Create bot with configurable token
    bot = telegram.Bot(token=os.environ['TG_TOKEN'])

    # Print bot info
    print("Bot info: ", bot.getMe())

