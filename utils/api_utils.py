import requests


class APIUtils:
    """A utility class for making HTTP API requests."""

    def get_headers(self):
        """Returns standard headers for API requests."""
        return {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def make_post_request(self, payload, url: str):
        """Makes a POST request to the specified URL with the given payload.

        Args:
            payload: The JSON payload for the request.
            url: The URL to send the POST request to.

        Returns:
            The JSON response from the API, or None if the request fails.
        """
        try:
            response = requests.post(url, headers=self.get_headers(), data=payload)
            return response.json() # This can raise JSONDecodeError
        except requests.exceptions.RequestException as e:
            # Log the error for debugging purposes if logging is set up
            # For now, just return None as per requirements
            return None

    def make_patch_request(self, payload, url: str):
        """Makes a PATCH request to the specified URL with the given payload.

        Args:
            payload: The JSON payload for the request.
            url: The URL to send the PATCH request to.

        Returns:
            The JSON response from the API, or None if the request fails.
        """
        try:
            response = requests.patch(url, headers=self.get_headers(), data=payload)
            return response.json() # This can raise JSONDecodeError
        except requests.exceptions.RequestException as e:
            # Log the error for debugging purposes if logging is set up
            # For now, just return None as per requirements
            return None

    def make_get_request(self, url: str):
        """Makes a GET request to the specified URL.

        Args:
            url: The URL to send the GET request to.

        Returns:
            The JSON response from the API, or None if the request fails.
        """
        try:
            response = requests.get(url, headers=self.get_headers())
            return response.json() # This can raise JSONDecodeError
        except requests.exceptions.RequestException as e:
            # Log the error for debugging purposes if logging is set up
            # For now, just return None as per requirements
            return None
