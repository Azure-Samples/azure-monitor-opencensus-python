---
title: 'Publishing traces and logs to Azure from fastApi application'
description: Publishing traces and logs to Azure from fastApi application using opencensus library.
ms.devlang: python
ms.topic: sample
---

# Overview

This document covers details around how to use opencensus to publish traces and logs to Azure. This is just one of 
the guideline and sample implementation amongst few others available on internet.
This code base consist of three projects

[opencensus_fastapi_lib_common](opencensus_fastapi_lib_common)
[opencensus_fastapi_examples](opencensus_fastapi_examples)
[opencensus_task_example](opencensus_task_example)

Below material will cover all these projects in details

## opencensus_fastapi_lib_common

This is common library can be used to instrument FastAPI applications. 

Expected usage is to build this library and 
include it in individual projects as shown in example section

Build steps are as below

    cd  azure_monitor/fastapi_logger_sample/opencensus_fastapi_lib_common

    pip install build

    python -m build 

One build command succeeds there will a wheel file and a source tar created in dist directory. These can be further 
uploaded to pip repository to be shared across other projects

One might also want to run below command to install dependencies on the local pip virtual environment which could be 
helpful to enhance the library and compile it as well

There are packages in the project that has codebase to instrument fastapi application and a decorator that can be 
used to non-web based applications. This could be useful in cases of batch workloads

## Usage in FastApi application

Once the library is build and included in a FastApi application one can use FastapiInstrumentator class to 
instrument the application as below

    FastapiInstrumentator(app, component_name) \
    .with_excluded_url("health").with_tracing() \
    .instrument()

The details of various methods and parameters for this class is given below


| method name         | Description                                                                            |
 |:---| :---: |
| with_excluded_url   | Comma seperated list or uri to exclude from tracing. This will be typically health url or liveness checks    |
| with_tracing | This method sets up tracing. It is very important to call this method if you want tracing to be enabled |
| instrument | This sets up instrumentator and create all relevant objects required for instrumentation to work as expected

with_tracing takes below parameters

| parameter name | Description |
 | :--- | :---: |
| sampler | Defines the sampling to be used for traces. Defaults to AlwaysOnSampler |
| exporter | Defines the exporter for traces. If none is configured then defaults to [PrintExporter](https://opencensus.io/api/python/trace/api/print_exporter.html). If app_insight_connection_string is configured and exporter is none then [AzureExporter](https://github.com/census-instrumentation/opencensus-python/blob/d0f99658bb2f78cd559d55732d7a062a884ecc75/contrib/opencensus-ext-azure/opencensus/ext/azure/trace_exporter/__init__.py#L58) is used
| propagator | Defines the propagator to be used. Defaults to header based propagation of trace_id |
| azure_log_config | Define level, formatter or custom filters when sending logs to Azure. These will go into Azure traces table. Defaults to None  |
| app_insight_connection_string | Connection string for Azure application insight instance. Defaults to None. This will also drive which exporter to use |
| trace_export_duration | Defines frequency of pusing traces. Defaults to 1 sec  |

## Usage in Batches/Task/ Non-Web applications

Once the library is build and included in an application one can use TaskInstrumentator class to
instrument the application as below

    TaskInstrumentator(component_name="batch-task").with_tracing().instrument()

Additionally one needs to include `@with_tracing` annotation on the main entrypoint where the instrumentation starts.
Example as below 

    @with_tracing
    def process_and_trace():
    log.info("Called process and trace")

All parameters and method definations are same as that of FastApi application with a minor difference that the 
propagator in this case will refer to trace propagation from environment variable instead of header

### Notes
Please also have look at https://github.com/Azure-Samples/opencensus-with-fastapi-and-azure-monitor

