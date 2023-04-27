from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


class Transcription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Guid, nullable=False)
    transcription_id= db.Column(db.String, nullable=False)
    results = db.Column(db.VARCHAR(10), nullable=False)
    paid =  db.Column(db.Boolean)

    def __init__(self, id, account_id, transcription_id, results, paid):
        self.id = id
        self.account_id = account_id
        self.transcription_id = transcription_id
        self.results = results
        self.paid = paid
        



   