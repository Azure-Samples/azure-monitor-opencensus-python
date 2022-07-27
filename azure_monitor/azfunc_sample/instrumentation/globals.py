import os
import socket
import logging

from logging import Logger
from opencensus.trace import config_integration
from opencensus.ext.azure.log_exporter import AzureLogHandler


AI_CONNECTION_STRING = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")

if not AI_CONNECTION_STRING:
    raise EnvironmentError(
        "AI Connection string not set. Set it through the environment variable: APPLICATIONINSIGHTS_CONNECTION_STRING."
    )

WEBSITE_SITE_NAME = os.getenv("WEBSITE_SITE_NAME")

if not WEBSITE_SITE_NAME:
    raise EnvironmentError(
        "Website site name not set. Set it through the environment variable: WEBSITE_SITE_NAME."
    )

EXTERNAL_DEPENDENCY_URL = os.getenv("EXTERNAL_DEPENDENCY_URL")

if not EXTERNAL_DEPENDENCY_URL:
    raise EnvironmentError(
        "External dependency URL not set. Set it through the environment variable: EXTERNAL_DEPENDENCY_URL."
    )

# initialize observability (with opencensus)
config_integration.trace_integrations(["logging", "requests"])


def callback_add_role_name(envelope):
    """Add role name for logger."""
    envelope.tags["ai.cloud.role"] = WEBSITE_SITE_NAME
    envelope.tags["ai.cloud.roleInstance"] = socket.getfqdn()


def getLogger(
    name: str,
    instrumentation_conn_string: str = AI_CONNECTION_STRING,
    propagate: bool = False,
) -> Logger:
    """Get a new logging instance with a handler to send logs to Application Insights

    Args:
        name([str]): [The name of the logger]
        instrumentation_conn_string([str]): [The AppInsights instrumentation connection string]
        propagate([bool]): [Enable log propagation (default: false)]
    """
    logHandler = AzureLogHandler(connection_string=instrumentation_conn_string)
    logHandler.add_telemetry_processor(callback_add_role_name)

    logger = logging.getLogger(name)
    logger.addHandler(logHandler)
    logger.propagate = propagate

    return logger
