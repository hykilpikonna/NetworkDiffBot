import json

from src.constants import dbPath


class Database:
    users = []
    userRequests = {}
    userStatus = {}

    def save(self):
        f = open(dbPath, 'w')
        f.write(json.dumps(self))
        f.close()
