"""REST API Module using AppLogger"""

import json
from flask import Flask, jsonify
import sys 
import os
sys.path.append(os.path.join(os.getcwd(),'monitoring'))

from src.logger import AppLogger, get_disabled_logger
component_name ="API_1"

logger = get_disabled_logger().get_logger(component_name=component_name)

app = Flask(component_name)

@app.route('/', methods=['GET'])
def home():
    """End point for API1

    Returns:
        [Json]: [{'data': '<return string>'}]
    """
    logger.info("In API1 home function")
    return jsonify({'data': 'Success API1'})

app.run(host="localhost", port=8000, debug=True)
