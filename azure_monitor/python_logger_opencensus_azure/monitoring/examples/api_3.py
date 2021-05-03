"""REST API Module using AppLogger"""
import logging
import json
from flask import Flask, jsonify
import requests
import sys 
import os
sys.path.append(os.path.join(os.getcwd(),'monitoring'))

from src.logger import AppLogger
component_name ="API_3"
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
    """End point for API3

    Returns:
        [Json]: [{'data': '<return string>'}]
    """
    logger.info("In API3 home function")

    with tracer.span("API3_Task1"):
        ret_val_1 = task1()

    with tracer.span("API3_Task2"):
        ret_val_2 = task2()

    logger.info("Calling API 2")
    response = requests.get(url='http://localhost:8100/')
    print(f"response = {response.content}")

    return jsonify({'data': 'Success API3'})

def task1():
    """Task1 function of API3

    Returns:
        [str]: [Return string]
    """
    logger.info("In API3 task1 function")
    return "task1 success!"


def task2():
    """Task1 function of API2

    Returns:
        [str]: [Return string]
    """
    logger.info("In API3 task2 function")
    return "task2 success!"

if __name__ == "__main__":
    app.run(host="localhost", port=8300,debug=True)