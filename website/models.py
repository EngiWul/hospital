from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    doc = db.Column(db.String(150))
    docfio = db.Column(db.String(150))
    diagnoz = db.Column(db.String(150))
    zhaloby = db.Column(db.String(150))
    date = db.Column(db.String(150))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    second_name = db.Column(db.String(150))
    third_name = db.Column(db.String(150))
    iin = db.Column(db.String(50))
    address = db.Column(db.String(150))
    phone_num = db.Column(db.String(150))
    notes = db.relationship('Note')
