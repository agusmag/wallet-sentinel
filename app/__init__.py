from flask import Flask, render_template, request, redirect, flash, url_for

# SQLAlchemy
from sqlalchemy import event, DDL
from flask_sqlalchemy import SQLAlchemy
 
# Flask_Login
from flask_login import LoginManager

# Flask_Migrate
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


    # Models
    from .models import Month, OperationType
    
    # Populate default info in the DB
    # event.listen(Month.__table__, 'after_create',
    #         DDL(""" INSERT INTO month (id, description) 
    #                     VALUES  (1, 'Enero')        ,
    #                             (2, 'Febrero')      ,
    #                             (3, 'Marzo')        ,
    #                             (4, 'Abril')        ,
    #                             (5, 'Mayo')         ,
    #                             (6, 'Junio')        ,
    #                             (7, 'Julio')        ,
    #                             (8, 'Agosto')       ,
    #                             (9, 'Septiembre')   ,
    #                             (10, 'Octubre')     ,
    #                             (11, 'Noviembre')   ,
    #                             (12, 'Diciembre')   
    #             """))
    
    # event.listen(OperationType.__table__, 'after_create',
    #         DDL(""" INSERT INTO operation_type (id, description) 
    #                     VALUES  (1, 'Indumentaria') ,
    #                             (2, 'Comida')       ,
    #                             (3, 'Impuesto')     ,
    #                             (4, 'Regalo')       ,
    #                             (5, 'Tecnología')   ,
    #                             (6, 'Mueble')       ,
    #                             (7, 'Decoración')   ,
    #                             (8, 'Cuota')        ,
    #                             (9, 'Belleza')      ,
    #                             (10, 'Higiene')     
    #             """))

    #with app.app_context():
        # Imports
        #from . import routes
        #db.create_all()

    return app