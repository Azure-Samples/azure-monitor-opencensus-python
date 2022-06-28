import logging
import os

from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure.log_exporter import AzureEventHandler

appKey = os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING')

logger = logging.getLogger(__name__)

logger.addHandler(AzureEventHandler(connection_string=appKey))

logger.setLevel(logging.INFO)

logger.info('Hello, World!')