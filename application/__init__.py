from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
import logging
import os


app = Flask('application.cases')
app.config.from_object(os.environ.get('SETTINGS'))

if not app.debug:
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

app.logger.info("\nConfiguration\n%s\n" % app.config)

db = SQLAlchemy(app)