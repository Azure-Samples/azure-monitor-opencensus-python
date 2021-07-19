---
page_type: sample
languages:
- python
products:
- azure
description: "This sample contains a simple Azure Function to show how you can send correlated application log information as well as information of external dependencies to Azure Monitor (Application Insights)."
urlFragment: azure-monitor-opencensus-python
---

# Instrument an Azure Function (Python) using Opencensus 

## Overview

Azure Function (Python) already supports instrumenting using Opencensus. However, the current out-of-the-box (OOTB) implementation/support contains has some frictions which make it difficult to get a correlated end-to-end view of a single function invocation.

The goal of this sample provides developers how to overcome the current limitations and get correlated log information. It covers the following scenarios:

- Log incoming Azure function requests
- Log appication traces & error messages
- Log external dependencies (IN-PROC & HTTP using Python's requests)
- Log entries (incoming requests, traces & errors, external dependencies) are correlated (using the Azure Function's operation id)

### Known Limitations in Current OOTB Logging Integration (Azure Function)

- External dependency log records don't have the correct *Cloud Role Name* (field: cloud_RoleName). This results in wrong information displayed in Application Insight's *Application Map*. Open issue **TODO**
- Errors (logged with the OOTB logging integration) are not correctly logged as Application Insights Exception records. Currently `logging.exception(..)` creates a trace record (with severity level 3 = Error). This comes with certain side effects: E.g. errors are won't show up in Application Insights dashboard (*Failures*) and troubleshooting becomes harder. **TODO**


## Run Locally

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

1. Run tests with `pytest`

### Run

1. Start the Azure Function host: `func host start`
1. Send HTTP request. `curl http://localhost:[PORT]/api/instrumentation`