import logging
import unittest

from opencensus.trace import execution_context, Span

from instrumentation.task import with_tracing, TaskInstrumentator

logging.basicConfig(
    level=logging.INFO
)

log=logging.getLogger("testlog")
log.addHandler(logging.StreamHandler())

@with_tracing
def call_hello_world():
    log.warning("Calling hello world")
    current_span:Span=execution_context.get_current_span()
    return current_span.context_tracer.trace_id,current_span.span_id


class TestLogger(unittest.TestCase):
    def test_logger(self):
        TaskInstrumentator(component_name="batch-task").with_tracing().instrument()
        call_hello_world()




