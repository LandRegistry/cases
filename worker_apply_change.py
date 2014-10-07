from application import service
import time
import logging
import os
import json

from application.mint import Mint
from application.modify_titles import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())

mint_url = os.environ['MINT_URL']
mint = Mint()

search_url = os.environ['SEARCH_URL']


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
        case_id = case.id
        service.update_case_with_status(case_id, 'wait')

        d = json.loads(case.serialize['request_details'])
        title_number = json.loads(d['data'])['title_number']
        title = get_title(search_url, title_number)
        changed_title = apply_change(title, json.loads(d['data']))

        logger.debug("Sending case to mint to apply change: %s for title:%s" % (case.id, d))
        if changed_title:
            changed_title_with_mod_date = apply_edition_date(changed_title)
            response = mint.post(mint_url, changed_title_with_mod_date, case.title_number)
            logger.info("mint response:: %s" % response.status_code)
            if response and response.status_code / 100 == 2:
                service.update_case_with_status(case_id, 'completed')
            else:
                service.update_case_with_status(case_id, 'error')
                logger.error("Failure when posting to mint, case id %s" % case_id)
        else:
            #TODO: If an update results in error it will show up on the casework list page, however, we do not tell the casework this it is in error or why it is in error.
            service.update_case_with_status(case_id, 'error')
            logger.error("Failure when posting to mint, case id %s. Unable to find the name in the title to edit." % case_id)



if __name__ == '__main__':
    process_approved_cases()
