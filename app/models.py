from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid




db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, unique=True, index=True, primary_key=True)
    uid = db.Column(db.String(150), nullable=False, unique=True, index=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    container_name = db.Column(UUID(as_uuid=True), default=uuid.uuid4)

    def __init__(self, uid, name, email):
        self.uid = uid
        self.name=name  
        self.email=email    

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
            'name':self.name,
            'email': self.email
        }


class Transcription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.VARCHAR, nullable=False)
    paid =  db.Column(db.Boolean)
    filename = db.Column(db.VARCHAR, nullable=False)
    user_uid = db.Column(db.String, db.ForeignKey('user.uid'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, body, paid, filename, user_uid):
        self.body = body
        self.paid = paid
        self.user_uid = user_uid
        self.filename = filename

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
            'body' : self.body,
            'paid' : self.paid,
            'filename': self.filename,
            'user': self.user_uid
        }
