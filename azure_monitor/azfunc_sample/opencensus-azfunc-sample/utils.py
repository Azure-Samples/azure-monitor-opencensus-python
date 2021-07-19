import time
import requests
from functools import wraps
from opencensus.trace import execution_context
from opencensus.trace.tracer import Tracer

from .globals import getLogger

logger = getLogger(__name__)


def trace_as_dependency(tracer: Tracer = None, name: str = None):
    """trace_as_dependency [method decorator to trace a method invocation as a dependency (in AppInsights)]

    Args:
        tracer (Tracer): [Opencensus tracer object used to create the trace record.]
        name (str): [Name of the created trace record]

    Returns:
        The inner function
    """

    def inner_function(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            trace_name = name if (name is not None) else method.__name__
            oc_tracer = (
                tracer
                if (tracer is not None)
                else execution_context.get_opencensus_tracer()
            )

            if oc_tracer is not None:
                with oc_tracer.span(trace_name):
                    result = method(*args, **kwargs)
            else:
                result = method(*args, **kwargs)

            return result

        return wrapper

    return inner_function


@trace_as_dependency(name="long running api call")
def call_internal_api(delay: float) -> None:
    """Dummy API call to demonstrate dependecy tracking (IN-PROC)

    Args:
        delay([float]): [Delay method execution in sec]
    """
    time.sleep(delay)


def call_external_api(url: str) -> None:
    """Dummy API call to demonstrate dependecy tracking (HTTP)

    Args:
        url([str]): [URL to invoke]
    """
    requests.get(url)
