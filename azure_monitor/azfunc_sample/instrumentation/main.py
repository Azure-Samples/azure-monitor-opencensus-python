import azure.functions as func
from opencensus.extension.azure.functions import OpenCensusExtension

from .globals import AI_CONNECTION_STRING, callback_add_role_name, getLogger
from .instrumentation_func import FunctionLogic

# configure opencensus ext for azure function.
# this ensures that the an opencensus tracer is created and associated with the func context
OpenCensusExtension.configure(connection_string=AI_CONNECTION_STRING)

# ensure that dependency records have the correct role name
OpenCensusExtension._exporter.add_telemetry_processor(callback_add_role_name)

logger = getLogger(__name__)


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """Azure Function entry point

    Args:
        req([HttpRequest]): [Incoming HTTP request]
        context([Context]): [Azure function invocation context]
    """
    logger.info("Python HTTP trigger function processed a request.")

    return FunctionLogic.run(req)
