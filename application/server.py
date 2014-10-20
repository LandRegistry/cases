import json
import logging

from flask import request, jsonify, Response
from sqlalchemy.exc import IntegrityError

from application import app, service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

@app.route("/")
def index():
    return 'OK'

@app.route('/cases', methods=['POST'])
def casework_post():
    try:
        case = service.save_case(request.get_json())
    except IntegrityError:
        logger.error('Failed to save')
        return jsonify({"status": "failed to save casework item"}), 400
    except KeyError as e:
        logger.error(e.message)
        logger.error('Invalid data')
        return jsonify({"status": "invalid data"}), 400
    except Exception as e:
        logger.error(e.message)
        return jsonify({"status": "unknown Error"}), 400

    return jsonify({"status": "successful", "id": str(case.id)})

@app.route('/cases', methods=['GET'])
def get_cases():
    return Response(json.dumps([i.serialize for i in service.get_case_items()]), mimetype='application/json')


@app.route('/cases/<case_id>', methods=(['PUT']))
def update_work_queue_for_case(case_id):
    try:
        if not service.update_case_with_work_queue(case_id, request.json):
            return 'Invalid data when updating the id for case: %s' % case_id, 400
    except KeyError as e:
        return 'Invalid data when updating the id for case: %s' % case_id, 400
    return 'OK', 200


@app.route('/cases/complete/<case_id>', methods=['PUT'])
def complete_case(case_id):
    case_to_update = service.get_case(case_id)
    if case_to_update.status in ['approved', 'completed']:
        logger.error('Case: %s has already been approved' % case_id)
        return 'Case: %s has already been approved' % case_id, 400
    if not service.update_case_with_status(case_id, new_status='approved'):
        return 'Approval of the case: %s was not successful.' % case_id, 400
    return 'OK', 200


@app.route('/cases/<status>/<work_queue>', methods=['GET'])
def get_cases_by_queue(status, work_queue):
    return Response(json.dumps([i.serialize for i in service.get_cases_by_status_and_queue(status, work_queue)]), mimetype='application/json')

@app.route('/cases/property/<title_number>', methods=['GET'])
def get_cases_by_title(title_number):
    return Response(json.dumps([i.serialize for i in service.get_cases_by_title(title_number)]), mimetype='application/json')
