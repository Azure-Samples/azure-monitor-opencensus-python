import os
import logging

from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure import metrics_exporter
from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import stats as stats_module
from opencensus.stats import view as view_module
from opencensus.tags import tag_map as tag_map_module

stats = stats_module.stats
view_manager = stats.view_manager
stats_recorder = stats.stats_recorder

appKey = os.getenv('APP_INSIGHTS_KEY')

REST_MEASURE = measure_module.MeasureInt("resturants",
                                            "number of resturants",
                                            "resturants")
REST_VIEW = view_module.View("rest_view",
                                "number of resturants",
                                ["state"],
                                REST_MEASURE,
                                aggregation_module.CountAggregation())

ORDERS_MEASURE = measure_module.MeasureInt("orders",
            "number of orders",
            "orders")

ORDERS_VIEW = view_module.View("orders_view",
                                "number of orders",
                                [],
                                ORDERS_MEASURE,
                                aggregation_module.CountAggregation())

REVIEWS_MEASURE = measure_module.MeasureInt("reviews","number of reviews","reviews")

REVIEWS_VIEW = view_module.View("reviews_view",
                                "number of reviews",
                                ["resturantId"],
                                REVIEWS_MEASURE,
                                aggregation_module.CountAggregation())

logger = logging.getLogger(__name__)

logger.addHandler(AzureLogHandler(
    connection_string=appKey)
)

def register_views():

    stats = stats_module.stats
    view_manager = stats.view_manager

    exporter = metrics_exporter.new_metrics_exporter(connection_string=appKey)
    view_manager.register_exporter(exporter)
    
    view_manager.register_view(REVIEWS_VIEW)
    view_manager.register_view(ORDERS_VIEW)
    view_manager.register_view(REST_VIEW)
    
def record_metric_pageviews():
    mmap = stats_recorder.new_measurement_map()
    tmap = tag_map_module.TagMap()
    mmap.measure_int_put(REVIEWS_MEASURE, 1)
    mmap.record(tmap)
    logger.info("metrics: %s value: %s number of measurements: %s ",REVIEWS_MEASURE.name, 1, len(mmap.measurement_map))

def record_metric_review(tmap):
    mmap = stats_recorder.new_measurement_map()
    mmap.measure_int_put(REVIEWS_MEASURE, 1)
    mmap.record(tmap)
    logger.info("metrics: %s value: %s number of measurements: %s ",REVIEWS_MEASURE.name, 1, len(mmap.measurement_map))

def record_metric_resturant(tmap):
    mmap = stats_recorder.new_measurement_map()
    mmap.measure_int_put(REST_MEASURE, 1)
    mmap.record(tmap)
    logger.info("metrics: %s value: %s number of measurements: %s ",REVIEWS_MEASURE.name, 1, len(mmap.measurement_map))

def record_metric_order():
    mmap = stats_recorder.new_measurement_map()
    tmap = tag_map_module.TagMap()
    mmap.measure_int_put(ORDERS_MEASURE, 1)
    mmap.record(tmap)
    logger.info("metrics: %s value: %s number of measurements: %s ",REVIEWS_MEASURE.name, 1, len(mmap.measurement_map))

def record_metric_float(mmap,value,measure):
    # data from the speed test
    mmap.measure_float_put(measure,value)
    # the measure becomes the key to the measurement map
    logger.info("metrics: %s value: %s number of measurements: %s ",measure.name, value, len(mmap.measurement_map))


