import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    INSTRUMENTATION_KEY = '70c241c9-206e-4811-82b4-2bc8a52170b9'
    CONNECTION_STRING = 'InstrumentationKey=' + INSTRUMENTATION_KEY
    sampler = 'opencensus.trace.samplers.ProbabilitySampler(rate=1.0)'
    OPENCENSUS = {
        'TRACE': {
            'SAMPLER': sampler,
            'EXPORTER': 'opencensus.ext.azure.trace_exporter.AzureExporter('
            + CONNECTION_STRING + ')',
            'BLACKLIST_PATHS': ['blacklist'],
        }
    }
