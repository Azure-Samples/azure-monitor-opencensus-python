__path__ = __import__("pkgutil").extend_path(__path__, __name__)

import functools
import os
import re

from opencensus.trace import span as span_module, Span
from opencensus.trace.print_exporter import PrintExporter
from opencensus.trace.propagation.trace_context_http_header_format import (
    TraceContextPropagator,
)
from opencensus.trace.samplers import AlwaysOnSampler
from opencensus.trace.span_context import SpanContext
from opencensus.trace.trace_options import TraceOptions
from opencensus.trace.tracer import Tracer

from instrumentation import BaseIntrumentator, handle_exception


TRACE_ID_PARAM = "traceparent"
SPAN_ID_PARAM = "spanId"
_TRACEPARENT_HEADER_FORMAT = (
    "^[ \t]*([0-9a-f]{2})-([0-9a-f]{32})-([0-9a-f]{16})-([0-9a-f]{2})" + "(-.*)?[ \t]*$"
)
_TRACE_CONTEXT_HEADER_RE = re.compile(_TRACEPARENT_HEADER_FORMAT)

is_instrumented = False
sampler = None
exporter = None
propagator = None
instrumentator: BaseIntrumentator = None

def add_additional_attributes(span, *args, **kwargs):
    span.span_kind = span_module.SpanKind.SERVER


def with_tracing(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        trace: Tracer = instrumentator.init_tracing(args, kwargs)
        span: Span = trace.span(name=f"{instrumentator.component_name}.{func.__name__}")
        # if we put server in span_kind then it will show up in application map but won't show as dependency in
        # transaction search.
        # trace.span_kind = SpanKind.SERVER
        # span.span_kind = SpanKind.SERVER
        try:
            instrumentator.add_azure_log_handler()
            return_value = func(*args, **kwargs)
        except Exception as exp:
            handle_exception(span, exp)
            trace.end_span()
            trace.finish()
            raise exp
        trace.end_span()
        trace.finish()
        return return_value

    return wrapper


class ArgumentPropagator(TraceContextPropagator):
    def __init__(self) -> None:
        super().__init__()

    def from_arugments(self):
        trace_id_param = os.getenv(TRACE_ID_PARAM)
        if trace_id_param is None:
            return SpanContext()
        try:
            match = re.search(_TRACE_CONTEXT_HEADER_RE, trace_id_param)
            version = match.group(1)
            trace_id = match.group(2)
            span_id = match.group(3)
            trace_options = match.group(4)
            if trace_options is None:
                trace_options = 1

            if trace_id == "0" * 32 or span_id == "0" * 16:
                return SpanContext()

            if version == "00":
                if match.group(5):
                    return SpanContext()
            if version == "ff":
                return SpanContext()

            span_context = SpanContext(
                trace_id=trace_id,
                span_id=span_id,
                trace_options=TraceOptions(trace_options),
                from_header=False,
            )
            return span_context
        except TypeError:
            # logger.warning("invalid value ", trace_id_param)
            return SpanContext()


class BatchInstrumentator(BaseIntrumentator):
    def __init__(
        self,
        component_name=None,
        sampler=AlwaysOnSampler(),
        exporter=PrintExporter,
        propogator=ArgumentPropagator(),
    ):

        super().__init__(
            component_name,
            sampler,
            exporter,
            propogator,
        )

    def create_span_context(self, args, kwargs):
        return ArgumentPropagator().from_arugments()

    def instrument(self):
        global is_instrumented
        is_instrumented = True
        global sampler
        global exporter
        global propagator
        sampler = self.sampler
        exporter = self.exporter
        propagator = self.propagator
        global instrumentator
        instrumentator = self
        super().add_azure_log_handler()
        super().init_tracing("", "")
