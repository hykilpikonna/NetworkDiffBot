import json

from src.constants import dbPath
from src.utils import toJson


class Database:
    users = []
    userRequests = {}
    userStatus = {}

    def save(self):
        f = open(dbPath, 'w')
        f.write(toJson(self))
        f.close()
