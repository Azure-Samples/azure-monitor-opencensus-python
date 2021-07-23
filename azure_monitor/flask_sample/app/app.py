import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_sample.config import Config
from opencensus.ext.azure import metrics_exporter
from opencensus.ext.flask.flask_middleware import FlaskMiddleware

logger = logging.getLogger(__name__)


def create_app(conf: Config) -> Flask:
    """Create the flask app

    Args:
        conf([Config]): [Configuration object]
    """

    def callback_function(envelope):
        """Callback function to update an log record.
        This function changes the cloud role name of the log entry

        Args:
            envelop: [Log record to update]
        """
        envelope.tags["ai.cloud.role"] = conf.CLOUD_ROLE
        return True

    app = Flask(__name__)
    app.config.from_object(conf)

    # FlaskMiddleware will track requests for the Flask application and send
    # request/dependency telemetry to Azure Monitor
    middleware = FlaskMiddleware(app, exporter=conf.EXPORTER, sampler=conf.SAMPLER)
    # Adds the telemetry processor to the trace exporter
    middleware.exporter.add_telemetry_processor(callback_function)

    # Exporter for metrics, will send metrics data
    _ = metrics_exporter.new_metrics_exporter(
        enable_standard_metrics=False, connection_string=f"{conf.CONNECTION_STRING}"
    )

    return app


app = create_app(Config)
db = SQLAlchemy(app)
