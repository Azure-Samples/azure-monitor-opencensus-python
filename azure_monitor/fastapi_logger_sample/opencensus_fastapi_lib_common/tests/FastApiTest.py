import unittest

from fastapi import FastAPI
from starlette.testclient import TestClient

from opencensus.trace import print_exporter, samplers
from opencensus.trace.propagation import trace_context_http_header_format

from instrumentation.fastapi import FastapiInstrumentator, OpenCensusMiddleware
from instrumentation.task import TRACE_ID_PARAM


class TestFastApi(unittest.TestCase):

    def create_app(self):
        app = FastAPI()

        @app.get('/')
        def index():
            return 'test fastapi trace'  # pragma: NO COVER

        return app

    def test_instrumentation(self):
        app = self.create_app()
        FastapiInstrumentator(app=app, component_name="test_component") \
            .with_excluded_url("/health") \
            .with_tracing() \
            .instrument()
        middlewares = [middleware for middleware in app.user_middleware if middleware.cls == OpenCensusMiddleware]
        self.assertEquals(len(middlewares), 1, "More than one Opencensus middleware found")

        opencensusmiddleware = middlewares[0]
        self.assertIsInstance(opencensusmiddleware.options['exporter'], print_exporter.PrintExporter)
        self.assertIsInstance(opencensusmiddleware.options['sampler'], samplers.AlwaysOnSampler)
        self.assertIsInstance(opencensusmiddleware.options['propagator'],
                              trace_context_http_header_format.TraceContextPropagator)
        self.assertIsNotNone(opencensusmiddleware.options['excluded_urls'])

    def test_request(self):
        trace_id = '11111111111111111111111111111111'
        span_id = '9999999999999999'
        formatted_trace_id = '00-{}-{}-00'.format(trace_id, span_id)
        app = self.create_app()
        FastapiInstrumentator(app=app, component_name="test_component") \
            .with_excluded_url("/health") \
            .with_tracing() \
            .instrument()
        test_client = TestClient(app)
        response = test_client.get("/")
        self.assertIsNotNone(response.headers['traceid'])
        self.assertIsNotNone(response.headers['spanid'])
        self.assertEqual(response.status_code, 200)
        response = test_client.get("/", headers={TRACE_ID_PARAM: formatted_trace_id})
        self.assertEqual(response.headers['traceid'], trace_id)
