import logging

import uvicorn
from fastapi import APIRouter, FastAPI
from opencensus.trace.print_exporter import PrintExporter

from instrumentation import AzureLoggerConfig
from instrumentation.fastapi import FastapiInstrumentator

logger = logging.getLogger(__name__)
#It is must to set the logging config. One can use any known method to init this
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(message)s',
#                     handlers=[
#                               logging.StreamHandler()])
component_name = "API_1"
app = FastAPI()
#Specify exporter explicitly
# FastapiInstrumentator(app, component_name)\
#     .with_excluded_url("health").with_tracing(exporter=PrintExporter())\
#     .instrument()

#Without exporter. Defaults to PrintExporter
FastapiInstrumentator(app, component_name) \
    .with_excluded_url("health").with_tracing() \
    .instrument()

# FastapiInstrumentator(app, component_name) \
#     .with_excluded_url("health").with_tracing(
#     app_insight_connection_string="instrumentation-key",
#     azure_log_config=AzureLoggerConfig(level="INFO")) \
#     .instrument()


router = APIRouter()


@router.get("/health")
async def health():
    return "healthy"


@router.get("/")
async def main():
    logger.info("Received request")
    return "Welcome"


app.include_router(router)

if __name__ == '__main__':
    config = uvicorn.Config("azure_monitor.fastapi_logger_sample.opencensus_fastapi_examples.api_1:app", port=80,
                            log_level="info", host="0.0.0.0", workers=4)
    server = uvicorn.Server(config)
    server.run()
