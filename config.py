import os 

basedir = os.path.abspath(os.path.dirname(__file__))

class Config: 
    SECRET_KEY = '1234'
    WTF_CSRF_TIME_LIMIT= None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '/sqlite/tripadvisor')


class TestingConfig(Config):
    TESTING = True 
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'default': DevelopmentConfig
}