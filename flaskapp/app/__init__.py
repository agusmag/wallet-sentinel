from flask import Flask, render_template, request, redirect, flash, url_for
import os

# Flask_SQLAlchemy
from app.extensions import db
 
# Flask_Migrate
from app.extensions import migrations

# Db Models
from app.models import User, UserConfiguration, Operation, Saving, OperationType, Month, Currency

# Flask Debugger
from app.extensions import initialize_flask_server_debugger_if_needed

from config import TestConfig

# Flask_Login
from app.extensions import login_manager

initialize_flask_server_debugger_if_needed()

def create_app(config=None):
    app = Flask(__name__)

    if os.environ.get('FLASK_ENV') == 'production':
        app.config.from_object('config.ProductionConfig')
    elif os.environ.get('FLASK_ENV') == 'development':
        app.config.from_object('config.DevConfig')
    else:
        app.config.from_object('config.TestConfig')

    #ORM to Manage DB Models
    # flask db stamp head  -> To set the revision in the database to the head, without performing any migrations. You can change head to the required change you want.
    # flask db migrate     -> To detect automatically all the changes.
    # flask db upgrade     -> To apply all the changes.
    db.init_app(app)

    #Enabled migrations
    migrations.init_app(app, db)

    if config != TestConfig:
        with app.app_context():
            db.create_all()

    #Set the default view for not authentication requests.
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from app.models import User

    #Flask_Login method to find the active user cookie and verify it in the DB
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.views.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.views.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.views.error import errors as errors_blueprint
    app.register_blueprint(errors_blueprint)

    return app
