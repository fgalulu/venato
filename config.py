import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    FLASK_APP = os.getenv('FLASK_APP')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ECHO = True
    

class DevelopmentConfig(Config):
    DEGUB = True
    # FLASK_ENV = os.getenv('FLASK_ENV')


class TestingConfig(Config):
    SECRET_KEY = 'jfsjnfofosnf5464oeoc'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL') or 'sqlite://'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}