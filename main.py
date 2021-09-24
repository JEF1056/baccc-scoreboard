import os
import json

#Load config
config = json.load(open("config.json","r"))

from src.api import api
import src.helpers as helpers
helpers.config=config
from werkzeug.exceptions import HTTPException
from flask_discord import DiscordOAuth2Session, requires_authorization, exceptions
from flask import Flask, redirect, url_for, render_template, session, request, send_from_directory, abort

app = Flask(__name__)
app.secret_key = config["key"].encode()
try: db = api(config["database"]['url'], config["database"]['password'], port=config["database"]['port'])
except: db = api(config["database"]['url'], config["database"]['password'])

app.config["DISCORD_CLIENT_ID"] = config["discord"]["client_id"]      # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = config["discord"]["client_secret"]  # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = config["discord"]["redirect_uri"]   # URL to your callback endpoint.
discord = DiscordOAuth2Session(app)

# Handle oauth login and logout
@app.route("/login/discord")
def discord_login():
    return discord.create_session(scope=["identify"])

@app.route("/login/discord/authorized")
def discord_callback():
    session.clear()
    try: discord.callback()
    except:pass
    return redirect(url_for(".index"))

@app.route("/logout/discord")
@requires_authorization
def discord_logout():
    discord.revoke()
    return redirect(url_for(".index"))
    
# Handle pages
@app.route("/", methods=['GET'])
def index():
    if discord.authorized: 
        discord_user = discord.fetch_user()
        user = db.create_user(discord_user.id, discord_user.username + '#' + discord_user.discriminator, None)
    else: discord_user, user = None, None   
    return render_template('index.html', authed=discord.authorized, discord_user=discord_user, user=user)

@app.route("/scores", methods=['GET', 'POST'])
def scores():
    teams, ctfs= db.get_teams(), helpers.preconvert_to_chartjs(db.get_ctfs())
    for index, team in enumerate(teams):
        for ctf in teams[team]["ctfs"]:
            ctfs[ctf]["data"]=helpers.insert_at_index(ctfs[ctf]["data"], index, teams[team]["ctfs"][ctf])
    ctfs, team_totals =helpers.convert_to_chartjs(ctfs, teams)

    print(teams)
    print(ctfs)
    return render_template('board.html', teams=list(teams), ctfs=ctfs, team_totals=team_totals)

@app.route("/upload", methods=["GET", "POST"])
@requires_authorization
def upload():
    discord_user=discord.fetch_user()
    user, ctfs, errors = db.get_user(discord_user.id), db.get_ctfs(), []
    if not user: abort(401)
    team = db.get_team(user["team"])
    if not team: abort(401)

    if request.method == 'POST':
        print(request.files)
        screenshot = request.files['screenshot']
        if screenshot.filename == '': errors.append("No Screenshot")
        elif screenshot and not helpers.allowed_file(screenshot.filename): errors.append("Not a supported screenshot type.")
        else:
            #save screenshot if possible
            try:
                helpers.create_dir(os.path.join(config["screenshots"], user['team']))
                screenshot.save(os.path.join(config["screenshots"], user['team'], request.form["ctf"]+".png"))
            except Exception as e: 
                print(e)
                errors.append("Unable to save screenshot. Contact an admin.")

            #ensure possible user errors can't be made
            if not str(request.form["ctf"].strip()): errors.append("CTF name is empty")
            if str(request.form["ctf"].strip()) not in ctfs: errors.append("CTF does not exist/is not enabled. Contact an admin.")
            try: int(request.form["score"])
            except: errors.append("Score is not an integer")

            #in the case of no errors, add score.
            if errors==[]: db.add_score(request.form["ctf"], request.form["score"], user["team"])

            #update variables before loading the page
            user, ctfs, errors = db.get_user(discord_user.id), db.get_ctfs(), []
            team = db.get_team(user["team"])

    return render_template("upload.html", ctfs=ctfs, user=str(discord_user), team=user["team"], scores=team['ctfs'], errors=errors)

"""
@app.route("/redir")
def redirect_to_page():
    path = request.path     
    return render_template('redirect.html', task=path)
"""

@app.errorhandler(exceptions.Unauthorized)
def handle_unauth_exception(e):
    return render_template("error.html", error="401 Unauthorized: The server could not verify that you are authorized to access the URL requested."), 401

@app.errorhandler(HTTPException)
def handle_exception(e):
    return render_template("error.html", error=e), e.code

if __name__ == "__main__":
   app.run(host="0.0.0.0", threaded=True)