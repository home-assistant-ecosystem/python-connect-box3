"""Tests for the ConnectBox client."""

import httpx
import pytest
from connect_box3 import ConnectBox
from connect_box3.exceptions import (
    ConnectBoxConnectionError,
    ConnectBoxError,
    ConnectBoxLoginError,
    ConnectBoxTimeoutError,
)
from connect_box3.models import (
    DhcpConfig,
    Dmz,
    Firewall,
    FirstInstall,
    Host,
    Languages,
    LanStatus,
    LedLight,
    Localization,
    LoginDetails,
    ModemMode,
    MtaLineEntry,
    PonState,
    PonStatus,
    Provisioning,
    SoftwareUpdate,
    SystemInfo,
    UiScreens,
    Upnp,
    UserLanguage,
    WifiConfig,
    WifiState,
    WpsConfig,
    WpsPairingJobs,
)

BASE_URL = "http://192.168.0.1/rest/v1"


@pytest.mark.asyncio
async def test_login(client, httpx_mock):
    """Test login stores the token."""
    httpx_mock.add_response(
        url=f"{BASE_URL}/user/login",
        method="POST",
        json={"created": {"token": "abc123"}},
    )
    await client.login("testpass")
    assert client._client._token == "abc123"


@pytest.mark.asyncio
async def test_login_bad_response(client, httpx_mock):
    """Test login raises on unexpected response."""
    httpx_mock.add_response(
        url=f"{BASE_URL}/user/login", method="POST", json={"error": "invalid"}
    )
    with pytest.raises(ConnectBoxLoginError):
        await client.login("testpass")


@pytest.mark.asyncio
async def test_logout(client, httpx_mock):
    """Test logout clears the token."""
    httpx_mock.add_response(
        url=f"{BASE_URL}/user/login",
        method="POST",
        json={"created": {"token": "abc123"}},
    )
    await client.login("testpass")

    httpx_mock.add_response(url=f"{BASE_URL}/user/3/token/abc123", method="DELETE")
    await client.logout()
    assert client._client._token is None


@pytest.mark.asyncio
async def test_reboot_device(client, httpx_mock):
    """Test reboot clears the token."""
    client._client._token = "abc123"
    httpx_mock.add_response(url=f"{BASE_URL}/system/reboot", method="POST")
    await client.reboot_device()
    assert client._client._token is None


@pytest.mark.asyncio
async def test_get_localization(client, httpx_mock):
    """Test get_localization returns Localization dataclass."""
    httpx_mock.add_response(
        url=f"{BASE_URL}/system/localization",
        json={
            "localization": {
                "modelName": "F5685LGB",
                "productName": "Connect Box 3",
                "skin": "sunrise",
            }
        },
    )
    result = await client.get_localization()
    assert isinstance(result, Localization)
    assert result.modelName == "F5685LGB"
    assert result.productName == "Connect Box 3"
    assert result.skin == "sunrise"


@pytest.mark.asyncio
async def test_get_system_info(client, httpx_mock):
    """Test get_system_info returns SystemInfo and stores it."""
    client._client._token = "tok"
    httpx_mock.add_response(
        url=f"{BASE_URL}/system/info",
        json={
            "info": {
                "modelName": "F5685LGB",
                "softwareVersion": "4.11.1",
                "hardwareVersion": "1.2.1b",
            }
        },
    )
    result = await client.get_system_info()
    assert isinstance(result, SystemInfo)
    assert result.modelName == "F5685LGB"
    assert result.softwareVersion == "4.11.1"
    assert client.system_info is result


@pytest.mark.asyncio
async def test_get_pon_state(client, httpx_mock):
    """Test get_pon_state extracts from 'pon' key."""
    client._client._token = "tok"
    httpx_mock.add_response(
        url=f"{BASE_URL}/pon/state",
        json={"mac": "c4:eb:43:00:00:01", "pon": {"status": "Online", "upTime": 12345}},
    )
    result = await client.get_pon_state()
    assert isinstance(result, PonState)
    assert result.status == "Online"
    assert result.upTime == 12345


