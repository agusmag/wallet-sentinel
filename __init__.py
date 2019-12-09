from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#ORM to Manage DB Models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    #MySQL Connection with SQLAlchemy
    app.config['SECRET_KEY'] = 'thisismysecretkeycustompython'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://agustinmag:password@localhost/wallet_centinel_db'

    db.init_app(app)

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

    return app