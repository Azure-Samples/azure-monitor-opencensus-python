"""REST API Module using AppLogger"""

import json
import logging
from flask import Flask, jsonify
import sys 
import os
import time
sys.path.append(os.path.join(os.getcwd(),'monitoring'))

from src.logger import AppLogger
component_name ="API_4"
app = Flask(component_name)

logging_config_file_path = os.path.join(os.getcwd(),'monitoring',"examples","logging_config.json")
with open(logging_config_file_path) as logging_config_file:
        logging_config = json.load(logging_config_file)
app_logger = AppLogger(config=logging_config)

app_logger.enable_flask(flask_app=app,component_name= component_name)
event_logger = app_logger.get_event_logger(component_name=component_name)

@app.route('/', methods=['GET'])
def home():
    """End point for API4

    Returns:
        [Json]: [{'data': '<return string>'}]
    """
    #Plain Event
    event_logger.info("Start_API4")

    start_time = time.time()
    jsonified_data= jsonify({'data': 'Success API4'})

    execution_time=time.time() - start_time
    extra_params = {"custom_dimensions": {"execution_time":execution_time}}

    #Event with an additional custom dimension execution_time
    event_logger.info("API4_Execution_Time", extra=extra_params)

    extra_params = {"custom_dimensions": {"response":jsonified_data}}

    #Event with an additional custom dimension with json value
    event_logger.info("API4_Return_Json", extra=extra_params)

    return jsonified_data

app.run(host="localhost", port=8100, debug=True)