@pytest.mark.asyncio
async def test_get_pon_status(client, httpx_mock):
    """Test get_pon_status returns PonStatus and stores it."""
    client._client._token = "tok"
    httpx_mock.add_response(
        url=f"{BASE_URL}/pon/status",
        json={
            "interface": {"transceiverTemp": 31.0, "laserBiasCurrent": "11000"},
            "status": {"status": "Online", "connectionMode": "IPOE"},
        },
    )
    result = await client.get_pon_status()
    assert isinstance(result, PonStatus)
    assert result.interface.transceiverTemp == 31.0
    assert result.status.status == "Online"
    assert client.pon_status is result


@pytest.mark.asyncio
async def test_get_modem_mode(client, httpx_mock):
    """Test get_modem_mode returns ModemMode."""
    httpx_mock.add_response(
        url=f"{BASE_URL}/system/modemmode", json={"modemmode": {"enable": False}}
    )
    result = await client.get_modem_mode()
    assert isinstance(result, ModemMode)
    assert result.enable is False


@pytest.mark.asyncio
async def test_get_first_install(client, httpx_mock):
    """Test get_first_install returns FirstInstall."""
    httpx_mock.add_response(
        url=f"{BASE_URL}/system/firstinstall", json={"firstInstall": {"complete": True}}
    )
    result = await client.get_first_install()
    assert isinstance(result, FirstInstall)
    assert result.complete is True


@pytest.mark.asyncio
async def test_get_languages(client, httpx_mock):
    """Test get_languages returns Languages."""
    httpx_mock.add_response(
        url=f"{BASE_URL}/system/languages",
        json={"languages": {"languages": ["en", "de", "fr"]}},
    )
    result = await client.get_languages()
    assert isinstance(result, Languages)
    assert result.languages == ["en", "de", "fr"]


@pytest.mark.asyncio
async def test_get_login_status(client, httpx_mock):
    """Test get_login_status returns LoginDetails."""
    httpx_mock.add_response(
        url=f"{BASE_URL}/user/login",
        method="GET",
        json={"loginDetails": {"numberOfContiguousFailures": "0", "lockoutTime": "0"}},
    )
    result = await client.get_login_status()
    assert isinstance(result, LoginDetails)
    assert result.numberOfContiguousFailures == "0"


@pytest.mark.asyncio
async def test_get_software_update(client, httpx_mock):
    """Test get_software_update returns SoftwareUpdate."""
    client._client._token = "tok"
    httpx_mock.add_response(
        url=f"{BASE_URL}/system/softwareupdate",
        json={"softwareUpdate": {"status": "not_started"}},
    )
    result = await client.get_software_update()
    assert isinstance(result, SoftwareUpdate)
    assert result.status == "not_started"


@pytest.mark.asyncio
async def test_get_provisioning(client, httpx_mock):
    """Test get_provisioning returns Provisioning."""
    client._client._token = "tok"
    httpx_mock.add_response(
        url=f"{BASE_URL}/system/gateway/provisioning",
        json={"provisioning": {"mode": "ipv4", "macAddress": "aa:bb:cc:dd:ee:ff"}},
    )
    result = await client.get_provisioning()
    assert isinstance(result, Provisioning)
    assert result.mode == "ipv4"


@pytest.mark.asyncio
async def test_get_lanstatus(client, httpx_mock):
    """Test get_lanstatus returns LanStatus and stores it."""
    client._client._token = "tok"
    httpx_mock.add_response(
        url=f"{BASE_URL}/network/ipv4/info",
        json={
            "info": {
                "lanIpAddress": "192.168.1.1",
                "lanSubnet": "192.168.1.0",
                "lanSubnetMask": "255.255.255.0",
            }
        },
    )
    result = await client.get_lanstatus()
    assert isinstance(result, LanStatus)
    assert result.lanIpAddress == "192.168.1.1"
    assert client.lanstatus is result


@pytest.mark.asyncio
async def test_get_led(client, httpx_mock):
    """Test get_led returns LedLight and stores it."""
    client._client._token = "tok"
    httpx_mock.add_response(
        url=f"{BASE_URL}/network/ledlight", method="GET", json={"value": "35"}
    )
    result = await client.get_led()
    assert isinstance(result, LedLight)
    assert client.led is result


