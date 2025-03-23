import requests

class TestimAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def trigger_test(self, test_id):
        url = f'https://api.testim.io/v1/tests/{test_id}/run'
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        response = requests.post(url, headers=headers)
        return response.json()