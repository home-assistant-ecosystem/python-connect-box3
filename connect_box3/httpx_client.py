"""Asynchronous Connect Box client using httpx."""

from typing import Optional

import httpx

from .exceptions import (
    ConnectBoxConnectionError,
    ConnectBoxError,
    ConnectBoxLoginError,
    ConnectBoxTimeoutError,
)


class ConnectBoxClient:
    """Client for interacting with the Connect Box 3 API using httpx."""

    def __init__(self, base_url: str, session: httpx.AsyncClient | None = None):
        """Initialize the client with the base URL and an optional httpx session."""
        self.base_url = base_url.rstrip("/")
        self._external_session = session is not None
        self.session = session or httpx.AsyncClient(
            base_url=self.base_url, timeout=25.0
        )
        self._token = None

    async def login(self, password: str) -> dict:
        """Authenticate and store the session token if provided."""
        url = "/user/login"
        payload = {"password": password}
        try:
            response = await self.request("POST", url, json=payload)
        except ConnectBoxError:
            raise
        except Exception as err:
            raise ConnectBoxConnectionError(f"Login connection failed: {err}") from err
        data = response.json()
        try:
            self._token = data["created"]["token"]
        except (KeyError, TypeError) as err:
            raise ConnectBoxLoginError(
                f"Login failed: unexpected response: {data}"
            ) from err
        return data

    async def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """Make an HTTP request with automatic token injection."""
        headers = kwargs.get("headers", {})
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        kwargs["headers"] = headers
        try:
            response = await self.session.request(method, url, **kwargs)
        except httpx.TimeoutException as err:
            raise ConnectBoxTimeoutError(f"Request timed out: {method} {url}") from err
        except httpx.ConnectError as err:
            raise ConnectBoxConnectionError(
                f"Connection failed: {method} {url}: {err}"
            ) from err
        except httpx.HTTPError as err:
            raise ConnectBoxConnectionError(
                f"HTTP error: {method} {url}: {err}"
            ) from err
        if response.status_code == 401:
            raise ConnectBoxLoginError(f"Authentication failed: {method} {url}")
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as err:
            raise ConnectBoxError(
                f"Request failed ({response.status_code}): {method} {url}"
            ) from err
        return response

    async def close(self):
        """Close the HTTP session if it was created internally."""
        if not self._external_session:
            await self.session.aclose()

    async def __aenter__(self):
        """Allow use as an asynchronous context manager."""
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """Ensure the session is closed when exiting the context."""
        await self.close()