@pytest.mark.asyncio
async def test_set_led(client, httpx_mock):
    """Test set_led returns LedLight and stores it."""
    client._client._token = "tok"
    httpx_mock.add_response(
        url=f"{BASE_URL}/network/ledlight", method="PUT", json={"value": "50"}
    )
    result = await client.set_led(50)
    assert isinstance(result, LedLight)
    assert client.led is result


@pytest.mark.asyncio
async def test_get_dhcp(client, httpx_mock):
    """Test get_dhcp returns DhcpConfig."""
    client._client._token = "tok"
    httpx_mock.add_response(
        url=f"{BASE_URL}/network/ipv4/dhcp",
        json={
            "dhcp": {
                "enable": True,
                "minAddress": "192.168.1.10",
                "maxAddress": "192.168.1.254",
            }
        },
    )
    result = await client.get_dhcp()
    assert isinstance(result, DhcpConfig)
    assert result.enable is True
    assert result.minAddress == "192.168.1.10"


@pytest.mark.asyncio
async def test_get_dmz(client, httpx_mock):
    """Test get_dmz returns Dmz."""
    client._client._token = "tok"
    httpx_mock.add_response(
        url=f"{BASE_URL}/network/ipv4/dmz",
        json={"dmz": {"enable": False, "internalIp": "192.168.1.0"}},
    )
    result = await client.get_dmz()
    assert isinstance(result, Dmz)
    assert result.enable is False


@pytest.mark.asyncio
async def test_get_ipv4_firewall(client, httpx_mock):
    """Test get_ipv4_firewall returns Firewall."""
    client._client._token = "tok"
    httpx_mock.add_response(
        url=f"{BASE_URL}/network/ipv4/firewall",
        json={
            "firewall": {"enable": True, "portScanProtect": True, "ipFloodDetect": True}
        },
    )
    result = await client.get_ipv4_firewall()
    assert isinstance(result, Firewall)
    assert result.enable is True


@pytest.mark.asyncio
async def test_get_upnp(client, httpx_mock):
    """Test get_upnp returns Upnp."""
    client._client._token = "tok"
    httpx_mock.add_response(
        url=f"{BASE_URL}/network/upnp", json={"upnp": {"enable": True}}
    )
    result = await client.get_upnp()
    assert isinstance(result, Upnp)
    assert result.enable is True


@pytest.mark.asyncio
async def test_get_wifi_band2g_state(client, httpx_mock):
    """Test get_wifi_band2g_state returns WifiState."""
    client._client._token = "tok"
    httpx_mock.add_response(
        url=f"{BASE_URL}/wifi/band2g/state",
        json={"state": {"enable": True, "status": "up"}},
    )
    result = await client.get_wifi_band2g_state()
    assert isinstance(result, WifiState)
    assert result.enable is True


@pytest.mark.asyncio
async def test_get_wifi_band2g_config(client, httpx_mock):
    """Test get_wifi_band2g_config returns WifiConfig."""
    client._client._token = "tok"
    httpx_mock.add_response(
        url=f"{BASE_URL}/wifi/band2g/config",
        json={"config": {"enable": True, "ssid": {"ssid": "MyNetwork"}}},
    )
    result = await client.get_wifi_band2g_config()
    assert isinstance(result, WifiConfig)
    assert result.enable is True
    assert result.ssid.ssid == "MyNetwork"


@pytest.mark.asyncio
async def test_get_wifi_band2g_wps_config(client, httpx_mock):
    """Test get_wifi_band2g_wps_config returns WpsConfig."""
    client._client._token = "tok"
    httpx_mock.add_response(
        url=f"{BASE_URL}/wifi/band2g/wps/config", json={"config": {"enable": True}}
    )
    result = await client.get_wifi_band2g_wps_config()
    assert isinstance(result, WpsConfig)
    assert result.enable is True


@pytest.mark.asyncio
async def test_get_wifi_band2g_wps_jobs(client, httpx_mock):
    """Test get_wifi_band2g_wps_jobs returns WpsPairingJobs."""
    client._client._token = "tok"
    httpx_mock.add_response(
        url=f"{BASE_URL}/wifi/band2g/wps/pairing/jobs",
        json={"jobs": {"pairingJobs": []}},
    )
    result = await client.get_wifi_band2g_wps_jobs()
    assert isinstance(result, WpsPairingJobs)
    assert result.pairingJobs == []


