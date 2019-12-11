import os

basedir = os.path.abspath(os.path.dirname(__file__))
prodDB = 'mysql+pymysql://agustinmag:password@localhost/wallet_sentinel_db_prod'
devDB = 'mysql+pymysql://agustinmag:password@localhost/wallet_sentinel_db_dev'
testDB = 'mysql+pymysql://agustinmag:password@localhost/wallet_sentinel_db_test'

class ProductionConfig(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = 'you-will-never-guess-prod'

    SQLALCHEMY_DATABASE_URI = prodDB

    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopConfig(object):
    DEBUG = True
    TESTING = False

    SECRET_KEY = 'you-will-never-guess-dev'

    SQLALCHEMY_DATABASE_URI = devDB

    SQLALCHEMY_TRACK_MODIFICATIONS = True