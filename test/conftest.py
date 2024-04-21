import pytest
import urllib3
from test.api.clients.stations.stations_client import StationsAPIClient


pytest_plugins = ["test.features"]


class Context:
    def __init__(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.stations_client = StationsAPIClient()

        # best to store version as part of base url or even separate, easier to update if needed
        self.base_url = 'https://api-energy-k8s.test.virtaglobal.com/v1/'

        self.responses = []
        self.shared_data = {}

    def set_shared_data(self, key, value):
        self.shared_data[key] = value

    def get_shared_data(self, key):
        return self.shared_data.get(key)

    def add_response(self, response):
        self.responses.append(response)

    def get_last_response(self):
        return self.responses[-1]


@pytest.fixture(scope="function")
def ctx():
    context = Context()
    yield context


def pytest_collection_modifyitems(items):
    for item in items:
        if "ignore" in item.keywords:
            item.add_marker(pytest.mark.skip(reason="Test is marked with @ignore"))
