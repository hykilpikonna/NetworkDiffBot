import json

import requests
from pygments import highlight as syntax_highlight
from pygments.formatters import img
from pygments.lexers import *
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
        if data is not None and data != '':
            context.bot.send_message(chat_id=update.effective_chat.id, text=data, parse_mode="markdown")

    # Create handler for the wrapper command
    return CommandHandler(method.__name__, command, run_async=True)


# Create and execute http request
def create(req):
    return requests.request(req['method'], req['url'], headers=req.get('headers', {}), data=req.get('payload', None))


# Convert json to more readable formats
def dictToString(obj, indent=4, indentLevel=1) -> str:
    if type(obj) == dict:
        if len(obj) == 0:
            return '{}'

        result = '{\n'

        for (k, v) in obj.items():
            result += ' ' * (indent * indentLevel) + k + ': '

            # Dict inside dict
            if type(v) == dict or type(v) == list:
                if len(v) != 0:
                    result += '\n' + ' ' * (indent * indentLevel)
                result += dictToString(v, indentLevel=indentLevel + 1) + '\n'

            elif type(v) == str:
                result += '"' + v.replace('\n', '\\n') + '"\n'

            # Regular value
            else:
                result += str(v) + '\n'

        return result + ' ' * (indent * (indentLevel - 1)) + '}'

    # List
    else:
        if len(obj) == 0:
            return '[]'

        result = '[\n'

        for v in obj:
            result += ' ' * (indent * indentLevel)

            # Dict inside list
            if type(v) == dict:
                result += dictToString(v, indentLevel=indentLevel + 1) + '\n'

            elif type(v) == str:
                result += '"' + v.replace('\n', '\\n') + '"\n'

            else:
                result += str(v) + '\n'

        return result + ' ' * (indent * (indentLevel - 1)) + ']'


def render(message):
    lexer = get_lexer_by_name("diff", stripall=True)
    # lexer = guess_lexer(message)
    formatter = img.JpgImageFormatter(style="colorful")
    result = syntax_highlight(message, lexer, formatter, outfile=None)
    return result
