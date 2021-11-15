import pytest

from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.log import TraceLogger

from instrumentation.globals import getLogger

CONNECTION_STRING = "InstrumentationKey=00000000-0000-0000-0000-000000000000"


@pytest.mark.parametrize(
    "name, conn_string, propagate",
    [(__name__, CONNECTION_STRING, False), ("test", CONNECTION_STRING, True)],
)
def test_logger_correctly_configured(
    name: str, conn_string: str, propagate: bool
) -> None:
    sut = getLogger(
        name=name, instrumentation_conn_string=conn_string, propagate=propagate
    )

    assert sut.name == name
    assert sut.propagate == propagate
    assert isinstance(sut, TraceLogger)
    assert len(sut.handlers) == 1
    assert isinstance(sut.handlers[0], AzureLogHandler)
    assert sut.handlers[0].options["connection_string"] == CONNECTION_STRING
