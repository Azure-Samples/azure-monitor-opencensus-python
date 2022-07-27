# module1.py
import logging
import os

from opencensus.trace import config_integration
from opencensus.trace.samplers import AlwaysOnSampler
from opencensus.trace.tracer import Tracer
from opencensus.ext.azure.log_exporter import AzureLogHandler
from module2 import function_1

config_integration.trace_integrations(['logging'])
logging.basicConfig(format='%(asctime)s spanId=%(spanId)s %(message)s')
tracer = Tracer(sampler=AlwaysOnSampler())

logger = logging.getLogger(__name__)

appKey = os.getenv('APP_INSIGHTS_KEY')

logger.addHandler(AzureLogHandler(
    connection_string=appKey)
)

logger.warning('Before the span')

with tracer.span(name='hello'):
   logger.warning('In the span')
   function_1(tracer)

logger.warning('After the span')