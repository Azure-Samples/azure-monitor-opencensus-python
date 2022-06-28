import logging
import os

from opencensus.ext.azure.log_exporter import AzureLogHandler

appKey = os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING')

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string=appKey))

properties = {'custom_dimensions': {'key_1': 'value_1', 'key_2': 'value_2'}}

# Use properties in exception logs
try:
    result = 1 / 0  # generate a ZeroDivisionError
except Exception:
    logger.exception('Captured an exception.', extra=properties)