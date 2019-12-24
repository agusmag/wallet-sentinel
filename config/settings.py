class BaseConfig():
   TESTING = False
   DEBUG = False

class DevConfig(BaseConfig):
   FLASK_ENV = 'development'
   DEBUG = True
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:adminpassword@localhost/wallet_sentinel_dev'
   CELERY_BROKER = 'pyamqp://client:client@broker-rabbitmq//'
   CELERY_RESULT_BACKEND = 'rpc://client:client@broker-rabbitmq//'

   SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(BaseConfig):
   FLASK_ENV = 'production'
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:adminpassword@localhost/wallet_sentinel_prod'
   CELERY_BROKER = 'pyamqp://rabbit_user:rabbit_password@broker-rabbitmq//'
   CELERY_RESULT_BACKEND = 'rpc://rabbit_user:rabbit_password@broker-rabbitmq//'

   SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(BaseConfig):
   FLASK_ENV = 'development'
   TESTING = True
   DEBUG = True

   SQLALCHEMY_TRACK_MODIFICATIONS = True
   
   # Make celery execute tasks synchronously in the same process
   CELERY_ALWAYS_EAGER = True