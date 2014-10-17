from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
import logging
import os
from .health import Health


app = Flask(__name__)
app.config.from_object(os.environ.get('SETTINGS'))

if not app.debug:
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

app.logger.info("\nConfiguration\n%s\n" % app.config)


def health(self):
    try:
        with self.engine.connect() as c:
            c.execute('select 1=1').fetchall()
            return True, 'DB'
    except:
        return False, 'DB'

SQLAlchemy.health = health

db = SQLAlchemy(app)
Health(app, checks=[db.health])
