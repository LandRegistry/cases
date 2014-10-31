from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
import logging
import os
from .health import Health

app = Flask(__name__)
app.config.from_object(os.environ.get('SETTINGS'))

from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)

if not app.debug:
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

app.logger.debug("\nConfiguration\n%s\n" % app.config)

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
