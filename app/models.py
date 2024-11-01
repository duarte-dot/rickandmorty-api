from datetime import datetime, timezone
from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    created = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Character(db.Model):
    __tablename__ = 'characters'

    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=True)
    species = db.Column(db.String(50), nullable=True)
    type = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    origin = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    episodes = db.Column(db.Text, nullable=True)
    url = db.Column(db.String(255), nullable=True)
    created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
