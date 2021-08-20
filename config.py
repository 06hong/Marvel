import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY= 'You shall not pass'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') #keep this a scret
    SQLALCHEMY_TRACK_MODIFICATIONS = False 