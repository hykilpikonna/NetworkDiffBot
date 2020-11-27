import re
from io import BytesIO

from telegram import Bot, Update
from telegram.ext import Updater, CallbackContext

from src.database import Database
from src.scheduler import Scheduler
from src.utils import toJson, sendRequest

helpMsg = """
Welcome! This bot monitors http changes!

/start - Start the bot

*Management Commands*
/ls - List the http requests you've created
/touch - Create a http request
/rm - Delete a http request

*Configuration Commands*
/nano - Edit a http request
/test - Test a http request
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

database = Database()
scheduler: Scheduler
updater: Updater


# Initialize bot
def init(bot: Bot, u: Updater):
    global updater
    updater = u
    global scheduler
    scheduler = Scheduler(database, updater)

    for user in database.users:
        for name in database.reqs[user]:
            if database.reqs[user][name]['enabled']:
                scheduler.start(user, name)


def start(update: Update, context: CallbackContext):
    chat = update.effective_chat
    database.checkUser(chat.id)

    return helpMsg


def ls(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = database.checkUser(chat.id)
    requests = database.reqs[user]

    return "Your requests: %s" % toJson(requests)


def touch(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = database.checkUser(chat.id)

    # Too many requests
    if len(database.reqs[user]) > 10:
        return "*Error:* One user can only have 10 requests for now ;-;"

    # No args
    if len(context.args) != 2:
        return "Usage: /touch <request name> <proper url>"

    # Validate name
    name = context.args[0]
    if not name.isalnum():
        return "*Error:* You can only use alphanumeric names!"

    if name in database.reqs[user]:
        return "*Error:* %s already exists" % name

    # Validate url
    url = context.args[1]
    if re.match(urlValidator, url) is None:
        return "*Error:* %s cannot pass the format check" % url

    # Create
    database.reqs[user][name] = {'method': 'GET', 'url': url, 'headers': {}, 'data': None, 'enabled': False}
    database.save()

    return "%s is successfully created!" % name


def rm(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = database.checkUser(chat.id)

    # No args
    if len(context.args) != 1:
        return "Usage: /rm <request name>"

    # Check if name exists
    name = context.args[0]
    if name not in database.reqs[user]:
        return "%s doesn't exist, nothing changed." % name

    # Remove
    scheduler.stop(user, name)
    database.reqs[user].pop(name, None)
    database.save()

    return "%s is successfully removed!" % name


def nano(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = database.checkUser(chat.id)


def test(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = database.checkUser(chat.id)

    # No args
    if len(context.args) != 1:
        return "Usage: /test <request name>"

    # Check if name exists
    name = context.args[0]
    if name not in database.reqs[user]:
        return "*Error:* %s doesn't exist." % name

    # Run
    text = sendRequest(database.reqs[user][name])

    if len(text) > 60000:
        return "File too large (>60kb)."

    context.bot.send_document(chat_id=chat.id, document=BytesIO(bytes(text, 'utf-8')), filename=name + '.txt')


def interval(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = database.checkUser(chat.id)

    # No args
    if len(context.args) != 2:
        return "Usage: /interval <request name> <interval in seconds>"

    # Check if name exists
    name = context.args[0]
    if name not in database.reqs[user]:
        return "*Error:* %s doesn't exist." % name
    request = database.reqs[user][name]

    # Validate the interval of the interval
    i = int(context.args[1])
    if i < 40:
        return "*Error:* %s is too long or too short. (Min: 40s)" % i

    request['interval'] = i
    database.save()

    return "Success!"


def enable(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = database.checkUser(chat.id)

    # No args
    if len(context.args) != 1:
        return "Usage: /enable <request name>"

    # Check if name exists
    name = context.args[0]
    if name not in database.reqs[user]:
        return "*Error:* %s doesn't exist." % name

    # Start task
    if not scheduler.start(user, name):
        return "*Error:* %s is already enabled." % name

    return "Started!"


def disable(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = database.checkUser(chat.id)

    # No args
    if len(context.args) != 1:
        return "Usage: /disable <request name>"

    # Check if name is running
    name = context.args[0]
    if not scheduler.stop(user, name):
        return "*Error:* %s isn't enabled." % name

    return "Removed!"


