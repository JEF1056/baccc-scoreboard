import json
import dataset

class dbhandler:
    def __init__(self, url, password, port=5432):
        self.db = dataset.connect(f'postgresql://postgres:{password}@{url}:{port}/postgres')
        self.teams = self.db['teams']
        self.ctfs = self.db['ctfs']
        self.users = self.db['users']
        if not self.teams.find_one(name="admins"):
            print("First database initialization. This might take some time.")
            #create ctfs table
            self.ctfs.create_column('name', self.db.types.text, unique=True, nullable=False)
            self.ctfs.create_column('teams', self.db.types.text, nullable=False)
            #create users table
            self.users.create_column('username', self.db.types.text, unique=True, nullable=False)
            self.users.create_column('role', self.db.types.text, nullable=True)
            self.users.create_column('team', self.db.types.text, nullable=True)
            self.users.create_column('discord', self.db.types.text, nullable=False)
            #create teams table
            self.teams.create_column('name', self.db.types.text, unique=True, nullable=False)
            self.teams.create_column('ctfs', self.db.types.text, nullable=True)
            
            self.teams.upsert({"name": "admins", "ctfs": None}, keys=["name"])
        print("~~~~~Init Complete~~~~~")

    def get_ctfs(self): 
        return {entry["name"]:json.loads(entry["teams"]) for entry in self.ctfs.find(id={'>=': 0})}
    
    def get_users(self): 
        return {entry["username"]:{i:entry[i] for i in entry if i!='username'} for entry in self.users.find(id={'>=': 0})}
    
    def get_teams(self): 
        return {entry["name"]:json.loads(entry["ctfs"]) if entry["ctfs"] else None for entry in self.teams.find(id={'>=': 0})}