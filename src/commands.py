import re

from src.bot import database
from src.utils import toJson
from src.request_configuration import RequestConfiguration

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

# https://stackoverflow.com/a/7160778/7346633
urlValidator = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


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
        return "Usage: /touch <request name> <proper url>"

    # Validate name
    name = context.args[0]
    if not name.isalnum():
        return "*Error:* You can only use alphanumeric names!"

    if name in database.userRequests[user]:
        return "*Error:* %s already exists" % name

    # Validate url
    url = context.args[1]
    if re.match(urlValidator, url) is None:
        return "*Error:* %s cannot pass the format check" % url

    # Create
    database.userRequests[user][name] = RequestConfiguration(url)
    database.save()

    return "*%s* is successfully created!" % name


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
