"""Exceptions for Connect Box 3 API client."""


class ConnectBoxError(Exception):
    """General ConnectBoxError exception occurred."""


class ConnectBoxConnectionError(ConnectBoxError):
    """When a connection error is encountered."""


class ConnectBoxTimeoutError(ConnectBoxConnectionError):
    """When a request times out."""


class ConnectBoxNoDataAvailable(ConnectBoxError):
    """When no data is available."""


class ConnectBoxLoginError(ConnectBoxError):
    """When login fails."""
