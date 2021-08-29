import json
import dataset
import sqlalchemy

class dbhandler:
    def __init__(self, url, password, port=5432):
        print("~~~~~Initializing database~~~~~")
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
            self.users.create_column('discord', self.db.types.text, unique=True, nullable=False)
            self.users.create_column('role', self.db.types.text, nullable=False)
            self.users.create_column('team', self.db.types.text, nullable=True)
            #create teams table
            self.teams.create_column('name', self.db.types.text, unique=True, nullable=False)
            self.teams.create_column('ctfs', self.db.types.text, nullable=True)
            
            self.teams.upsert({"name": "admins", "ctfs": None}, keys=["name"])
        print("~~~~~Init Complete~~~~~")

    def get_ctfs(self): 
        return {entry["name"]:json.loads(entry["teams"]) for entry in self.ctfs.find(id={'>=': 0})}
    
    def get_users(self): 
        return {entry["discord"]:{i:entry[i] for i in entry if i not in ["id", 'discord']} for entry in self.users.find(id={'>=': 0})}
    
    def get_teams(self, members=False): 
        temp={entry["name"]:{"ctfs": json.loads(entry["ctfs"])} if entry["ctfs"] else None for entry in self.teams.find(id={'>=': 0})}
        if members:
            for user in self.get_users():
                if "members" in temp[user["team"]]: temp[user["team"]]["members"].append(user)
                else: temp[user["team"]]["members"]=[user]
        return temp
    
    def get_user(self, discord):
        ret=self.users.find_one(discord=str(discord))
        if ret: ret={i:ret[i] for i in ret if i not in ["id", 'discord']}
        return ret
    
    def get_team(self, name):
        ret=self.teams.find_one(name=name)
        if ret: ret={"ctfs": json.loads(ret["ctfs"])}
        return ret
        
    def create_team(self, name):
        self.teams.upsert({"name": name, "ctfs": "{}"}, keys=["name"])
        return self.get_team(name)
    
    def create_user(self, discord, team, role="user"):
        if team: #create team if verifiable and nonexisitent
            curr_team, discord = self.get_team(team), str(discord)
            if not curr_team: curr_team=self.create_team(team)
        #do not update if key already exists
        try: self.users.insert({"discord": discord, "role": role, "team": None})
        except sqlalchemy.exc.IntegrityError: pass
        return self.get_user(discord)