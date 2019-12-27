from flask import Flask, render_template, request, redirect, flash, url_for
import os

# Flask_SQLAlchemy
from app.extensions import db
 
# Flask_Migrate
from app.extensions import migrations

# Flask_Login
from app.extensions import login_manager

def create_app():
    app = Flask(__name__)

    if os.environ.get('FLASK_ENV') == 'production':
        app.config.from_object('config.ProductionConfig')
    else:
        app.config.from_object('config.DevConfig')

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

    from app.views.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.views.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app