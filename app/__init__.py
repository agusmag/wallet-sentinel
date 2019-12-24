from flask import Flask, render_template, request, redirect, flash, url_for
import os, logging, config

# Flask_SQLAlchemy
from app.extensions import db
 
# Flask_Migrate
from app.extensions import migrations

# Flask_Login
from app.extensions import login_manager

logging.basicConfig(level=logging.DEBUG,
                   format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(os.getpid()),
                   datefmt='%Y-%m-%d %H:%M:%S',
                   handlers=[logging.StreamHandler()])

logger = logging.getLogger()

def create_app():
    logger.info(f'Starting app in {config.APP_ENV} environment')
    app = Flask(__name__)
    app.config.from_object('config')

    #ORM to Manage DB Models
    db.init_app(app)

    #Enabled migrations
    migrations.init_app(app, db)

    #Set the default view for not authentication requests.
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from app.models import User

    #Flask_Login method to find the active user cookie and verify it in the DB
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.views.auth import auth
    app.register_blueprint(auth)

    from app.views.main import main
    app.register_blueprint(main)

    return app
