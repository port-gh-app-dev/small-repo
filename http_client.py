import requests


class HttpClient:
    """A simple HTTP client for interacting with a RESTful API."""

    def __init__(self, base_url: str, headers: dict | None = None, timeout: int = 30):
        """
        Initialize the HTTP client.

        Args:
            base_url: The base URL of the API (e.g. "https://api.example.com").
            headers: Optional default headers to include in every request.
            timeout: Request timeout in seconds (default: 30).
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update(headers or {})

    def get(self, path: str, params: dict | None = None) -> requests.Response:
        """
        Perform a GET request.

        Args:
            path: The API path (e.g. "/users/1").
            params: Optional query parameters.

        Returns:
            The HTTP response.
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = self._session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response

    def post(self, path: str, data: dict | None = None) -> requests.Response:
        """
        Perform a POST request.

        Args:
            path: The API path (e.g. "/users").
            data: The JSON body to send.

        Returns:
            The HTTP response.
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = self._session.post(url, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response

    def put(self, path: str, data: dict | None = None) -> requests.Response:
        """
        Perform a PUT request.

        Args:
            path: The API path (e.g. "/users/1").
            data: The JSON body to send.

        Returns:
            The HTTP response.
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = self._session.put(url, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response

    def delete(self, path: str) -> requests.Response:
        """
        Perform a DELETE request.

        Args:
            path: The API path (e.g. "/users/1").

        Returns:
            The HTTP response.
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = self._session.delete(url, timeout=self.timeout)
        response.raise_for_status()
        return response

    def close(self):
        """Close the underlying HTTP session."""
        self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
