import os 

basedir = os.path.abspath(os.path.dirname(__file__))

class Config: 
    SECRET_KEY = '1234'
    WTF_CSRF_TIME_LIMIT= None
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True 


class TestingConfig(Config):
    TESTING = True 


config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'default': DevelopmentConfig
}