import os
import unittest

import mock
from opencensus.trace import execution_context, Span

from instrumentation.task import TaskInstrumentator, with_tracing, TRACE_ID_PARAM


@with_tracing
def call_hello_world():
    current_span:Span=execution_context.get_current_span()
    return current_span.context_tracer.trace_id,current_span.span_id
trace_id = '11111111111111111111111111111111'
span_id = '9999999999999999'
formatted_trace_id = '00-{}-{}-00'.format(trace_id, span_id)

class TestTask(unittest.TestCase):
    def test_instrumentation(self):
        TaskInstrumentator(component_name="batch-task").with_tracing().instrument()
        trace_id,span_id=call_hello_world()
        self.assertIsNotNone(trace_id)
        self.assertIsNotNone(span_id)
    @mock.patch.dict(os.environ, {TRACE_ID_PARAM: formatted_trace_id})
    def test_instrumentation_with_preset_value(self):
        TaskInstrumentator(component_name="batch-task").with_tracing().instrument()

        t, s = call_hello_world()
        self.assertEqual(t,trace_id)


