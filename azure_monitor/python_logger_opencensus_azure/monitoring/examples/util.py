import logging
import sys 
import os
sys.path.append(os.path.join(os.getcwd(),'monitoring'))

from src.logger import AppLogger, get_disabled_logger
from opencensus.trace.tracer import Tracer

component_name="util"

def util_func(app_logger=get_disabled_logger(), parent_tracer=None):
    """Util function

    Args:
        app_logger (AppLogger, optional): AppLogger Object. Defaults to get_disabled_logger().
        parent_tracer (Tracer, optional): Parent tracer. Defaults to None.
    """
    logger = app_logger.get_logger(component_name=component_name)
    tracer = app_logger.get_tracer(parent_tracer=parent_tracer )
    logger.info("In util_func")
