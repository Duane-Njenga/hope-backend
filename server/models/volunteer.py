from flask import session
from server.config import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

class Volunteer(db.Model, SerializerMixin):
    __tablename__ = 'volunteers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.DateTime, default=datetime.now)
    email = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    city = db.Column(db.String)
