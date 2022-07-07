# module2.py

import logging
import os

from opencensus.trace import config_integration
from opencensus.trace.samplers import AlwaysOnSampler
from opencensus.trace.tracer import Tracer
from opencensus.ext.azure.log_exporter import AzureLogHandler

config_integration.trace_integrations(['logging'])
logging.basicConfig(format='%(asctime)s spanId=%(spanId)s %(message)s')
tracer = Tracer(sampler=AlwaysOnSampler())

logger = logging.getLogger(__name__)

appKey = os.getenv('APP_INSIGHTS_KEY')

logger.addHandler(AzureLogHandler(
    connection_string=appKey)
)

def function_1(parent_tracer=None):
    if parent_tracer is not None:
        tracer = Tracer(
                    span_context=parent_tracer.span_context,
                    sampler=AlwaysOnSampler(),
                )
    else:
        tracer = Tracer(sampler=AlwaysOnSampler())

    with tracer.span("function_1"):
        logger.info("In function_1")