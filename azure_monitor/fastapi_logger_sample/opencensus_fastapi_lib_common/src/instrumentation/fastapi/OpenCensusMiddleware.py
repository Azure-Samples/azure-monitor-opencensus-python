import logging

from opencensus.trace import (
    attributes_helper,
)
from opencensus.trace import span as span_module
from opencensus.trace.span import Span
from opencensus.trace.tracer import Tracer
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from instrumentation import create_tracer, add_exception_details_to_span

HTTP_HOST = attributes_helper.COMMON_ATTRIBUTES["HTTP_HOST"]
HTTP_METHOD = attributes_helper.COMMON_ATTRIBUTES["HTTP_METHOD"]
HTTP_PATH = attributes_helper.COMMON_ATTRIBUTES["HTTP_PATH"]
HTTP_ROUTE = attributes_helper.COMMON_ATTRIBUTES["HTTP_ROUTE"]
HTTP_URL = attributes_helper.COMMON_ATTRIBUTES["HTTP_URL"]
HTTP_STATUS_CODE = attributes_helper.COMMON_ATTRIBUTES["HTTP_STATUS_CODE"]

framework_logger = None

async def finish_tracer(response, span, tracer):
    span.add_attribute(HTTP_STATUS_CODE, response.status_code)
    # will this always be same method
    span_context = tracer.span_context
    traceid = span_context.trace_id
    spanid = span_context.span_id
    trace_options = span_context.trace_options.enabled
    # Convert the trace options
    trace_options = "01" if trace_options else "00"
    response.headers.append("traceid", traceid)
    response.headers.append("trace_options", trace_options)
    response.headers.append("spanid", spanid)
    tracer.end_span()
    tracer.finish()


class OpenCensusMiddleware(BaseHTTPMiddleware):
    """Middleware for opencensus tracing"""

    def __init__(
        self,
        app: ASGIApp,
        componentName,
        instrumentator,
        excluded_urls=None,
        sampler=None,
        exporter=None,
        propagator=None,
    ):
        super().__init__(app)
        global framework_logger
        framework_logger = logging.getLogger("trace_logger")
        self.sampler = sampler
        self.exporter = exporter
        self.propagator = propagator
        self.component_name = componentName
        self.excluded_urls = excluded_urls
        self.app_insights_key = None
        self.loadConfig = False
        self.instrumentator = instrumentator

    def _init_tracer(self, request: Request) -> Tracer:
        span_context = self.propagator.from_headers(request.headers)
        return create_tracer(span_context, self.sampler, self.exporter, self.propagator)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if self.excluded_urls and self.excluded_urls.url_disabled(str(request.url)):
            return await call_next(request)
        self.instrumentator.add_azure_log_handler()  # Add handler to loggers
        try:
            tracer = self._init_tracer(request)
            span: Span = tracer.start_span(self.component_name)
            span.span_kind = span_module.SpanKind.SERVER
            span.name = "[{}]{}".format(request.method, request.url)
            span.add_attribute(HTTP_HOST, request.url.hostname)
            span.add_attribute(HTTP_METHOD, request.method)
            span.add_attribute(HTTP_PATH, request.url.path)
            span.add_attribute(HTTP_URL, str(request.url))
            span.add_attribute(HTTP_ROUTE, request.url.path)
        except Exception:  # pragma: NO COVER
            framework_logger.error("Failed to trace request", exc_info=True)
            return await call_next(request)
        try:
            response = await call_next(request)
        except Exception as err:  # pragma: NO COVER
            try:
                add_exception_details_to_span(span, err)
                await finish_tracer(response, span, tracer)
            except Exception:  # pragma: NO COVER
                framework_logger.error("Failed to trace response", exc_info=True)
            raise err
        try:
            await finish_tracer(response, span, tracer)
        except Exception:  # pragma: NO COVER
            framework_logger.error("Failed to trace response", exc_info=True)
        return response
