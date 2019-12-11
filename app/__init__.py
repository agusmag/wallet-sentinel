from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app(config=None):
    app = Flask(__name__)

    #Load App Config file & Initialize Database
    if app.config["ENV"] == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopConfig")

    #ORM to Manage DB Models
    db.init_app(app)

    #Enabled migrations
    migrate = Migrate(app, db)

    #Initialize LoginManager and set the default view for not authentication requests.
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    #Flask_Login method to find the active user cookie and verify it in the DB
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #with app.app_context():
        # Imports
        #from . import routes
        #db.create_all()

    return app