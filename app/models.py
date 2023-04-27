from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

import uuid

db = SQLAlchemy()



class Transcription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    transcription_id= db.Column(db.String, nullable=False)
    results = db.Column(db.VARCHAR, nullable=False)
    paid =  db.Column(db.Boolean)

    def __init__(self, id, account_id, transcription_id, results, paid):
        self.id = id
        self.account_id = account_id
        self.transcription_id = transcription_id
        self.results = results
        self.paid = paid
        



   