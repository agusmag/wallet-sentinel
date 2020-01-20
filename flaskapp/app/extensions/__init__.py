# Flask_SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Flask_Migrate
from flask_migrate import Migrate
migrations = Migrate()

# Flask_Login
from flask_login import LoginManager
login_manager = LoginManager()

#Slack Client
import slack
import os

def sendNewUserSlackMessage(channel, username):
    slack_token = os.environ["SLACK_API_TOKEN"]
    client = slack.WebClient(token=slack_token)

    client.chat_postMessage(
        channel=channel,
        text=":memo: New user has been created! Welcome {0} :hugging_face:".format(username)
    )