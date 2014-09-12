import os
from requests.auth import HTTPBasicAuth

headers = {'content-type': 'application/json'}


class Mint(object):

    def __init__(self, decision_url):
        self.api = '%s/decisions' % decision_url
        if 'BASIC_AUTH_USERNAME' in os.environ:
            self.auth = HTTPBasicAuth(
                os.environ['BASIC_AUTH_USERNAME'],
                os.environ['BASIC_AUTH_PASSWORD'])
        else:
            self.auth = None

    def post(self, data):
        return True