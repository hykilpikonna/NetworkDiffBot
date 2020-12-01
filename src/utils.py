import difflib
import json
import textwrap
from urllib.parse import unquote

import requests
from pygments import highlight as syntax_highlight
from pygments.formatters.img import ImageFormatter
from pygments.lexers import *
from telegram.ext import CommandHandler

from src.constants import font


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
    message = unquote(message)
    lexer = get_lexer_by_name("diff", stripall=True)
    # lexer = guess_lexer(message)
    formatter = ImageFormatter(font_name=font, style="colorful", font_size=12, line_pad=4)
    result = syntax_highlight(message, lexer, formatter, outfile=None)
    return result


def wrap(string: str):
    return '\n'.join([' ⏎\n  '.join(textwrap.wrap(line, 120)) for line in string.splitlines()])


def sendRequest(req):
    try:
        response = create(req)
        text = response.text
        if response.headers['Content-Type'] == 'application/json':
            text = dictToString(json.loads(text))
        response.close()
        return text
    except requests.exceptions.ConnectionError as e:
        return "Error: ConnectionError!\n" + str(e)


if __name__ == '__main__':
    before = wrap("""
 <li><a href="Etterna-0.70.3-Darwin.dmg">Etterna-0.70.3-Darwin.dmg</a></li>
 <li><a href="favicon-dark.svg">favicon-dark.svg</a></li>
 <li><a href="Kant-%20short%20form%20%28no%20Kingdom%20of%20Ends%29.pdf">Kant- short form (no Kingdom of Ends).pdf</a></li>
 <li><a href="kdeconnect-kde-master-985-macos-64-clang%20%281%29.dmg">kdeconnect-kde-master-985-macos-64-clang (1).dmg</a></li>
 <li><a href="Keep/">Keep/</a></li>
 <li><a href="Media/">Media/</a></li>
 <li><a href="osu%21macOS%20Agent中文.app/">osu!macOS Agent中文.app/</a></li>""")
    after = wrap("""
 <li><a href="Etterna-0.70.3-Darwin.dmg">Etterna-0.70.3-Darwin.dmg</a></li>
 <li><a href="favicon-dark.svg">favicon-dark.svg</a></li>
 <li><a href="Kant-z%20short%20form%20%28no%20Kingdom%20of%20Ends%29.pdf">Kant- short form (no Kingdom of Ends).pdf</a></li>
 <li><a href="kdeconnect-kde-master-985-macos-64-clang%20%281%29.dmg">kdeconnect-kde-master-985-macos-64-clang (111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111).dmg</a></li>
 <li><a href="Keep/">Keep/</a></li>
 <li><a href="Media/">Media/</a></li>
 <li><a href="osu%21macOS%20Agent中文.app/">osu!macOS Agent中文.app/</a></li>""")

    diffRaw = difflib.unified_diff(before.splitlines(1), after.splitlines(1))
    diff = ''.join(diffRaw)
    r = render(diff)
    f = open('test.png', 'wb')
    f.write(r)
    f.close()
