import json
from src.api import api

config = json.load(open("config.json","r"))
init = json.load(open("init.json","r"))

try: db = api(config["database"]['url'], config["database"]['password'], port=config["database"]['port'])
except: db = api(config["database"]['url'], config["database"]['password'])

print("CREATING CTFS")
for ctf in init["ctfs"]: print(f"{ctf}: {db.create_ctf(ctf)}")

print("CREATING USERS")
for team in init["users"]: print(f"{init['users'][team]}: {db.create_user(team, init['users'][team])}")

print('SETUP COMPLETE')