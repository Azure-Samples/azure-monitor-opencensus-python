from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import stats as stats_module
from opencensus.stats import view as view_module
from opencensus.tags import tag_map as tag_map_module

stats = stats_module.stats
view_manager = stats.view_manager
stats_recorder = stats.stats_recorder

request_measure = measure_module.MeasureInt("added tasks",
                                            "number of added tasks",
                                            "tasks")
request_view = view_module.View("added tasks",
                                "number of tasks",
                                ["application_type"],
                                request_measure,
                                aggregation_module.CountAggregation())
view_manager.register_view(request_view)
mmap = stats_recorder.new_measurement_map()
tmap = tag_map_module.TagMap()
tmap.insert("application_type", "flask")
tmap.insert("os_type", "linux")
