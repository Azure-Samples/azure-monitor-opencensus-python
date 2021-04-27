"""REST API Module using AppLogger"""

import json
import logging
from flask import Flask, jsonify
import sys 
import os
sys.path.append(os.path.join(os.getcwd(),'monitoring'))

from src.logger import AppLogger
component_name ="API_2"
app = Flask(component_name)

logging_config_file_path = os.path.join(os.getcwd(),'monitoring',"examples","logging_config.json")
with open(logging_config_file_path) as logging_config_file:
        logging_config = json.load(logging_config_file)
app_logger = AppLogger(config=logging_config)

app_logger.enable_flask(flask_app=app,component_name= component_name)
logger = app_logger.get_logger(component_name=component_name)
tracer = app_logger.get_tracer(component_name=component_name)

@app.route('/', methods=['GET'])
def home():
    """End point for API2

    Returns:
        [Json]: [{'data': '<return string>'}]
    """
    logger.info("In API2 home function")
    return jsonify({'data': 'Success API2'})

app.run(host="localhost", port=8100, debug=True)
