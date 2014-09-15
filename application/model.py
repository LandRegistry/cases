import datetime
import json
import logging
from pytz import timezone
from sqlalchemy import TEXT

from application import db

class Case(db.Model):
    __tablename__ = 'cases'

    id = db.Column(db.Integer, primary_key=True)
    title_number = db.Column(db.String(64), nullable=False)
    application_type = db.Column(db.String(50), nullable=False)
    request_details = db.Column(TEXT) #nullable    # TODO: should be a JSON
    status = db.Column(db.String(100)) #pending/complete
    work_queue = db.Column(db.String(100))
    submitted_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    submitted_by = db.Column(db.String(200))

    @property
    def submitted_at_bst(self):
        utc = timezone('UTC').localize(self.submitted_at)
        bst = timezone('Europe/London').localize(self.submitted_at)
        return bst + (utc - bst)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'title_number': self.title_number,
            'application_type': self.application_type,
            'request_details' : json.loads(self.request_details),
            'request_details_data' : json.loads((json.loads(self.request_details))['data']),
            'status' : self.status,
            'work_queue' : self.work_queue,
            'submitted_by': self.submitted_by,
            'submitted_at': datetime.datetime.strftime(self.submitted_at, '%d-%m-%Y %H:%M:%S %f')
        }


