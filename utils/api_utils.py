import requests

class APIUtils:
    @staticmethod
    def get(url, headers=None):
        response = requests.get(url, headers=headers)
        return response.json()

    @staticmethod
    def post(url, data, headers=None):
        response = requests.post(url, json=data, headers=headers)
        return response.json()

    @staticmethod
    def put(url, data, headers=None):
        response = requests.put(url, json=data, headers=headers)
        return response.json()

    @staticmethod
    def delete(url, headers=None):
        response = requests.delete(url, headers=headers)
        return response.json()