"""REST API Module using AppLogger"""

import json
from flask import Flask, jsonify
import sys 
import os
sys.path.append(os.path.join(os.getcwd(),'monitoring'))

from src.logger import AppLogger
component_name ="API_1"

logging_config_file_path = os.path.join(os.getcwd(),'monitoring',"examples","logging_disabled_config.json")
with open(logging_config_file_path) as logging_config_file:
        logging_config = json.load(logging_config_file)
logger = AppLogger(config=logging_config).get_logger(component_name=component_name)
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
