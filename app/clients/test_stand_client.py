import requests


class TestStandClient():

    @staticmethod
    def is_stand_healthy(url):
        return requests.get(f"http://{url}").status_code == 200
