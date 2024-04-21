from test.api.clients.base.base_client import BaseAPIClient
from test.api.clients.stations.stations_resources import TestStationResources
from test.api.api_utils import create_default_headers


class StationsAPIClient(BaseAPIClient):
    def __init__(self):
        self.resources = TestStationResources
        super().__init__()

    def test_station_id(self, ctx, data, station_id):
        return self.post(
            url=f'{ctx.base_url}{self.resources.TEST_STATION}{station_id}',
            data=data,
            headers=create_default_headers())
