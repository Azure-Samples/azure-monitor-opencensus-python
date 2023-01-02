import logging
import traceback
from abc import ABC, abstractmethod
from typing import Union

from opencensus.ext.azure.log_exporter import AzureLogHandler, BaseLogHandler
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.log import TRACE_ID_KEY, SPAN_ID_KEY, LogAttrs, ATTR_DEFAULTS
from opencensus.trace import (
    config_integration,
    integrations,
    execution_context,
    Span,
    attributes_helper,
)
from opencensus.trace.base_exporter import Exporter
from opencensus.trace.blank_span import BlankSpan
from opencensus.trace.samplers import Sampler, AlwaysOnSampler
from opencensus.trace.span_context import SpanContext
from opencensus.trace.trace_options import TraceOptions
from opencensus.trace.tracer import Tracer

integrations.add_integration(integrations._Integrations.LOGGING)
integrations.add_integration(integrations._Integrations.REQUESTS)

config_integration.trace_integrations(["logging"])
config_integration.trace_integrations(["requests"])

ERROR_MESSAGE = attributes_helper.COMMON_ATTRIBUTES["ERROR_MESSAGE"]
ERROR_NAME = attributes_helper.COMMON_ATTRIBUTES["ERROR_NAME"]
STACKTRACE = attributes_helper.COMMON_ATTRIBUTES["STACKTRACE"]

component_name = "NOT-SET"


class TracingAttributeFilter(logging.Filter):
    def filter(self, record):
        tracer = execution_context.get_opencensus_tracer()
        if not hasattr(record, TRACE_ID_KEY):
            try:
                setattr(record, TRACE_ID_KEY, tracer.span_context.trace_id)
            except Exception:
                setattr(record, TRACE_ID_KEY, "None")
        if not hasattr(record, SPAN_ID_KEY):
            try:
                setattr(record, SPAN_ID_KEY, tracer.span_context.span_id)
            except Exception as e:
                setattr(record, SPAN_ID_KEY, "None")

        return True


# Add filter for loggers created before TraceLogger is set
for name in logging.root.manager.loggerDict:
    logger = logging.root.manager.loggerDict[name]
    if not isinstance(logger, logging.PlaceHolder):
        logger.addFilter(TracingAttributeFilter())


def handle_exception(span: Union[Span, BlankSpan], exception: Exception):
    span.add_attribute(ERROR_NAME, exception.__class__.__name__)
    span.add_attribute(ERROR_MESSAGE, str(exception))
    span.add_attribute(
        STACKTRACE, "\n".join(traceback.format_tb(exception.__traceback__))
    )


def get_tracer(
        span_context: SpanContext, sampler: Sampler, exporter: Exporter, propagator
):
    tracer = Tracer(
        span_context=span_context,
        sampler=sampler,
        exporter=exporter,
        propagator=propagator,
    )
    return tracer


def already_tracing():
    t: Tracer = execution_context.get_opencensus_tracer()
    if t.span_context is not None:
        trace_options: TraceOptions = t.span_context.trace_options
        return trace_options.get_enabled()
    return False


module_logger = logging.getLogger(__name__)


class AzureLoggerConfig:
    def __init__(self, filters=None, level: str = "INFO",
                 log_format: str = "%(asctime)s %(levelname)s %(name)s %(filename)s:%("
                                   "lineno)d traceId=%(traceId)s spanId=%(spanId)s - %(message)s") -> None:
        super().__init__()
        self.level = level or "INFO"
        self.level = self.level.upper()
        self.filters = filters
        self.log_format = log_format


def init_azure_log_handler(connection_string, azure_log_config, component_n):
    def callback(envelope):
        envelope.tags["ai.cloud.role"] = component_n
        envelope.tags["ai.cloud.roleInstance"] = component_n
        """Adding cloud role name. This is required to give the name of component in application map.
        https://docs.microsoft.com/azure/azure-monitor/app/app-map?tabs=net#understanding-cloud-role-name-within-the-context-of-the-application-map

        Args:
            component_name ([str]): [The name of the component or applicaiton]
        """

    log_handler = AzureLogHandler(connection_string=connection_string)
    log_handler.add_telemetry_processor(callback)
    log_handler.name = "opencensus-azure-handler"
    log_handler.formatter = logging.Formatter(azure_log_config.log_format)
    log_handler.setLevel(azure_log_config.level)
    if azure_log_config.filters is not None:
        for fil in azure_log_config.filters:
            log_handler.addFilter(fil)
    log_handler.addFilter(DropNonSpanFilter())
    return log_handler


