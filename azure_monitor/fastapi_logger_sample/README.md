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

### Notes
Please also have look at https://github.com/Azure-Samples/opencensus-with-fastapi-and-azure-monitor

