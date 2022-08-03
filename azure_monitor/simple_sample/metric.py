import os

from opencensus.ext.azure import metrics_exporter
from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import stats as stats_module
from opencensus.stats import view as view_module
from opencensus.tags import tag_map as tag_map_module

stats = stats_module.stats
view_manager = stats.view_manager
stats_recorder = stats.stats_recorder

appKey = os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING')

CARROTS_MEASURE = measure_module.MeasureInt("carrots",
                                            "number of carrots",
                                            "carrots")
CARROTS_VIEW = view_module.View("carrots_view",
                                "number of carrots",
                                [],
                                CARROTS_MEASURE,
                                aggregation_module.CountAggregation())

# Enable metrics
# Set the interval in seconds in which you want to send metrics
exporter = metrics_exporter.new_metrics_exporter(connection_string=appKey)
view_manager.register_exporter(exporter)

view_manager.register_view(CARROTS_VIEW)
mmap = stats_recorder.new_measurement_map()
tmap = tag_map_module.TagMap()

def prompt():
    mmap.measure_int_put(CARROTS_MEASURE, 1000)
    mmap.record(tmap)
    # Default export interval is every 15.0s

def main():
    while True:
        prompt()

    print("Done recording metrics")

if __name__ == "__main__":
    main()