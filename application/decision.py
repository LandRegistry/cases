import requests
import json
from application import app
from requests.auth import HTTPBasicAuth

headers = {'content-type': 'application/json'}

class Decision(object):


    def __init__(self, decision_url):
        self.api = '%s/decisions' % decision_url

    def post(self, data):
        decision_response = self._post_decision(data).json()
        url = decision_response['url']
        downstream_response = self._post_downstream(url, data)
        return (decision_response, downstream_response)

    def _post_decision(self, data):
        try:
            json_data = self._payload_decision(data)
            app.logger.info("Sending data %s to the decision at %s" % (json_data, self.api))
            return requests.post(
                    self.api,
                    data=json_data,
                    headers=headers,
                    auth=HTTPBasicAuth(
                        app.config['BASIC_AUTH_USERNAME'],
                        app.config['BASIC_AUTH_PASSWORD']))
        except requests.exceptions.RequestException as e:
            app.logger.error("Could not effect decision at %s: Error %s" % (self.api, e))
            raise RuntimeError

    def _post_downstream(self, url, data):
        try:
            json_data = self._payload_downstream(data)
            app.logger.info("Sending data %s to the downstream at %s" % (json_data, url))
            return requests.post(
                    url,
                    data=json_data,
                    headers=headers,
                    auth=HTTPBasicAuth(
                        app.config['BASIC_AUTH_USERNAME'],
                        app.config['BASIC_AUTH_PASSWORD']))
        except requests.exceptions.RequestException as e:
            app.logger.error("Could not effect decision at %s: Error %s" % (self.api, e))
            raise RuntimeError

    def __repr__(self):
        return self.api

    def _payload_decision(self, data):
        return json.dumps({
               "action": "change-name-marriage",
               "data": {
                   "iso-country-code": data['marriage_country']
               },
               "context": {
                   "session-id": "123456",
                   "transaction-id": "ABCDEFG"
               }
           })

    def _payload_downstream(self, data):
        # date hack until we can settle on data formats/handling/ser/deser
        dt = data.pop('marriage_date')
        data['marriage_date'] = long(dt.strftime("%s"))

        data['application_type'] = 'change-name-marriage'
        return json.dumps(data)
