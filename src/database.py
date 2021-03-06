import json
import os

from src.constants import dbPath
from src.utils import toJson


class Database:
    def __init__(self):
        self.users = []
        self.reqs = {}
        self.load()

    def save(self):
        f = open(dbPath, 'w')
        f.write(toJson(self))
        f.close()

    def load(self):
        if os.path.isfile(dbPath):
            f = open(dbPath, 'r')
            database = json.loads(f.read())
            self.__dict__ = database
            f.close()
            print("Database loaded.")

    def checkUser(self, user):
        user = str(user)
        if user not in self.users:
            self.users.append(user)
            self.reqs[user] = {}
        return user

    def isEnabled(self, user: str, request: str):
        return user in self.reqs and request in self.reqs[user] and self.reqs[user][request]['enabled']
