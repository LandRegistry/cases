from application import service
import time
import logging
import os
import json

from application.decision import Decision
from application.mint import Mint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())

mint_url = os.environ['MINT_URL']
mint = Mint()


def process_approved_cases():
    while 1:

        time.sleep(1)

        try:
            case = service.get_next_approved_case()
            submit_change_to_mint(case)

        except Exception, e:
            logger.error(e)

def submit_change_to_mint(case):
    if case:
        #TODO: add title to case
        case_id = case.id
        service.update_case_with_status(case_id, 'wait')

        d = json.loads(case.serialize['request_details'])
        title = json.loads(d['data'])['title']

        logger.info("Sending case to mint to apply change: %s for title:%s" % (case.id, d))
        logger.info("title: %s" % title)

        response = mint.post(mint_url, title, case.title_number)
        logger.info("mint response:: %s" % response.status_code)
        if response and response.status_code / 100 == 2:
            service.update_case_with_status(case_id, 'completed')
        else:
            service.update_case_with_status(case_id, 'error')
            logger.error("Failure when posting to mint, case id " % case_id)


if __name__ == '__main__':
    process_approved_cases()
