import pickle
import os
class Users:
    def __init__(self, DataBase):
        self.users = {}
        self.FileName = DataBase
        if not os.path.getsize(self.FileName) :
            with open(self.FileName, "wb") as fh:
                pickle.dump(self.users, fh)
        with open(self.FileName, "rb") as fh:
            self.users = pickle.load(fh)
    def save(self):
        with open(self.FileName, "wb") as fh:
            pickle.dump(self.users, fh)
    def add(self, chat_id, first_name, last_name, username):
        self.users[chat_id] = [first_name, last_name, username]
        self.save()
