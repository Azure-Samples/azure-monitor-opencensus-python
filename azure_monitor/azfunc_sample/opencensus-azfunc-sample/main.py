import azure.functions as func
from opencensus.extension.azure.functions import OpenCensusExtension
from opencensus.trace import execution_context

from .globals import INSTRUMENTATION_KEY, getLogger
from .greeter_function import GreeterFunction

# configure opencensus ext for azure function.
# this ensures that the an opencensus tracer is created and associated with the func context
OpenCensusExtension.configure(connection_string=INSTRUMENTATION_KEY)

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

    return GreeterFunction.run(req)
