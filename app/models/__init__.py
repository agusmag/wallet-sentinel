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
    totalAmount = Column(Integer, nullable=False)
    spendLimit = Column(Float)
    warningPercent = Column(Integer)
    operations = relationship('Operation', backref='user', lazy=True)
    configuration = relationship('UserConfiguration', backref='user', lazy=True)

class UserConfiguration(db.Model):
    id = Column(Integer, primary_key=True)
    available_amount = Column(Float, nullable=False)
    main_theme = Column(Boolean)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

class Operation(db.Model):
    id = Column(Integer, primary_key=True)
    description = Column(String(100), nullable=False)
    date = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    type_id = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

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