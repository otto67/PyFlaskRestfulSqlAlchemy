from flask_login import UserMixin
from . import db
# Database rows
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    admin = db.Column(db.Boolean)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)
