import os
import sys

token = os.getenv('TG_TOKEN', None)
if token is None:
    print('Please configure your token in environment variable TG_TOKEN first.')
    sys.exit(0)

font = os.getenv('FONT', None)
dbPath = 'database.json'
