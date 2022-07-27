import os
from azure.identity import DefaultAzureCredential
import django.conf as conf

def get_token():
    if 'WEBSITE_HOSTNAME' in os.environ:   
        # Azure hosted, refresh token that becomes password.
        azure_credential = DefaultAzureCredential()
        # Get token for Azure Database for PostgreSQL
        token = azure_credential.get_token("https://ossrdbms-aad.database.windows.net")
        #conf.settings.DATABASES['default']['PASSWORD'] = token.token
        conf.settings.DATABASES['default']['PASSWORD'] = os.environ['DBPASS']
    else:
        # Locally, read password from environment variable.
        conf.settings.DATABASES['default']['PASSWORD'] = os.environ['DBPASS']
        print("Read password env variable.")
    return