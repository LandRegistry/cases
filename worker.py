from application import service
import time
import logging
import os

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
        logger.info("Sending case to decision: %s" % case)
        decision_response, downstream_response = decision.post(case.serialize())
        logger.info("Downstream response %s" % downstream_response)
        if decision_response and downstream_response:
            logger.info("Dunno")
        else:
            logger.error("Failure")


if __name__ == '__main__':
    process_pending_cases()
