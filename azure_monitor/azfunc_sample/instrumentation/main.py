import azure.functions as func
from opencensus.extension.azure.functions import OpenCensusExtension
from opencensus.trace import execution_context

from .globals import INSTRUMENTATION_KEY, callback_add_role_name, getLogger
from .instrumentation_func import FunctionLogic

# configure opencensus ext for azure function.
# this ensures that the an opencensus tracer is created and associated with the func context
OpenCensusExtension.configure(connection_string=INSTRUMENTATION_KEY)

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

    if context.tracer is not None:  # type: ignore[attr-defined]
        # ensure the opencensus execution context use
        # the Azure function tracer (ensures that log statements)
        # have the correct correlaton (operation) id
        execution_context.set_opencensus_tracer(context.tracer)  # type: ignore[attr-defined]

    return FunctionLogic.run(req)
