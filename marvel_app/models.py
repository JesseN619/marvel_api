from flask_sqlalchemy import SQLAlchemy
import uuid
import secrets
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

db = SQLAlchemy()

ma = Marshmallow()

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True, unique = True)
    name = db.Column(db.String(150), nullable = False)
    email = db.Column(db.String(150), unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, nullable = False, unique = True)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    character = db.relationship('Character', backref = 'owner', lazy = True)

    def __init__(self, name, email, password, token = '', id = ''):
        self.id = self.set_id()
        self.name = name
        self.email = email
        self.password = self.set_password(password)
        self.token = self.get_token(24)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def get_token(self, length):
        return secrets.token_hex(length)

class Character(db.Model):
    id = db.Column(db.String, primary_key = True, unique = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    comics_appeared_in = db.Column(db.Integer, nullable = True)
    super_power = db.Column(db.String(150), nullable = True)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, comics_appeared_in, super_power, user_token, id=''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.comics_appeared_in = comics_appeared_in
        self.super_power = super_power
        self.user_token = user_token

    def set_id(self):
        return secrets.token_urlsafe()

class CharacterSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'comics_appeared_in', 'super_power']

character_schema = CharacterSchema()
characters_schema = CharacterSchema(many=True)