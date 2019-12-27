import os

class BaseConfig:
   TESTING = False
   DEBUG = False

class DevConfig(BaseConfig):
   DEBUG = True
   #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(os.environ.get('MYSQL_USER'), os.environ.get('MYSQL_PASSWORD'), os.environ.get('MYSQL_HOSTNAME'), os.environ.get('MYSQL_DATABASE'))
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://agustinmag:password@localhost/wallet_sentinel_dev'
   SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductionConfig(BaseConfig):
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(os.environ.get('MYSQL_USER'), os.environ.get('MYSQL_PASSWORD'), os.environ.get('MYSQL_HOSTNAME'), os.environ.get('MYSQL_DATABASE'))
   SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(BaseConfig):
   TESTING = True
   DEBUG = True

   SQLALCHEMY_TRACK_MODIFICATIONS = True