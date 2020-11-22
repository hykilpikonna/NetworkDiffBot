from src.bot import database
from src.utils import toJson

helpMsg = """
Welcome! This bot monitors http changes!

/start - Start the bot

*Management Commands*
/ls - List the http requests you've created
/touch - Create a http request
/rm - Delete a http request
/mv - Rename a http request

*Configuration Commands*
/nano - Edit a http request
/interval - Change the interval between the updates of a http request

*Start/Stop Commands*
/enable - Start listening to a http request
/disable - Stop listening to a http request
"""


def start(update, context):
    chat = update.effective_chat
    database.checkUser(chat.id)

    return helpMsg


def ls(update, context):
    chat = update.effective_chat
    user = database.checkUser(chat.id)
    requests = database.userRequests[user]

    return "Your requests: %s" % toJson(requests)


def touch(update, context):
    chat = update.effective_chat
    user = database.checkUser(chat.id)

    # No args
    if len(context.args) != 2:
        return "用法: /touch <request name> <proper url>"

    # Validate name
    name = context.args[0]
    if not name.isalnum():
        return "只能有数字或者字母哦w"


def rm(update, context):
    chat = update.effective_chat
    user = database.checkUser(chat.id)


def mv(update, context):
    chat = update.effective_chat
    user = database.checkUser(chat.id)


def nano(update, context):
    chat = update.effective_chat
    user = database.checkUser(chat.id)


def interval(update, context):
    chat = update.effective_chat
    user = database.checkUser(chat.id)


def enable(update, context):
    chat = update.effective_chat
    user = database.checkUser(chat.id)


def disable(update, context):
    chat = update.effective_chat
    user = database.checkUser(chat.id)
