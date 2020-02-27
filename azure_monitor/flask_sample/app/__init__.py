import logging
import sys

from flask import Flask

sys.path.append('..')
from config import Config
from flask_sqlalchemy import SQLAlchemy
from opencensus.ext.azure import metrics_exporter
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace import config_integration

logger = logging.getLogger(__name__)
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# Import here to avoid circular imports
from app import routes  # noqa isort:skip

# Trace integrations for sqlalchemy library
config_integration.trace_integrations(['sqlalchemy'])

# Trace integrations for requests library
config_integration.trace_integrations(['requests'])

# FlaskMiddleware will track requests for the Flask application and send
# request/dependency telemetry to Azure Monitor
middleware = FlaskMiddleware(app)

# Processor function for changing the role name of the app
def callback_function(envelope):
    envelope.tags['ai.cloud.role'] = "To-Do App"
    return True

# Adds the telemetry processor to the trace exporter
middleware.exporter.add_telemetry_processor(callback_function)

# Exporter for metrics, will send metrics data
exporter = metrics_exporter.new_metrics_exporter(
    enable_standard_metrics=False,
    connection_string='InstrumentationKey=' + Config.INSTRUMENTATION_KEY)

# Exporter for logs, will send logging data
logger.addHandler(
    AzureLogHandler(
        connection_string='InstrumentationKey=' + Config.INSTRUMENTATION_KEY
        )
    )


if __name__ == '__main__':
    app.run(host='localhost', port=5000, threaded=True, debug=True)
