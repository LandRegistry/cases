import datetime

from application import db

class Cases(db.Model):
    __tablename__ = 'cases'

    id = db.Column(db.Integer, primary_key=True)
    title_number = db.Column(db.String(64), nullable=False)
    submitted_at = db.Column(db.DateTime(), default=datetime.datetime.now)
    application_type = db.Column(db.String(50), nullable=False)