import logging
import requests
from werkzeug.exceptions import abort

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())


def get_title(search_url, title_number):
    title_url = "%s/%s/%s" % (
        search_url,
        'auth/titles',
        title_number)
    logger.debug("Requesting title url : %s" % title_url)
    try:
        response = requests.get(title_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error("HTTP Error %s", e)
        abort(response.status_code)
    except requests.exceptions.ConnectionError as e:
        logger.error("Error %s", e)
        abort(500)


def apply_change(current_title, change):
    logger.info('Dealing with: %s' % type(change))
    old_name = change['proprietor_full_name']
    proprietors = current_title['proprietorship']['fields']['proprietors']
    for x in proprietors:
        if x['name']['full_name'] == old_name:
            x['name']['full_name'] = change['proprietor_new_full_name']
            return current_title
    return None