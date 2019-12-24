import os

basedir = os.path.abspath(os.path.dirname(__file__))

class ProductionConfig(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.environ.get('SECRET_KEY_PROD')

    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DB')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopConfig(object):
    DEBUG = True
    TESTING = True

    SECRET_KEY = os.environ.get('SECRET_KEY_DEV')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DB')

    SQLALCHEMY_TRACK_MODIFICATIONS = True