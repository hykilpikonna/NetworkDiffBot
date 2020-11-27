import difflib
from datetime import datetime
from io import BytesIO

from telegram.ext import Job, CallbackContext, Updater

from src.commands import sendRequest
from src.database import Database
from src.utils import wrap, render


class Scheduler:
    tasks: {str: {str: Job}} = {}
    cache: {str: {str: str}} = {}

    def __init__(self, database: Database, updater: Updater):
        self.database = database
        self.updater = updater

    def create(self, user: str, taskName: str, request):
        if user not in self.cache:
            self.cache[user] = {}

        def task(context: CallbackContext):
            # Send request
            text = wrap(sendRequest(request))

            # First time http request
            if taskName not in self.cache[user]:
                self.cache[user][taskName] = text

            # Compare diff
            else:
                # Generate diff
                diffRaw = difflib.unified_diff(self.cache[user][taskName].splitlines(1), text.splitlines(1),
                                               fromfile='before', tofile='after')
                diff = ''.join(diffRaw)
                self.cache[user][taskName] = text

                if diff != '':
                    # Render diff
                    doc = BytesIO(render(diff))
                    time = datetime.now().strftime('%b %d %Y %H-%M-%S')
                    fileName = 'diff %s %s.png' % (taskName, time)
                    caption = '*%s Changed!*' % taskName

                    # Send as file
                    context.bot.send_document(int(user), doc, fileName, caption, parse_mode='markdown')

        return task

    def start(self, user: str, request):
        name = request['name']

        if self.isStarted(user, name):
            return False

        if user not in self.tasks:
            self.tasks[user] = {}

        self.tasks[user][name] = self.updater.job_queue.run_repeating(self.create(user, name, request), interval=request.get('interval', 120), first=0)

        # Keep record
        if not request['enabled']:
            request['enabled'] = True
            self.database.save()

        return True

    def stop(self, user: str, name: str):
        if not self.isStarted(user, name):
            return False

        # Stop and remove task
        job = self.tasks[user][name]
        job.enabled = False
        job.schedule_removal()
        self.tasks[user].pop(name, None)
        self.database.reqs[user][name]['enabled'] = False
        self.database.save()

        return True

    def isStarted(self, user: str, name: str):
        return user in self.tasks and name in self.tasks[user]

    def updateInterval(self, user: str, name: str, request):
        if not self.isStarted(user, name):
            return False

        self.stop(user, name)
        self.start(user, request)
        return True
