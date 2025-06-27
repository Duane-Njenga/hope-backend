from server.config import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

class Project(db.Model, SerializerMixin):
    __tablename__ = 'projects'

    serialize_rules = ('-volunteers.project',) 

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)  
    date = db.Column(db.DateTime, default=datetime.now)
    description = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=False)

    volunteers = db.relationship('Volunteer', back_populates='project', lazy=True)

    def __repr__(self):
        return f'<Project {self.type} - ID: {self.id}>'
