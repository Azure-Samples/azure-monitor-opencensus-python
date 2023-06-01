from re import compile as re_compile
from re import search
from typing import Iterable

from fastapi import FastAPI
from opencensus.trace import (
    print_exporter,
)
from opencensus.trace.base_exporter import Exporter
from opencensus.trace.propagation import trace_context_http_header_format
from opencensus.trace.samplers import Sampler, AlwaysOnSampler
from starlette.types import ASGIApp

from instrumentation import BaseIntrumentator, AzureLoggerConfig
from instrumentation.fastapi.OpenCensusMiddleware import (
    OpenCensusMiddleware,
)

instrumentator: BaseIntrumentator = None
#app_name = None

class ExcludeList:
    """Class to exclude certain paths (given as a list of regexes) from tracing requests (Copied from OpenTelemetry.
    Once opentelemetry is GA we get rid of all these)"""

    def __init__(self, excluded_urls: Iterable[str]):
        self._excluded_urls = excluded_urls
        if self._excluded_urls:
            self._regex = re_compile("|".join(excluded_urls))

    def url_disabled(self, url: str) -> bool:
        return bool(self._excluded_urls and search(self._regex, url))


def parse_excluded_urls(excluded_urls: str) -> ExcludeList:
    """
    Small helper to put an arbitrary url list inside an ExcludeList( Copied from OpenTelemetry. Once opentelemetry is GA we get rid of all these)
    """
    if excluded_urls:
        excluded_url_list = [
            excluded_url.strip() for excluded_url in excluded_urls.split(",")
        ]
    else:
        excluded_url_list = []

    return ExcludeList(excluded_url_list)


class FastapiInstrumentator(BaseIntrumentator):
    """
    Concrete instrumentator for FastApi Application
    """
    app: FastAPI
    def __init__(self,app: ASGIApp,component_name: str):

        self.excluded_urls = None
        self.app = app
        #global app_name

        #app_name = self.component_name
        super().__init__(component_name)

    def with_excluded_url(self, excluded_urls):
        self.excluded_urls = parse_excluded_urls(excluded_urls)
        return self

    def with_tracing(self, sampler: Sampler = None, exporter: Exporter = None, propagator=None,
                     azure_log_config: AzureLoggerConfig = None, app_insight_connection_string: str = None,
                     trace_export_duration=1.0):
        # if connection string is set then ignore the exporter configured
        self.sampler = sampler or AlwaysOnSampler()
        if app_insight_connection_string is None and exporter is None:
            self.exporter = exporter or print_exporter.PrintExporter()
        self.propagator = propagator or trace_context_http_header_format.TraceContextPropagator()
        return super().with_tracing(
            self.sampler,
            self.exporter,
            self.propagator,
            azure_log_config,
            app_insight_connection_string,
            trace_export_duration)

    def instrument(self):
        self.app.add_middleware(
            OpenCensusMiddleware,
            componentName=self.component_name,
            instrumentator=self,
            excluded_urls=self.excluded_urls,
            sampler=self.sampler,
            exporter=self.exporter,
            propagator=self.propagator,
        )
