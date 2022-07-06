import logging
import os
from opencensus.ext.azure.log_exporter import AzureLogHandler

logger = logging.getLogger(__name__)

appKey = os.getenv('APP_INSIGHTS_KEY')

logger.addHandler(AzureLogHandler(
    connection_string=appKey)
)

# You can also instantiate the exporter directly if you have the environment variable
# `APPLICATIONINSIGHTS_CONNECTION_STRING` configured
# logger.addHandler(AzureLogHandler())

def valuePrompt():
    line = input("Enter a value: ")
    logger.warning(line)

def main():
    while True:
        valuePrompt()

if __name__ == "__main__":
    main()