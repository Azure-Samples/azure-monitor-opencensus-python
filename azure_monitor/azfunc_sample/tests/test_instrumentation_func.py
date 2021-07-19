import azure.functions as func

from instrumentation.instrumentation_func import FunctionLogic


def create_http_request() -> func.HttpRequest:
    # Construct a mock HTTP request.
    req = func.HttpRequest(
        method="GET",
        body="",
        url="/api/sample",
    )
    return req


def test_run_successful() -> None:
    http_req = create_http_request()
    http_resp = FunctionLogic.run(http_req)

    assert http_resp.status_code == 200
