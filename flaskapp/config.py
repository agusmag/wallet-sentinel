import os

class BaseConfig:
   TESTING = False
   DEBUG = False

class DevConfig(BaseConfig):
   DEBUG = True
   SECRET_KEY = "{0}dev".format(os.environ.get('SECRET_KEY'))
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(os.environ.get('MYSQL_USER'), os.environ.get('MYSQL_PASSWORD'), os.environ.get('MYSQL_HOST'), os.environ.get('MYSQL_DATABASE'))
   SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductionConfig(BaseConfig):
   SECRET_KEY = "{0}prod".format(os.environ.get('SECRET_KEY'))
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(os.environ.get('MYSQL_USER'), os.environ.get('MYSQL_PASSWORD'), os.environ.get('MYSQL_HOST'), os.environ.get('MYSQL_DATABASE'))
   SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(BaseConfig):
   TESTING = True
   DEBUG = True
   SECRET_KEY = "{0}test".format(os.environ.get('SECRET_KEY'))
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://agustinmag:password@localhost/wallet_sentinel_db_dev'
   SQLALCHEMY_TRACK_MODIFICATIONS = True