---
page_type: sample
languages:
- python
- html
products:
- azure
description: "This sample contains a simple Flask application to show how you can instrument the OpenCensus Azure Monitor exporters as well as track telemetry from popular Python libraries via OpenCensus integrations."
urlFragment: azure-monitor-opencensus-python
---

# Flask "To-Do" Sample Application

## Setup

To send telemetry to Azure Monitor, pass in your instrumentation key into `INSTRUMENTATION_KEY` in `config.py`.

```
INSTRUMENTATION_KEY = <your-ikey-here>
```

The default database URI links to a sqlite database `app.db`. To configure a different database, you can modify `config.py` and change the `SQLALCHEMY_DATABASE_URI` value to point to a database of your choosing.

```
SQLALCHEMY_DATABASE_URI = <your-database-URI-here>
```

## Usage

1. Navigate to where `azure_monitor\flask_sample` is located.
2. Run the main application via `python sample.py`.
4. Hit your local endpoint (should be http://localhost:5000). This should open up a browser to the main page.
5. On the newly opened page, you can add tasks via the textbox under `Add a new todo item:`. You can enter any text you want (cannot be blank).
6. Click `Add Item` to add the task. The task will be added under `Incomplete Items`. Adding an item with greater than 10 characters will generate an error.
7. To utilize the `Save to File` feature, run the endpoint application via `python endpoint.py`. This will run another Flask application with a WSGI server running on http://localhost:5001. Click `Save to File` and all tasks will be written to a file `file.txt` in the `output` folder.
8. Each task has a `Mark As Complete` button. Clicking it will move the task from incomplete to completed.
9. You can also hit the `blacklist` url page to see a sample of a page that does not have telemetry being sent (http://localhost:5000/blacklist).
10. You can also run a command line interface application to hit the endpoints on you Flask application directly. Run `command.py` and follow the prompts accordingly.

## Types of telemetry sent

There are various types of telemetry that are being sent in the sample application. Refer to `Telemetry Type in Azure Monitor <https://docs.microsoft.com/en-us/azure/azure-monitor/app/opencensus-python#telemetry-type-mappings>`_. Every button click hits an endpoint that exists in the flask application, so they will be treated as incoming requests (`requests` table in Azure Monitor). A log message is also sent every time a button is clicked, so a log telemetry is sent (`traces` table in Azure Monitor). An exception telemetry is sent when an invalid task is entered (greater than 10 characters). A counter metric is recorded every time the `add` button is clicked. Metric telemetry is sent every interval (default 15.0 s, `customMetrics` table in Azure Monitor).
