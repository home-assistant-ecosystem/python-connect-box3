"""API wrapper to get data from a Connect Box 3."""

from typing import List, Optional, Self

import httpx

from .httpx_client import ConnectBoxClient
from .models import (
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

# Endpoint definitions: (method_name, url, model_class, extract_key, store_attr)
_ENDPOINTS = [
    ("get_dhcp", "/network/ipv4/dhcp", DhcpConfig, "dhcp", "dhcp"),
    ("get_dmz", "/network/ipv4/dmz", Dmz, "dmz", "dmz"),
    (
        "get_first_install",
        "/system/firstinstall",
        FirstInstall,
        "firstInstall",
        "first_install",
    ),
    (
        "get_ipv4_firewall",
        "/network/ipv4/firewall",
        Firewall,
        "firewall",
        "ipv4_firewall",
    ),
    (
        "get_ipv6_firewall",
        "/network/ipv6/firewall",
        Firewall,
        "firewall",
        "ipv6_firewall",
    ),
    ("get_languages", "/system/languages", Languages, "languages", "languages"),
    ("get_lanstatus", "/network/ipv4/info", LanStatus, "info", "lanstatus"),
    ("get_led", "/network/ledlight", LedLight, None, "led"),
    (
        "get_localization",
        "/system/localization",
        Localization,
        "localization",
        "localization",
    ),
    ("get_login_status", "/user/login", LoginDetails, "loginDetails", "login_status"),
    ("get_modem_mode", "/system/modemmode", ModemMode, "modemmode", "modem_mode"),
    ("get_pon_state", "/pon/state", PonState, "pon", "pon_state"),
    ("get_pon_status", "/pon/status", PonStatus, None, "pon_status"),
    (
        "get_provisioning",
        "/system/gateway/provisioning",
        Provisioning,
        "provisioning",
        "provisioning",
    ),
    (
        "get_software_update",
        "/system/softwareupdate",
        SoftwareUpdate,
        "softwareUpdate",
        "software_update",
    ),
    ("get_system_info", "/system/info", SystemInfo, "info", "system_info"),
    ("get_ui_screens", "/system/ui/screens", UiScreens, None, "ui_screens"),
    ("get_upnp", "/network/upnp", Upnp, "upnp", "upnp"),
    (
        "get_wifi_band2g_config",
        "/wifi/band2g/config",
        WifiConfig,
        "config",
        "wifi_band2g_config",
    ),
    (
        "get_wifi_band2g_state",
        "/wifi/band2g/state",
        WifiState,
        "state",
        "wifi_band2g_state",
    ),
    (
        "get_wifi_band2g_wps_config",
        "/wifi/band2g/wps/config",
        WpsConfig,
        "config",
        "wifi_band2g_wps_config",
    ),
    (
        "get_wifi_band2g_wps_jobs",
        "/wifi/band2g/wps/pairing/jobs",
        WpsPairingJobs,
        "jobs",
        "wifi_band2g_wps_jobs",
    ),
    (
        "get_wifi_band5g_config",
        "/wifi/band5g/config",
        WifiConfig,
        "config",
        "wifi_band5g_config",
    ),
    (
        "get_wifi_band5g_state",
        "/wifi/band5g/state",
        WifiState,
        "state",
        "wifi_band5g_state",
    ),
    (
        "get_wifi_band5g_wps_config",
        "/wifi/band5g/wps/config",
        WpsConfig,
        "config",
        "wifi_band5g_wps_config",
    ),
    (
        "get_wifi_band5g_wps_jobs",
        "/wifi/band5g/wps/pairing/jobs",
        WpsPairingJobs,
        "jobs",
        "wifi_band5g_wps_jobs",
    ),
]


def _make_getter(url, model_cls, extract_key=None, store_attr=None):
    """Factory to create async getter methods for ConnectBox."""

    async def method(self):
        """Generic method to retrieve data from a Connect Box endpoint."""
        response = await self._client.request("GET", url)
        data = response.json()
        if extract_key:
            data = data.get(extract_key, {})
        result = model_cls.from_dict(data)
        if store_attr:
            setattr(self, store_attr, result)
        return result

    return method


class ConnectBox:
    """Class for handling the data retrieval from a Connect Box 3."""

    def __init__(
        self,
        password: str,
        host: str = "192.168.0.1",
        session: httpx.AsyncClient | None = None,
    ):
        """Initialize the connection."""
        self.base_url = f"http://{host}/rest/v1"
        self._client = ConnectBoxClient(base_url=self.base_url, session=session)
        self.host: str = host
        self.password: str = password
        self.dhcp: DhcpConfig | None = None
        self.dmz: Dmz | None = None
        self.first_install: FirstInstall | None = None
        self.hosts: list[Host] | None = None
        self.ipv4_firewall: Firewall | None = None
        self.ipv6_firewall: Firewall | None = None
        self.languages: Languages | None = None
        self.lanstatus: LanStatus | None = None
        self.led: LedLight | None = None
        self.localization: Localization | None = None
        self.login_status: LoginDetails | None = None
        self.modem_mode: ModemMode | None = None
        self.mta_lines: list[MtaLineEntry] | None = None
        self.pon_state: PonState | None = None
        self.pon_status: PonStatus | None = None
        self.provisioning: Provisioning | None = None
        self.software_update: SoftwareUpdate | None = None
        self.system_info: SystemInfo | None = None
        self.ui_screens: UiScreens | None = None
        self.upnp: Upnp | None = None
        self.user_language: UserLanguage | None = None
        self.wifi_band2g_config: WifiConfig | None = None
        self.wifi_band2g_state: WifiState | None = None
        self.wifi_band2g_wps_config: WpsConfig | None = None
        self.wifi_band2g_wps_jobs: WpsPairingJobs | None = None
        self.wifi_band5g_config: WifiConfig | None = None
        self.wifi_band5g_state: WifiState | None = None
        self.wifi_band5g_wps_config: WpsConfig | None = None
        self.wifi_band5g_wps_jobs: WpsPairingJobs | None = None

    async def login(self, password: str) -> dict:
        """Authenticate with the Connect Box and store the session token."""
        return await self._client.login(password)

    async def logout(self, user_id: int = 3) -> None:
        """Delete user token (logout)."""
        await self._client.request(
            "DELETE", f"/user/{user_id}/token/{self._client._token}"
        )
        self._client._token = None

    async def get_user_language(self, user_id: int = 3) -> UserLanguage:
        """Get user language preference."""
        response = await self._client.request("GET", f"/user/{user_id}/language")
        data = response.json()
        self.user_language = UserLanguage.from_dict(data.get("language", {}))
        return self.user_language

    async def get_hosts(self, connected_only: bool = True) -> list[Host]:
        """Get network hosts."""
        params = {"connectedOnly": str(connected_only).lower()}
        response = await self._client.request("GET", "/network/hosts", params=params)
        data = response.json()
        self.hosts = [Host.from_dict(h) for h in data["hosts"]["hosts"]]
        return self.hosts

    async def get_mta_lines(self) -> list[MtaLineEntry]:
        """Get MTA lines information."""
        response = await self._client.request("GET", "/mta/lines")
        data = response.json()
        self.mta_lines = [MtaLineEntry.from_dict(e) for e in data.get("lines", [])]
        return self.mta_lines

    async def set_led(self, brightness: int) -> LedLight:
        """Set LED brightness."""
        response = await self._client.request(
            "PUT", "/network/ledlight", json={"value": str(brightness)}
        )
        self.led = LedLight.from_dict(response.json())
        return self.led

    async def reboot_device(self) -> None:
        """Request that the device reboot."""
        await self._client.request("POST", "/system/reboot")
        self._client._token = None

    async def close(self) -> None:
        """Close the underlying HTTP session."""
        await self._client.close()

    async def __aenter__(self) -> Self:
        """Support async context manager entry."""
        await self._client.__aenter__()
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None,
        exc: BaseException | None, tb: object
    ) -> None:
        """Support async context manager exit."""
        await self._client.__aexit__(exc_type, exc, tb)


for _name, _url, _model, _key, _attr in _ENDPOINTS:
    setattr(ConnectBox, _name, _make_getter(_url, _model, _key, _attr))
