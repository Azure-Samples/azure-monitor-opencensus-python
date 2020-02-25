import json
import logging

from endpoint import endpoint_app
from flask import make_response, request

logger = logging.getLogger(__name__)


@endpoint_app.route('/api/save', methods=['POST'])
def save_tasks():
    try:
        data = json.loads(request.data)
        with open('./output/file.txt', 'w') as file:
            for item in data:
                file.write(item)
                file.write('\n')
    except Exception as ex:
        logger.exception("Exception occurred while saving: ")
        return make_response("Server exception: " + ex, 500)
    return request.data
