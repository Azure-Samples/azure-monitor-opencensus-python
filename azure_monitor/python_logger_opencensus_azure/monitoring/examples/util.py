import logging
import sys 
import os
sys.path.append(os.path.join(os.getcwd(),'monitoring'))

from src.logger import AppLogger
from opencensus.trace.tracer import Tracer

component_name="util"

def util_func(app_logger=None, parent_tracer=None):
    """Util function

    Args:
        app_logger (AppLogger, optional): AppLogger Object. Defaults to None.
        parent_tracer (Tracer, optional): Parent tracer. Defaults to None.
    """
    if app_logger is None:
        app_logger = AppLogger()
    logger = app_logger.get_logger(component_name=component_name)
    tracer = app_logger.get_tracer(parent_tracer=parent_tracer )
    logger.info("In util_func")
