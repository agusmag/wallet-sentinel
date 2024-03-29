# Flask_SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Flask_Migrate
from flask_migrate import Migrate
migrations = Migrate(compare_type=True)

# Flask_Login
from flask_login import LoginManager
login_manager = LoginManager()

#Slack Client
import slack
from os import getenv

def sendNewUserSlackMessage(channel, username):
    slack_token = os.environ["SLACK_API_TOKEN"]
    client = slack.WebClient(token=slack_token)

    client.chat_postMessage(
        channel=channel,
        text="*Production* -> :memo: New user has been created! Welcome *{0}* :hugging_face:".format(username)
    )

def initialize_flask_server_debugger_if_needed():
    if getenv("DEBUGGER") == "True":
        import multiprocessing

        if multiprocessing.current_process().pid > 1:
            import debugpy

            debugpy.listen(("0.0.0.0", 10001))
            print("⏳ VS Code debugger can now be attached, press F5 in VS Code ⏳", flush=True)
            debugpy.wait_for_client()
            print("🎉 VS Code debugger attached, enjoy debugging 🎉", flush=True)
