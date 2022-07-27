import logging
import os
import requests
import time

from opencensus.ext.azure.log_exporter import AzureLogHandler

appKey = os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING')
funcUrl = os.getenv('FUNCTION_URL')

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string=appKey))

#fire the functions
def callFunction(apiUrl):
    #wait 3 seconds...
    time.sleep(3)

    logger.warning('Calling function app')
    response = requests.get(apiUrl)
    logger.warning(response)

def main():
    while True:
        callFunction(funcUrl)

if __name__ == "__main__":
    main()