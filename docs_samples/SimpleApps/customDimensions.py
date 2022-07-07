import logging
import os

from opencensus.ext.azure.log_exporter import AzureLogHandler

logger = logging.getLogger(__name__)

appKey = os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING')

logger.addHandler(AzureLogHandler(
    connection_string=appKey)
)

properties = {'custom_dimensions': {'key_1': 'value_1', 'key_2': 'value_2'}}

# Use properties in logging statements
logger.warning('action', extra=properties)