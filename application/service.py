import logging

from application import db
from application.model import Case


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


def save_case(data):
    logger.info("Received POST new case. %s" % data)
    case = Case()
    case.title_number = data.get('title_number')
    case.application_type = data.get('application_type')
    case.request_details = data.get('request_details')
    case.status = 'pending'
    q = data.get('work_queue', None)
    if q:
        case.work_queue = q
    case.submitted_by = data.get('submitted_by')

    db.session.add(case)
    db.session.commit()


def get_case_items():
    return Case.query.order_by(Case.submitted_at).all()

def update_case_with_work_queue(title_number, data):
    logger.info("Received update for case %s, set work_queue to %s" % (title_number, data))
    q = data.get('work_queue', None)
    if not q:
        return False

    Case.query.filter_by(title_number=title_number).update(dict(work_queue=q))
    db.session.commit()
    return True

def update_case_with_status(title_number, new_status):
    logger.info("Received update for case: %s, set status to %s" % (title_number, new_status))
    if not new_status:
        return False

    Case.query.filter_by(title_number=title_number).update(dict(status=new_status))
    db.session.commit()
    return True


