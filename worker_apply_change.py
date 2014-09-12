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

mint = Mint(os.environ['MINT_URL'])


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
        logger.info("Sending case to mint to apply change: %s" % case.id)
        #TODO: add title to case
        #title = case['title_number']
        #case_id = case['id']

        # response, work_queue = mint.post(title)
        # if response and response.status_code / 100 == 2:
        #     service.update_case_with_status(case_id, 'completed')
        # else:
        #     logger.error("Failure when posting to mint, case id " % case_id)


if __name__ == '__main__':
    process_approved_cases()
