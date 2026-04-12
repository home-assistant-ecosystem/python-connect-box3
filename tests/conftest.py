"""Configuration for pytest."""

import pytest
from connect_box3 import ConnectBox

BASE_URL = "http://192.168.0.1/rest/v1"


@pytest.fixture
def client():
    """Create a ConnectBox client."""
    return ConnectBox(password="testpass", host="192.168.0.1")