class DropNonSpanFilter(logging.Filter):
    def filter(self, record):
        if hasattr(record, SPAN_ID_KEY):
            span_id = getattr(record, SPAN_ID_KEY)
            if span_id is None or span_id == ATTR_DEFAULTS.span_id:
                # This is some internal log we need log to Azure
                return False

        return True


class BaseIntrumentator(ABC):
    def __init__(self, name):
        self.exporter = None
        self.propagator = None
        self.sampler = None
        self.app_insight_connection_string = None
        global component_name
        self.component_name: str = name
        component_name = name
        # self.app_insight_connection_string: str = app_insight_connection_string
        self.azure_log_config = None
        self.enable_traces_on_azure: bool = False
        # if azure_logger_config is not None:
        #     self.enable_traces_on_azure = True
        #     self.azure_log_config = azure_logger_config

        self.__logger_dict = {}
        self.tracer = None

    def with_tracing(
            self,
            sampler: Sampler = None,
            exporter: Exporter = None,
            propagator=None,
            azure_log_config: AzureLoggerConfig = None,
            app_insight_connection_string: str = None,
            trace_export_duration=1.0
    ):
        self.app_insight_connection_string = app_insight_connection_string
        self.exporter = exporter
        if exporter is None:
            if self.app_insight_connection_string is not None:
                self.setup_azure_exporter(trace_export_duration)
        if azure_log_config is not None:
            if self.app_insight_connection_string is None:
                raise KeyError(
                    "App insight connection string is not configured. Please configure it in API or env"
                )
            self.azure_log_config = azure_log_config
            self.enable_traces_on_azure = True
        return self

    @abstractmethod
    def instrument(self):
        """To be implemented"""

    def create_span_context(self):
        """Override this to init span context. This will be useful when
        one need to set up propagator"""
        return SpanContext()

    def init_tracing(self, args, kwargs):
        span_context = self.create_span_context(args, kwargs)
        tracer = get_tracer(span_context, self.sampler, self.exporter, self.propagator)
        self.tracer = tracer
        return tracer

    def add_azure_log_handler(self):
        if self.azure_log_config is None:
            return
        if self.app_insight_connection_string is None:
            raise KeyError(
                "Missing config for app_insight_key. App_insight_key is not found"
            )

        for name in logging.root.manager.loggerDict:

            if not name in self.__logger_dict and name != BaseLogHandler.name:
                log = logging.root.manager.loggerDict[name]

                if not isinstance(log, logging.PlaceHolder):
                    # add handler to this logger
                    connection_String = self.app_insight_connection_string
                    log_handler = init_azure_log_handler(
                        connection_String, self.azure_log_config, self.component_name
                    )

                    # Figure out way to add this handler to all future loggers
                    if not any(x for x in log.handlers if x.name == log_handler.name):
                        log.addHandler(log_handler)
                        log_level = self.azure_log_config.level
                        # check if the user logger is at lower level or Azure log config is at lower level
                        # set to lowest of the two
                        if logging.getLevelName(log_level) > log.level:
                            log.setLevel(self.azure_log_config.level)
                self.__logger_dict[name] = log_handler

    def setup_azure_exporter(self, trace_export_duration):
        def callback(envelope):
            envelope.tags["ai.cloud.role"] = self.component_name
            envelope.tags["ai.cloud.roleInstance"] = self.component_name
            """Adding cloud role name. This is required to give the name of component in application map.
            https://docs.microsoft.com/azure/azure-monitor/app/app-map?tabs=net#understanding-cloud-role-name-within-the-context-of-the-application-map

            Args:
                component_name ([str]): [The name of the component or applicaiton]
            """

        exporter = AzureExporter(
            connection_string=self.app_insight_connection_string,
            export_interval=trace_export_duration
        )
        exporter.add_telemetry_processor(callback)
        self.exporter = exporter
