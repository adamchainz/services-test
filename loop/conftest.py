# Configuration file for running our tests
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        help="choose a test environment: staging or production"
    )
    parser.addoption(
        "--server-version",
        action="store",
        help="Version of Loop server we are testing"
    )


@pytest.fixture
def env(request):
    return request.config.getoption("--env")


@pytest.fixture
def server_version(request):
    return request.config.getoption("--server-version")