@pytest.mark.asyncio
async def test_get_ui_screens(client, httpx_mock):
    """Test get_ui_screens returns UiScreens."""
    client._client._token = "tok"
    httpx_mock.add_response(
        url=f"{BASE_URL}/system/ui/screens",
        json={"screens": {"dns": {"display": False}, "ddns": {"display": True}}},
    )
    result = await client.get_ui_screens()
    assert isinstance(result, UiScreens)
    assert result.screens["dns"].display is False
    assert result.screens["ddns"].display is True


@pytest.mark.asyncio
async def test_get_user_language(client, httpx_mock):
    """Test get_user_language extracts from 'language' key."""
    client._client._token = "tok"
    httpx_mock.add_response(
        url=f"{BASE_URL}/user/3/language", json={"language": {"language": "de"}}
    )
    result = await client.get_user_language()
    assert isinstance(result, UserLanguage)
    assert result.language == "de"


@pytest.mark.asyncio
async def test_get_hosts(client, httpx_mock):
    """Test get_hosts returns list of Host."""
    client._client._token = "tok"
    httpx_mock.add_response(
        url=f"{BASE_URL}/network/hosts?connectedOnly=true",
        json={
            "hosts": {
                "hosts": [
                    {
                        "macAddress": "AA:BB:CC:DD:EE:FF",
                        "config": {"hostname": "mypc", "connected": True},
                    }
                ]
            }
        },
    )
    result = await client.get_hosts()
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], Host)
    assert result[0].macAddress == "AA:BB:CC:DD:EE:FF"
    assert result[0].config.hostname == "mypc"


@pytest.mark.asyncio
async def test_get_hosts_all(client, httpx_mock):
    """Test get_hosts with connected_only=False."""
    client._client._token = "tok"
    httpx_mock.add_response(
        url=f"{BASE_URL}/network/hosts?connectedOnly=false",
        json={"hosts": {"hosts": []}},
    )
    result = await client.get_hosts(connected_only=False)
    assert result == []


@pytest.mark.asyncio
async def test_get_mta_lines(client, httpx_mock):
    """Test get_mta_lines returns list of MtaLineEntry."""
    client._client._token = "tok"
    httpx_mock.add_response(
        url=f"{BASE_URL}/mta/lines",
        json={"lines": [{"id": 1, "line": {"enable": False, "operational": False}}]},
    )
    result = await client.get_mta_lines()
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], MtaLineEntry)
    assert result[0].id == 1
    assert result[0].line.enable is False


@pytest.mark.asyncio
async def test_context_manager(httpx_mock):
    """Test async context manager."""
    async with ConnectBox("testpass", host="192.168.0.1") as client:
        assert isinstance(client, ConnectBox)


@pytest.mark.asyncio
async def test_request_401_raises_login_error(client, httpx_mock):
    """Test that 401 response raises ConnectBoxLoginError."""
    client._client._token = "tok"
    httpx_mock.add_response(url=f"{BASE_URL}/system/info", status_code=401)
    with pytest.raises(ConnectBoxLoginError):
        await client.get_system_info()


@pytest.mark.asyncio
async def test_request_500_raises_error(client, httpx_mock):
    """Test that 500 response raises ConnectBoxError."""
    client._client._token = "tok"
    httpx_mock.add_response(url=f"{BASE_URL}/system/info", status_code=500)
    with pytest.raises(ConnectBoxError):
        await client.get_system_info()


@pytest.mark.asyncio
async def test_request_timeout_raises_timeout_error(client, httpx_mock):
    """Test that timeout raises ConnectBoxTimeoutError."""
    httpx_mock.add_exception(
        httpx.ReadTimeout("timed out"), url=f"{BASE_URL}/system/localization"
    )
    with pytest.raises(ConnectBoxTimeoutError):
        await client.get_localization()


@pytest.mark.asyncio
async def test_request_connection_error(client, httpx_mock):
    """Test that connection error raises ConnectBoxConnectionError."""
    httpx_mock.add_exception(
        httpx.ConnectError("refused"), url=f"{BASE_URL}/system/localization"
    )
    with pytest.raises(ConnectBoxConnectionError):
        await client.get_localization()
