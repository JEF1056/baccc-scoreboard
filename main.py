import json
from src.database import dbhandler
from werkzeug.exceptions import HTTPException
from flask_discord import DiscordOAuth2Session, requires_authorization
from flask import Flask, redirect, url_for, render_template, request, send_from_directory

#Load config
config = json.load(open("config.json","r"))

app = Flask(__name__)
app.secret_key = config["key"].encode()
try: db = dbhandler(config["database"]['url'], config["database"]['password'], port=config["database"]['port'])
except: db = dbhandler(config["database"]['url'], config["database"]['password'])

app.config["DISCORD_CLIENT_ID"] = config["discord"]["client_id"]      # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = config["discord"]["client_secret"]  # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = config["discord"]["redirect_uri"]   # URL to your callback endpoint.
discord = DiscordOAuth2Session(app)

# Handle oauth login and logout
@app.route("/login/discord")
def discord_login():
    return discord.create_session(scope=["identify"])

@app.route("/logout/discord")
@requires_authorization
def discord_logout():
    discord.revoke()
    return redirect(url_for(".index"))
    
# Handle pages
@app.route("/", methods=['GET'])
def index():
    print(db.create_user("249024790030057472", None))
    if discord.authorized: 
        user = discord.fetch_user()
        user = db.create_user(user.id, None)
    else: user=None
    return render_template('index.html', authed=discord.authorized)

@app.route("/board", methods=['GET', 'POST'])
def board():
    teams=db.get_teams()
    ctfs=db.get_ctfs()
    return render_template('board.html', teams=list(teams), ctfs=ctfs)

"""
@app.route("/redir")
def redirect_to_page():
    path = request.path     
    return render_template('redirect.html', task=path)
"""

@app.errorhandler(HTTPException)
def handle_exception(e):
    return render_template("error.html", error=e), e.code

if __name__ == "__main__":
   app.run(host="0.0.0.0", threaded=True)