import json

from src.constants import dbPath
from src.utils import toJson


class Database:
    def __init__(self):
        self.users = []
        self.userRequests = {}
        self.userStatus = {}

    def save(self):
        f = open(dbPath, 'w')
        f.write(toJson(self))
        f.close()

    def checkUser(self, user):
        if user not in self.users:
            self.users.append(user)
            self.userRequests[user] = {}
            self.userStatus[user] = {}
        return user
