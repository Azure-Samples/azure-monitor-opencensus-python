import azure.functions as func

from .globals import getLogger, EXTERNAL_DEPENDENCY_URL
from .utils import call_internal_api, call_external_api

logger = getLogger(__name__)


class FunctionLogic:
    @classmethod
    def run(cls, req: func.HttpRequest) -> func.HttpResponse:
        """Azure Function business logic

        Args:
            req([HttpRequest]): [Incoming HTTP request]
        """
        logger.info("new invocation received")

        # TRACK DEPENDENCY (IN-PROC):
        # This long running code is logged as a dependency
        # it uses a method decorator
        call_internal_api(delay=3.0)

        # TRACK DEPENDENCY (HTTP):
        # This uses Opencensus' requests extension
        call_external_api(url=EXTERNAL_DEPENDENCY_URL)

        # TRACES (SEVERITY)
        # create log entries with different severity levels (warning, exception)
        logger.warning("log warning message")

        try:
            assert 1 == 0
        except Exception as ex:
            logger.exception(ex)

        return func.HttpResponse(
            "This HTTP triggered function executed successfully.",
            status_code=200,
        )
