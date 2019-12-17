from flask_login import UserMixin
from app import db

#The UserMixin is a module from flask_login to ease the login implementation
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    totalAmount = db.Column(db.Integer, nullable=False)
    spendLimit = db.Column(db.Float)
    warningPercent = db.Column(db.Integer)
    operations = db.relationship('Operation', backref='user', lazy=True)
    configuration = db.relationship('UserConfiguration', backref='user', lazy=True)

class UserConfiguration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    available_amount = db.Column(db.Float, nullable=False)
    main_theme = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Operation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class OperationType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '{}'.format(self.description)

class Month(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '{}'.format(self.description)