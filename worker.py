from application import service
import time
import logging
import os
import json

from application.decision import Decision

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())

decision = Decision(os.environ['DECISION_URL'])


def process_pending_cases():
    while 1:

        time.sleep(5)

        try:
            case = service.get_next_pending_case()
            handle_case(case)
            
        except Exception, e:
            logger.error(e)

def handle_case(case):
    if case:
        logger.debug("Sending case to decision: %s" % case.serialize)
        details = json.loads(case.serialize['request_details'])
        logger.info('request details %s , %s' % (type(details), details))
        decision_response, downstream_response, work_queue = decision.post(details)
        logger.info("Downstream response: %s" % downstream_response)
        if decision_response and downstream_response and downstream_response.status_code / 100 == 2:
            service.update_case_with_dict(case.title_number, {'work_queue': work_queue, 'status': 'queued'})
        else:
            logger.error("Failure when posting to decision, details = %s" % details)


if __name__ == '__main__':
    process_pending_cases()
