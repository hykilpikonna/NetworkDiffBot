import difflib
import json
import re
from io import BytesIO

from telegram import Bot, Update
from telegram.ext import Updater, CallbackContext, Job

from src.database import Database
from src.utils import toJson, create, dictToString

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
tasks: {str: {str: Job}} = {}
cache: {str: {str: str}} = {}
updater: Updater = {}


def sendRequest(req: str):
    r = create(req)
    text = r.text
    if r.headers['Content-Type'] == 'application/json':
        text = dictToString(json.loads(text))
    r.close()
    return text


def createTaskCallback(user: str, taskName: str, request):
    if user not in cache:
        cache[user] = {}

    def task(context: CallbackContext):
        print('request sent!')

        # Send request
        text = sendRequest(request)

        # First time http request
        if taskName not in cache[user]:
            cache[user][taskName] = text

        # Compare diff
        else:
            diffRaw = difflib.unified_diff(cache[user][taskName].splitlines(1), text.splitlines(1), fromfile='before', tofile='after')
            diff = ''.join(diffRaw)
            cache[user][taskName] = text
            if diff != '':
                context.bot.send_message(chat_id=user, text='*%s Changed!*\n\n```diff\n%s```' % (taskName, diff), parse_mode="markdown")
    return task


def startTask(user: str, taskName: str):
    request = database.userRequests[user][taskName]
    if user not in tasks:
        tasks[user] = {}

    tasks[user][taskName] = updater.job_queue.run_repeating(createTaskCallback(user, taskName, request),
                                                            interval=request.get('interval', 120), first=0)

    # Keep record
    if taskName not in database.userStatus[user]['enabledTasks']:
        database.userStatus[user]['enabledTasks'].append(taskName)
        database.save()


# Initialize bot
def init(bot: Bot, u: Updater):
    global updater
    updater = u


def start(update: Update, context: CallbackContext):
    chat = update.effective_chat
    database.checkUser(chat.id)

    return helpMsg


def ls(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = database.checkUser(chat.id)
    requests = database.userRequests[user]

    return "Your requests: %s" % toJson(requests)


def touch(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = database.checkUser(chat.id)

    # Too many requests
    if len(database.userRequests[user]) > 10:
        return "*Error:* One user can only have 10 requests for now ;-;"

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
    database.userRequests[user][name] = {'method': 'GET', 'url': url, 'headers': {}, 'data': None}
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
    if name not in database.userRequests[user]:
        return "%s doesn't exist, nothing changed." % name

    # Remove
    database.userRequests[user].pop(name, None)
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
    if name not in database.userRequests[user]:
        return "*Error:* %s doesn't exist." % name

    # Run
    text = sendRequest(database.userRequests[user][name])

    if len(text) > 60000:
        return "File too large (>60kb)."

    context.bot.send_document(chat_id=chat.id, document=BytesIO(bytes(text, 'utf-8')), filename=name + '.txt')
    return 'Done!'


def interval(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = database.checkUser(chat.id)


def enable(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = database.checkUser(chat.id)


def disable(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = database.checkUser(chat.id)
