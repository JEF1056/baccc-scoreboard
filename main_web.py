import json
import dataset
from werkzeug.exceptions import HTTPException
from flask import Flask, request, render_template, request

"""
# Below uis useful code if github/discord oauth2 floaws are needed

from flask_dance.contrib.github import make_github_blueprint, github
from flask_discord import DiscordOAuth2Session, requires_authorization

app.config["DISCORD_CLIENT_ID"] =      # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] =  # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] =   # URL to your callback endpoint.
#app.config["DISCORD_BOT_TOKEN"] = ""  # Required to access BOT resources.

github_blueprint = make_github_blueprint(
    client_id="35d779aeb1dd69469cd8",
    client_secret="104b76a96bc86ec5797ef552d667bf52ca17430f",
    redirect_url="/dashboard",
    redirect_to="/dashboard"
)
app.register_blueprint(github_blueprint, url_prefix="/login", redirect_url="/dashboard", redirect_to="/dashboard")
discord = DiscordOAuth2Session(app)
#executor=concurrent.futures.ThreadPoolExecutor(max_workers=100)
"""

config = json.load("config.json")

app = Flask(__name__)
app.secret_key = config["key"].encode()
    
@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

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
   app.run(host="0.0.0.0", threaded=True, port=8080)