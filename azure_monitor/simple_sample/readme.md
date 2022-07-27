# Simple Applications

## Setup

Follow the steps in the [setup documentation](/azure_monitor/readme.md).

## Create a simple Python App

- Create a new python file called `app.py`.
- Copy the following into it, be sure to replace your Application Insights connection string that you copied above:

```python
import logging

from opencensus.ext.azure.log_exporter import AzureLogHandler

logger = logging.getLogger(__name__)

logger.addHandler(AzureLogHandler(connection_string='InstrumentationKey=<your-instrumentation_key-here>'))

logger.warning('Hello, World!')
```

- Press **F5** to run the file, select **Python file** in the debug configuration window.
- If you get an error about `psutil._psutil_windows` do the following:
  - Open the `.venv\Lib\site-packages` folder and delete the `psutil` and `psutil-5.9.1.dist-info` folders.
  - Then run the following:

    ```Python
    python -m pip install --upgrade pip
    python -m pip install psutil
    ```

- Switch to the Azure Portal, navigate to your Application Insights resource.
- Under **Monitoring**, select **Logs**.
- Run the following kusto query:

```kusto
traces
| sort by timestamp
| where cloud_RoleName == "app.py"
```

- You should see the following:

  ![The query is displayed with one result from the above program.](./media/python_simple_app_trace.png "Review the results of the query.")

- Open the `./SimpleApps/metric.py` file.
- Press **F5** to run the file, select **Python file** in the debug configuration window.
- Switch to the Azure Portal.
- Browse to your lab resource group.
- Browse to the `python-appinsights-SUFFIX` application insights resource and select it.
- Under **Monitoring**, select **Metrics**.
- For the **Metric namespace**, select **carrots_view**.
- For the **Metric**, select **carrots_view**.
- You should see some data displayed:

    ![The custom metric for the carrots view is displayed.](./media/python_custommetrics-carrots.png "Review the results of the metric data.")

- Stop the application.

- You can user kusto queries to get metric data:
  - Under **Montioring**, select **Logs**.
  - Run the following query:

```kusto
customMetrics 
| where cloud_RoleName == "metric.py"
```

- You should see the metric value is recorded every 15 seconds:

    ![The custom metric for the carrots view is displayed.](./media/python_custommetrics-carrots-logs.png "Review the results of the metric data.")

## Sending trace data

- Open the `./azure_monitor/SimpleApps/trace.py` file, notice that the connection string is being pulled from an environment variable rather than being hard coded.
- Press **F5** to run the file.
- Switch to the Azure Portal.
- Browse to your lab resource group.
- Browse to the `python-appinsights-SUFFIX` application insights resource and select it.
- Under **Monitoring**, select **Logs**.
- Run the following Kusto query to see the `traces` sent to application insights:

```kql
traces
| sort by timestamp
| where cloud_RoleName == "trace.py"
```

- You should see your trace in the **message** column:

  ![The query is displayed with one result from the above program.](./media/python_simple_trace_trace.png "Review the results of the query.")

- For your trace item notice that some of the columns are empty, but others (such as `cloud_RoleName`, `cloud_RoleInstance` and `client_*`) are populated based on the client information from the SDK.

## Capture exceptions and custom dimensions

- Switch back to your Visual Studio Code window.
- Select the `./SimpleApps/properties.py` file.
- Press **F5** to run the file, select **Python file** in the debug configuration window.
- Switch to the Azure Portal.
- Browse to your lab resource group.
- Browse to the `python-appinsights-SUFFIX` application insights resource and select it.
- Under **Monitoring**, select **Logs**.
- Run the following Kusto query to see the `exception` sent to application insights:

```kql
exceptions
| sort by timestamp
| where cloud_RoleName == "properties.py"
```

- Expand your exception item, notice the `details` column has the exception details you would expect, but also expand the `customDimensions` column to review the custom data that was sent to the application insights table.

  ![The query is displayed with one result from the above program.](./media/python_simple_exception_custom.png "Review the results of the query.")