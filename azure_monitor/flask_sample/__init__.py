import logging
from logging import Logger
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.trace import config_integration

from .config import Config

config_integration.trace_integrations(
    ["logging", "requests", "sqlalchemy"], tracer=Config.TRACER
)


def getLogger(name: str) -> Logger:
    """Initializes a logger instance (ready for sending logs to Azure Monitor)

    Args:
        name([str]): [logger name. empty name represents the root logger]
    """
    logger = logging.getLogger(name)
    logger.addHandler(AzureLogHandler(connection_string=f"{Config.CONNECTION_STRING}"))
    logger.setLevel("INFO")

    return logger


# initialize the root logger and connect with AppInsights
# by using logger propagation every logger (based from the root logger) uses that
# handler automtically (by default - if not disabled intenionally)
root_logger = getLogger(name="")
