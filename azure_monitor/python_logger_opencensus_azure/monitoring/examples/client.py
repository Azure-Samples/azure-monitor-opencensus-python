""""REST API Client Module using AppLogger"""
import requests
import logging
import sys 
import os
import pathlib
import json
sys.path.append(os.path.join(os.getcwd(),'monitoring'))

from src.logger import AppLogger
from util import util_func

component_name = "client"

logging_config_file_path = os.path.join(os.getcwd(),'monitoring',"examples","logging_config.json")
with open(logging_config_file_path) as logging_config_file:
        logging_config = json.load(logging_config_file)

app_logger = AppLogger(config=logging_config)
logger = app_logger.get_logger(component_name=component_name)
tracer = app_logger.get_tracer(component_name=component_name)

def call_api_3():
    """Function calling endpoint of API3
    """
    logger.info("Calling api 3")
    response = requests.get(url='http://localhost:8300/')
    print(f"response = {response.content}")

    with tracer.span("util_func"):
        util_func(app_logger=app_logger,parent_tracer=tracer)

if __name__ == '__main__':
    call_api_3()