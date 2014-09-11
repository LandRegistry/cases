import requests
import json
from application import app
from requests.auth import HTTPBasicAuth
import os
import string

headers = {'content-type': 'application/json'}


class Decision(object):

    def __init__(self, decision_url):
        self.api = '%s/decisions' % decision_url
        if 'BASIC_AUTH_USERNAME' in os.environ:
            self.auth = HTTPBasicAuth(
                        os.environ['BASIC_AUTH_USERNAME'],
                        os.environ['BASIC_AUTH_PASSWORD'])
        else:
            self.auth = None

    def post(self, data):
        decision_response = self._post_decision(data)
        url = decision_response.json()['url']
        work_queue = string.split(url, '/')[3]
        return (decision_response, work_queue)

    def _post_decision(self, data):
        try:
            json_data = self._payload_decision(data)
            app.logger.info("Sending data %s to the decision at %s" % (json_data, self.api))
            return requests.post(
                    self.api,
                    data=json_data,
                    headers=headers,
                    auth=self.auth)
        except requests.exceptions.RequestException as e:
            app.logger.error("Could not effect decision at %s: Error %s" % (self.api, e))
            raise RuntimeError

    def __repr__(self):
        return self.api

    def _payload_decision(self, data):
        payload = json.loads(data['data'])
        return json.dumps({
               "action": data['action'],
               "data": {
                   "iso-country-code": payload['marriage_country']
               },
               "context": {
                   "session-id": "123456",
                   "transaction-id": "ABCDEFG"
               }
           })
