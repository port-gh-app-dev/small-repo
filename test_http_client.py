import pytest
import requests

from http_client import HttpClient


BASE_URL = "https://api.example.com"


@pytest.fixture
def client(mocker):
    """Return an HttpClient with a mocked underlying session."""
    mock_session = mocker.MagicMock()
    mocker.patch("http_client.requests.Session", return_value=mock_session)
    return HttpClient(BASE_URL), mock_session


# ---------------------------------------------------------------------------
# Initialisation
# ---------------------------------------------------------------------------

class TestInit:
    def test_base_url_trailing_slash_stripped(self, mocker):
        mocker.patch("http_client.requests.Session")
        c = HttpClient("https://api.example.com/")
        assert c.base_url == "https://api.example.com"

    def test_default_timeout(self, mocker):
        mocker.patch("http_client.requests.Session")
        c = HttpClient(BASE_URL)
        assert c.timeout == 30

    def test_custom_timeout(self, mocker):
        mocker.patch("http_client.requests.Session")
        c = HttpClient(BASE_URL, timeout=10)
        assert c.timeout == 10

    def test_default_headers_applied_to_session(self, mocker):
        mock_session = mocker.MagicMock()
        mocker.patch("http_client.requests.Session", return_value=mock_session)
        HttpClient(BASE_URL, headers={"Authorization": "Bearer token"})
        mock_session.headers.update.assert_called_once_with({"Authorization": "Bearer token"})

    def test_no_headers_uses_empty_dict(self, mocker):
        mock_session = mocker.MagicMock()
        mocker.patch("http_client.requests.Session", return_value=mock_session)
        HttpClient(BASE_URL)
        mock_session.headers.update.assert_called_once_with({})


# ---------------------------------------------------------------------------
# GET
# ---------------------------------------------------------------------------

class TestGet:
    def test_correct_url_constructed(self, client):
        http_client, mock_session = client
        mock_session.get.return_value.status_code = 200
        mock_session.get.return_value.raise_for_status.return_value = None

        http_client.get("/users/1")

        mock_session.get.assert_called_once_with(
            f"{BASE_URL}/users/1", params=None, timeout=30
        )

    def test_leading_slash_in_path_normalised(self, client):
        http_client, mock_session = client
        mock_session.get.return_value.raise_for_status.return_value = None

        http_client.get("users/1")

        args, kwargs = mock_session.get.call_args
        assert args[0] == f"{BASE_URL}/users/1"

    def test_query_params_forwarded(self, client):
        http_client, mock_session = client
        mock_session.get.return_value.raise_for_status.return_value = None

        http_client.get("/search", params={"q": "hello"})

        mock_session.get.assert_called_once_with(
            f"{BASE_URL}/search", params={"q": "hello"}, timeout=30
        )

    def test_returns_response(self, client):
        http_client, mock_session = client
        fake_response = mock_session.get.return_value
        fake_response.raise_for_status.return_value = None

        result = http_client.get("/users")

        assert result is fake_response

    def test_raises_for_http_error(self, client):
        http_client, mock_session = client
        mock_session.get.return_value.raise_for_status.side_effect = requests.HTTPError("404")

        with pytest.raises(requests.HTTPError):
            http_client.get("/missing")


# ---------------------------------------------------------------------------
# POST
# ---------------------------------------------------------------------------

class TestPost:
    def test_correct_url_and_json_body(self, client):
        http_client, mock_session = client
        mock_session.post.return_value.raise_for_status.return_value = None

        http_client.post("/users", data={"name": "Alice"})

        mock_session.post.assert_called_once_with(
            f"{BASE_URL}/users", json={"name": "Alice"}, timeout=30
        )

    def test_no_body_sends_none(self, client):
        http_client, mock_session = client
        mock_session.post.return_value.raise_for_status.return_value = None

        http_client.post("/users")

        mock_session.post.assert_called_once_with(
            f"{BASE_URL}/users", json=None, timeout=30
        )

    def test_returns_response(self, client):
        http_client, mock_session = client
        mock_session.post.return_value.raise_for_status.return_value = None

        result = http_client.post("/users")

        assert result is mock_session.post.return_value

    def test_raises_for_http_error(self, client):
        http_client, mock_session = client
        mock_session.post.return_value.raise_for_status.side_effect = requests.HTTPError("400")

        with pytest.raises(requests.HTTPError):
            http_client.post("/users", data={"bad": "payload"})


# ---------------------------------------------------------------------------
# PUT
# ---------------------------------------------------------------------------

class TestPut:
    def test_correct_url_and_json_body(self, client):
        http_client, mock_session = client
        mock_session.put.return_value.raise_for_status.return_value = None

        http_client.put("/users/1", data={"name": "Bob"})

        mock_session.put.assert_called_once_with(
            f"{BASE_URL}/users/1", json={"name": "Bob"}, timeout=30
        )

    def test_no_body_sends_none(self, client):
        http_client, mock_session = client
        mock_session.put.return_value.raise_for_status.return_value = None

        http_client.put("/users/1")

        mock_session.put.assert_called_once_with(
            f"{BASE_URL}/users/1", json=None, timeout=30
        )

    def test_returns_response(self, client):
        http_client, mock_session = client
        mock_session.put.return_value.raise_for_status.return_value = None

        result = http_client.put("/users/1")

        assert result is mock_session.put.return_value

    def test_raises_for_http_error(self, client):
        http_client, mock_session = client
        mock_session.put.return_value.raise_for_status.side_effect = requests.HTTPError("422")

        with pytest.raises(requests.HTTPError):
            http_client.put("/users/1", data={"bad": "data"})


# ---------------------------------------------------------------------------
# DELETE
# ---------------------------------------------------------------------------

class TestDelete:
    def test_correct_url(self, client):
        http_client, mock_session = client
        mock_session.delete.return_value.raise_for_status.return_value = None

        http_client.delete("/users/1")

        mock_session.delete.assert_called_once_with(
            f"{BASE_URL}/users/1", timeout=30
        )

    def test_returns_response(self, client):
        http_client, mock_session = client
        mock_session.delete.return_value.raise_for_status.return_value = None

        result = http_client.delete("/users/1")

        assert result is mock_session.delete.return_value

    def test_raises_for_http_error(self, client):
        http_client, mock_session = client
        mock_session.delete.return_value.raise_for_status.side_effect = requests.HTTPError("404")

        with pytest.raises(requests.HTTPError):
            http_client.delete("/users/999")


# ---------------------------------------------------------------------------
# Session lifecycle / context manager
# ---------------------------------------------------------------------------

class TestLifecycle:
    def test_close_calls_session_close(self, client):
        http_client, mock_session = client
        http_client.close()
        mock_session.close.assert_called_once()

    def test_context_manager_calls_close(self, mocker):
        mock_session = mocker.MagicMock()
        mocker.patch("http_client.requests.Session", return_value=mock_session)

        with HttpClient(BASE_URL):
            pass

        mock_session.close.assert_called_once()

    def test_context_manager_returns_client(self, mocker):
        mock_session = mocker.MagicMock()
        mocker.patch("http_client.requests.Session", return_value=mock_session)

        with HttpClient(BASE_URL) as c:
            assert isinstance(c, HttpClient)

    def test_context_manager_closes_on_exception(self, mocker):
        mock_session = mocker.MagicMock()
        mocker.patch("http_client.requests.Session", return_value=mock_session)

        with pytest.raises(ValueError):
            with HttpClient(BASE_URL):
                raise ValueError("something went wrong")

        mock_session.close.assert_called_once()
