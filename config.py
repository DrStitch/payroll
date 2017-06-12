class Config(object):
    DEBUG = False
    TESTING = False
    # change next line to make DATABASE available
    DATABASE = 'dbname= user= password= host= port= '

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
