import dataset

class dbhandler:
    def __init__(self, url, password, port=5432):
        self.db = dataset.connect(f'postgresql://postgres:{password}@{url}:{port}/postgres')
        self.teams = self.db['teams']
        self.ctfs = self.db['ctfs']
        self.users = self.db['users']
        if not self.users.find_one(role="admin"):
            self.users.upsert({"username": "admin", "role": "admin", "team": "admin"}, keys=["username"])
            self.teams.upsert({"name": "admin", "ctfs": "{}"}, keys=["name"])
            self.ctfs.insert({"name": "temp", "teams": "[]"})
            self.ctfs.delete(name="temp")
        print("~~~~~Init Complete~~~~~")

    def get_ctfs(self):
        pass