# the code in globals ensures that logging
# is initialized at the very beginning
from . import globals  # noqa: F401


# PRs

# 0. Fix wrong documentation
# https://github.com/census-ecosystem/opencensus-python-extensions-azure/pull/6

# 1. Ensure that the cloud role is set correctly
# e.g. dependencies don't set it - needs to be fixed (when logging a dependency in AppInsights) like an additional option
# when creating a AzureLogExporter fixes this (but for AzFunc it is enough to set WEBSITE_SITE_NAME)

# 2. Ensure that the opencensus trace context is set on function (pre) invocation.
# without this the trace context is not correct and log entries won't be correlated with request log entry
# https://github.com/census-ecosystem/opencensus-python-extensions-azure/blob/12feaa323aa4b698024659d09fba7fc127c666f3/extensions/functions/src/opencensus/extension/azure/functions.py#L77
# something like: "execution_context.set_opencensus_tracer(tracer)  # type: ignore[attr-defined]""
