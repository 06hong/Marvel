from enum import unique
from flask_sqlalchemy import SQLAlchemy
import uuid
import secrets
from datetime import datetime 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow

login_manager = LoginManager()
ma = Marshmallow()
@login_manager.user_loader
def load_user(user_id): #when someone logs in
    return User.query.get(user_id) #query data for that id

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key= True, unique = True)
    email = db.Column(db.String(150), unique = True, nullable= False)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, nullable = False, unique=True)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    marvel = db.relationship('Marvel', backref = 'owner', lazy = True) #every person does nesscary have a relationship with marvel

    def __init__(self, email, password, token = '', id=''):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.token = self.get_token(24)

    def set_id(self):
        return str(uuid.uuid4()) #look at self.id

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def get_token(self, length):
        return secrets.token_hex(length)

#class for marvel table
class Marvel(db.Model):
    id = db.Column(db.String, primary_key= True, unique = True)
    name = db.Column(db.String, nullable= False)
    powers = db.Column(db.String, nullable = True)
    traits = db.Column(db.String, nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False) #user.token

    def __init__(self, name, powers, traits, user_token, id= ''):
        self.id = self.set_id()
        self.name = name
        self.powers = powers
        self.traits = traits
        self.user_token = user_token

    def set_id(self):
        return str(uuid.uuid4())

# model in flash (class inpython)
class MarvelSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'powers', 'traits', 'user_token']

#Create a singular data point return
marvel_schema = MarvelSchema()

#Create mutiple data point return
marvel_schema = MarvelSchema(many=True)
    

