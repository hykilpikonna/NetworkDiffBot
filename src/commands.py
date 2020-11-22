# Help message
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


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=helpMsg)
