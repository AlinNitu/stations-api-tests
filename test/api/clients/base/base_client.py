import json
import requests


class BaseAPIClient:
    def __init__(self):
        self.client = requests.session()

    def get_request(self, url: str, query_params=None, headers=None):
        if headers is None:
            headers = {}
        if query_params is None:
            query_params = {}
        return self.client.get(
            url=url,
            params=query_params,
            headers=headers,
        )

    def post(self, url: str, data=None, headers=None):
        if headers is None:
            headers = {}
        if data is None:
            data = {}
        return self.client.post(
            url=url,
            data=json.dumps(data),
            headers=headers,
            verify=False
        )

    # TODO: add other methods: PUT, PATCH, DELETE...
