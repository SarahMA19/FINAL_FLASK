from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

import uuid

db = SQLAlchemy()


class Transcription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transcription_id= db.Column(db.String, nullable=False)
    results = db.Column(db.VARCHAR, nullable=False)
    paid =  db.Column(db.Boolean)
    user_uid = db.Column(db.String, db.ForeignKey('user.uid'), nullable=False)
    user = db.relationship('User', backref=db.backref('user', lazy=True))

    def __init__(self, transcription_id, results, paid, user_uid):
        self.transcription_id = transcription_id
        self.results = results
        self.paid = paid
        self.user_uid = user_uid

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def to_dict(self):
        return {
            'id': self.id,
            'transcription_id': self.transcription_id,
            'results' : self.results,
            'paid' : self.paid,
            'user': self.user.to_dict()
        }



class User(db.Model):
    id = db.Column(db.Integer, unique=True, index=True, primary_key=True)
    uid = db.Column(db.String(150), nullable=False, unique=True, index=True)
    name = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, uid, name):
        self.uid = uid
        self.name = name
        

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def to_dict(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'name': self.name,
            'created_at' : self.created_at
        }

