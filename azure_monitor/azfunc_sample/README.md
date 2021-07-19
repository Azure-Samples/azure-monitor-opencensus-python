---
page_type: sample
languages:
- python
products:
- azure
description: "This sample contains a simple Azure Function to show how you can send correlated application log information as well as information of external dependencies to Azure Monitor (Application Insights)."
urlFragment: azure-monitor-opencensus-python
---

# Azure Function Sample Application

## Overview

## Run it locally

### Setup

1. Install [Azure Functions Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=linux%2Ccsharp%2Cbash).
1. Install Azure Storage Emulator [Azurite](https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azurite) & start Azurite's Blob service 
1. Install all package dependencies locally using `pip install -r requirements.txt`.
1. Create a file named `local.settings.json` which contains the following configuration information (*replace the placeholders*)

    ```json
    {
    "IsEncrypted": false,
    "Values": {
        "AzureWebJobsStorage": "UseDevelopmentStorage=true",
        "FUNCTIONS_WORKER_RUNTIME": "python",
        "PYTHON_ENABLE_WORKER_EXTENSIONS": "1",
        "APPLICATIONINSIGHTS_CONNECTION_STRING": "InstrumentationKey=[YOUR-APPLICATION-INSIGHTS-KEY]",
        "WEBSITE_SITE_NAME": "[YOUR-APPLICATION-INSIGHTS-CLOUD-ROLE-NAME e.g. MyFunction]",
        "EXTERNAL_DEPENDENCY_URL":"[SOME-WEB-URL-FOR-DEPENDENCY-TRACKING e.g. https://www.bing.com]"
        }
    }
    ```

### Test

1. Run '```pytest```'

### Run

1. Start the Azure Function host: ```func host start```
1. Send HTTP request. ```curl http://localhost:[PORT]/api/instrumentation```