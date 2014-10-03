import unittest
import json
import responses
from application.server import app
from application.decision import Decision

class TestDecisionCase(unittest.TestCase):
    CASE = {'action': 'change-name-marriage', 'data':
        '{"confirm": true, "partner_name": "Jane", "application_type": "change-name-marriage", '
        '"marriage_country": "GB", "proprietor_new_full_name": "Bob", "marriage_place": "London", '
        '"title_number": "TEST1412604722719", "proprietor_full_name": "Hank Bond", '
        '"marriage_certificate_number": "Nono", "marriage_date": 1388534400}',
            'context': {'session-id': '123456', 'transaction-id': 'ABCDEFG'}}

    @responses.activate
    def test_post(self):
        self.decision = Decision(self)
        self.decision.api = 'http://nowhere/decisions'

        responses.add(responses.POST, self.decision.api,
                      body=json.dumps({"status": "200"}), status=200, content_type='application/json')

        resp = self.decision.post(self.CASE)

        assert resp.status_code == 200