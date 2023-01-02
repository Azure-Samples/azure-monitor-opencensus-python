import logging

from instrumentation import AzureLoggerConfig
from instrumentation.task import TaskInstrumentator, with_tracing

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] traceId=%(traceId)s spanId=%(spanId)s  %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

log=logging.getLogger(__name__)

TaskInstrumentator(component_name="batch-task").with_tracing(app_insight_connection_string="InstrumentationKey=535b709e-f3c8-46ca-b0f9-3bdb3c80dd7f;IngestionEndpoint=https"
                                                                                           "://centralindia-0.in.applicationinsights.azure.com/;LiveEndpoint=https"
                                                                                           "://centralindia.livediagnostics.monitor.azure.com/", azure_log_config=AzureLoggerConfig(level="INFO")).instrument()

@with_tracing
def process_and_trace():
    log.info("Called process and trace")


if __name__ == '__main__':
    process_and_trace()