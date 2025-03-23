import requests

class TestRailAPI:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.auth = (username, password)

    def add_result(self, test_id, status_id, comment):
        url = f'{self.base_url}/index.php?/api/v2/add_result/{test_id}'
        data = {
            'status_id': status_id,
            'comment': comment
        }
        response = requests.post(url, json=data, auth=self.auth)
        return response.json()