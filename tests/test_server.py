import unittest
from application.server import app
from application import db


class CasesServerTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        db.create_all()
        self.app = app
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_check_server(self):
        rv = self.client.get('/cases')
        self.assertEquals(rv.status, '200 OK')

        rv = self.client.get('/pagedoesnotexist')
        self.assertEqual(rv.status, '404 NOT FOUND')

        rv = self.client.get('/')
        self.assertEqual(rv.status, '200 OK')
