import os
from .settings import *
from .get_token import get_token
from azureproject.app_insights import *
from opencensus.trace import config_integration

config_integration.trace_integrations(['postgresql'])
config_integration.trace_integrations(['requests'])

# Configure the domain name using the environment variable
# that Azure automatically creates for us.
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []

CSRF_TRUSTED_ORIGINS = ['https://'+ os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []
DEBUG = False
DEBUG_PROPAGATE_EXCEPTIONS = True

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# DBHOST is only the server name, not the full URL
#hostname = os.environ['DBHOST']
#username = os.environ['DBUSER'] + "@" + os.environ['DBHOST']

# Configure Postgres database; the full username for PostgreSQL flexible server is
# username (not @sever-name).
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
