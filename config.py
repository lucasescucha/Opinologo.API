import os

class Config:
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    
    db_user = os.getenv('DB_USER')    
    db_pass = os.getenv('DB_PASS')

    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')

    SQLALCHEMY_DATABASE_URI = 'mysql://{db_user}:{db_pass}@{db_host}:{db_port}/opinologo'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    JSON_AS_ASCII = False

config = {
    'development': DevelopmentConfig,
}

currentConfig = config['development']