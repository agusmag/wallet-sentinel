from flask import Flask, render_template, request, redirect, flash, url_for

# Flask_SQLAlchemy
from .extensions import db
 
# Flask_Migrate
from .extensions import migrations

# Flask_Login
from .extensions import login_manager

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
    migrations.init_app(app, db)

    #Set the default view for not authentication requests.
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