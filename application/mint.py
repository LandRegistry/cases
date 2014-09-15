import json
import logging
import os
import requests
from requests.auth import HTTPBasicAuth

headers = {'content-type': 'application/json'}
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class Mint(object):

    def __init__(self):
        if 'BASIC_AUTH_USERNAME' in os.environ:
            self.auth = HTTPBasicAuth(
                os.environ['BASIC_AUTH_USERNAME'],
                os.environ['BASIC_AUTH_PASSWORD'])
        else:
            self.auth = None

def post_to_mint(self, url, data, title_number):
    title_url = '%stitles/%s' % (url, title_number)
    logger.info("Sending data %s to the mint at %s" % (data, title_url))
    # try:
    #     response = requests.post(title_url, data=json.dumps(data), headers=headers)
    #     return response
    # except requests.exceptions.RequestException as e:
    #     logger.error("Could not create title number %s: Error %s" % (title_url, e))
    #     raise RuntimeError