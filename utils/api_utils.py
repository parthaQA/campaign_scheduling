import requests


class APIUtils:

    def get_headers(self):
        """Returns the headers for API requests."""
        return {
            'accept': '*/*',
            'Content-Type': 'application/json'
        }

    def make_post_request(self, payload, url):
        try:
            response = requests.post(url, headers=self.get_headers(), data=payload)
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Request failed: {str(e)}"

    def make_patch_request(self, payload, url):
        try:
            response = requests.patch(url, headers=self.get_headers(), data=payload)
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Request failed: {str(e)}"

    def make_get_request(self, url):
        try:
            response = requests.get(url, headers=self.get_headers())
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Request failed: {str(e)}"
