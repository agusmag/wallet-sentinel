from flask_login import UserMixin

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import db

#The UserMixin is a module from flask_login to ease the login implementation
class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    operations = relationship('Operation', backref='user', lazy=True)
    configuration = relationship('UserConfiguration', backref='user', lazy=True)

class UserConfiguration(db.Model):
    id = Column(Integer, primary_key=True)
    spend_limit = Column(Float)
    warning_percent = Column(Integer)
    hide_amounts = Column(Boolean)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    exchange_rates = Column(String(100), nullable=True)

class Operation(db.Model):
    id = Column(Integer, primary_key=True)
    description = Column(String(100), nullable=False)
    date = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    type_id = Column(Integer, ForeignKey('operation_type.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=True)
    from_saving = Column(Boolean)

class Saving(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=False)
    amount = Column(Float, nullable=False)

class OperationType(db.Model):
    id = Column(Integer, primary_key=True)
    description = Column(String(200), nullable=False)

    def __repr__(self):
        return '{}'.format(self.description)

class Month(db.Model):
    id = Column(Integer, primary_key=True)
    description = Column(String(50), nullable=False)

    def __repr__(self):
        return '{}'.format(self.description)

class Currency(db.Model):
    id = Column(Integer, primary_key=True)
    code = Column(Integer, nullable=False)
    description = Column(String(50), nullable=False)
    symbol = Column(String(3), nullable=True)

    def __repr__(self):
        return '{}'.format(self.description)
