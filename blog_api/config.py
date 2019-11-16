import os

class Config:
    ENV = 'development'
    SECRET_KEY = 'zzr'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SERVER_NAME = '0.0.0.0'
    # SQLALCHEMY_POOL_TIMEOUT = 10
    # SQLALCHEMY_MAX_OVERFLOW = 20
    #配置email
    # MAIL_SERVER = 'smtp.163.com'
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('EMAIL_USER')
    # MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

key = Config().SECRET_KEY