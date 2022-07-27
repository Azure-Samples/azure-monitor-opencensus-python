import logging
import os

from opencensus.ext.azure.log_exporter import AzureLogHandler

appKey = os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING')

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string=appKey))
logger.warning('Hello, World!')

logger.addHandler