class Config:
    ENV = 'dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@localhost/flask_workout'
    SECRET_KEY = 'secret'
    DEBUG = True
