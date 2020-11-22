import json

from telegram.ext import CommandHandler


def toJson(obj):
    return json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True, indent=4)


# Wrap command
def createCommand(method):

    # Create wrapper command
    def command(update, context):

        # Run command and get return data
        data = method(update, context)

        # Send back data if not null
        if data is not None and data is not '':
            context.bot.send_message(chat_id=update.effective_chat.id, text=data)

    # Create handler for the wrapper command
    return CommandHandler(method.__name__, command, run_async=True)
