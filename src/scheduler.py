import difflib
import time
from datetime import datetime
from io import BytesIO

from telegram.ext import CallbackContext, Updater

from src.database import Database
from src.utils import wrap, render, sendRequest


class CacheEntry:
    user: str
    name: str
    time: float
    text: str

    def __init__(self, user: str, name: str, time: float, text: str):
        self.user = user
        self.name = name
        self.time = time
        self.text = text


class Scheduler:
    # storage[user][name] = CacheEntry
    storage: {str: {str: CacheEntry}} = {}

    # Constructor
    def __init__(self, database: Database, updater: Updater):
        self.database = database
        self.updater = updater

        # Start job
        self.job = self.updater.job_queue.run_repeating(self.update, interval=5, first=0)

    # Update tasks
    def update(self, context: CallbackContext):
        now = time.time()
        nowText = datetime.now().strftime('%b %d %Y %H-%M-%S')

        # Function to update a single task
        def updateTask(cache: CacheEntry):
            request = self.database.reqs[cache.user][cache.name]
            if now - cache.time < request.get('interval', 120):
                return

            # Execute request
            text: str = wrap(sendRequest(request))

            # First time http request
            if cache.text == '':
                cache.text = text

            # Generate diff
            diffRaw = difflib.unified_diff(cache.text.splitlines(True), text.splitlines(True), fromfile='before', tofile='after')
            diff = ''.join(diffRaw)

            # Update cache
            cache.text = text
            cache.time = now

            if diff != '':
                # Render diff
                doc = BytesIO(render(diff))
                fileName = 'diff %s %s.png' % (cache.name, nowText)
                caption = '*%s Changed!*' % cache.name

                # Send as file
                context.bot.send_document(int(user), doc, fileName, caption, parse_mode='markdown')

        # Update all tasks
        for user in self.storage:
            for name in self.storage[user]:
                updateTask(self.storage[user][name])

    # Start a task
    def start(self, user: str, name: str):
        if self.isStarted(user, name):
            return False

        request = self.database.reqs[user][name]
        if user not in self.storage:
            self.storage[user] = {}

        # Add task
        self.storage[user][name] = CacheEntry(user, name, 0, '')
        if not request['enabled']:
            request['enabled'] = True
            self.database.save()

        return True

    # Stop a task
    def stop(self, user: str, name: str):
        if not self.isStarted(user, name):
            return False

        # Stop and remove task
        self.storage[user].pop(name, None)
        self.database.reqs[user][name]['enabled'] = False
        self.database.save()

        return True

    # Check if a task is started
    def isStarted(self, user: str, name: str):
        return user in self.storage and name in self.storage[user]
