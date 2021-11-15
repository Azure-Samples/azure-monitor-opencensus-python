---
page_type: sample
languages:
- python
products:
- azure
description: "This sample contains a simple Azure Function to show how you can send correlated application log information as well as information of external dependencies to Azure Monitor (Application Insights)."
urlFragment: azure-monitor-opencensus-python
---

# Correlated End-To-End Azure Function (Python) Instrumentation with Opencensus 

## Overview

Azure Function (Python) already supports instrumentation using Opencensus. The following sample utilizes the OpenCensus Functions extension and enables additional common telemetry scenarios used by Azure Monitor and Functions users. Such scenarios include:
- End-to-end view of a single function invocation (in Azure Monitor Application Insights)
- Create an application topology view (application dependencies to support distributed tracing) using Azure Monitor Application Insight's Application Map (especially useful when working with distributed, scalable applications). 

### Example of a Correlated End-to-End Azure Function Invocation

End-to-end transaction:

![AI Correlated end2end function invocation](./docs/assets/01-ai-correlated-invocation.PNG)

Associated application trace messages:

![AI Application trace messages](./docs/assets/02-ai-correlated-invocation.PNG)

Associated AI Application Map:

![AI Application Map](./docs/assets/03-ai-application-map.PNG)

The images shows the following elements:

- Correlated (per Azure Function invocation) log information including:
    - Incoming request information
    - Application traces & error messages
    - External dependencies (IN-PROC & HTTP using Python's `requests` library)
- Application Map (defined cloud role and cloud instance values)

### Additional Customizations Enabling Azure Monitor Scenarios

- In order to get the application topology (Application Insight's Application Map) the correct *Cloud Role Name* (field: cloud_RoleName) must be set (using a [Telemetry Processor](https://docs.microsoft.com/en-us/azure/azure-monitor/app/api-filtering-sampling#opencensus-python-telemetry-processors))

### Known Limitations in Current OpenCensus Azure Monitor Log Exporter

- Errors (logged using the OpenCensus Azure Monitor Log Exporter) are logged as Application Insights Trace records (e.g. `logging.exception(..)` creates a trace record (with severity level 3 = Error)). Since errors don't result in a not logged as Application Insights Exceptions log record, errors don't show up in the Application Insights dashboard (*Failures* tab) - see issue <https://github.com/Azure/azure-functions-python-worker/issues/866>)
- Logs are not correlated when crossing API boundaries (distributed tracing).

## Goal 

The goal of this code sample is to demonstrate an alternative (custom) approach of instrumenting Azure Function code using Opencensus. This should give developers more insights how to use Opencensus and how to customize monitoring integration (based on the OpenCensus Azure Monitor Log Exporter).

> *Important. Once the issues (see below) are resolved in the platform, it is recommended to move to updated OpenCensus Azure Monitor Log Exporter implementation!* 

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

1. (Optional) Update environment variables in file `.test.env`
1. Run tests with `pytest`

### Run

1. Start the Azure Function host: `func host start`
1. Send HTTP request. `curl http://localhost:[PORT]/api/instrumentation`

## Contributors
[Oliver Lintner](https://github.com/se02035)  