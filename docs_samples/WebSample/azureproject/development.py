import os
from .settings import *
from .get_token import get_token
from azureproject.app_insights import *
from opencensus.trace import config_integration

config_integration.trace_integrations(['postgresql'])

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Don't use Whitenoise to avoid having to run collectstatic first.
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

ALLOWED_HOSTS = ['*']

# Configure Postgres database for local development
#   Set these environment variables in the .env file for this project.  
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['PGDBNAME'],
        'HOST': os.environ['PGDBHOST'],
        'USER': os.environ['PGDBUSER'],
        'OPTIONS': {'sslmode': 'require'},
        'PASSWORD': os.environ['PGDBPASS'] 
    }
}

#load all the custom metrics...
register_views()

#get_token()
