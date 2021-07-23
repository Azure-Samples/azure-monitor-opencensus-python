import os
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.tracer import Tracer
from opencensus.trace.samplers import AlwaysOnSampler

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    FLASK_ENV = os.getenv("FLASK_ENV") or "dev"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret-key"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CLOUD_ROLE = os.environ.get("CLOUD_ROLE") or "To-Do App"
    INSTRUMENTATION_KEY = (
        os.environ.get("APPINSIGHTS_INSTRUMENTATIONKEY")
        or "<your-ikey-here>"
    )
    CONNECTION_STRING = "InstrumentationKey=" + INSTRUMENTATION_KEY
    SAMPLER = AlwaysOnSampler()
    EXPORTER = AzureExporter(connection_string=f"{CONNECTION_STRING}")
    TRACER = Tracer(sampler=SAMPLER, exporter=EXPORTER)
