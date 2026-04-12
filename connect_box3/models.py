"""Data models for Connect Box 3."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from mashumaro.mixins.dict import DataClassDictMixin


@dataclass
class SystemInfo(DataClassDictMixin):
    """System information from /system/info."""

    modelName: str | None = None
    softwareVersion: str | None = None
    hardwareVersion: str | None = None


@dataclass
class Localization(DataClassDictMixin):
    """Localization from /system/localization."""

    modelName: str | None = None
    productName: str | None = None
    skin: str | None = None


@dataclass
class ModemMode(DataClassDictMixin):
    """Modem mode from /system/modemmode."""

    enable: bool | None = None


@dataclass
class FirstInstall(DataClassDictMixin):
    """First install status from /system/firstinstall."""

    complete: bool | None = None


@dataclass
class Languages(DataClassDictMixin):
    """Available languages from /system/languages."""

    languages: list[str] | None = None


@dataclass
class SoftwareUpdate(DataClassDictMixin):
    """Software update status from /system/softwareupdate."""

    status: str | None = None


@dataclass
class LoginDetails(DataClassDictMixin):
    """Login details from GET /user/login."""

    numberOfContiguousFailures: str | None = None
    lockoutTime: str | None = None


@dataclass
class UserLanguage(DataClassDictMixin):
    """User language from /user/3/language."""

    language: str | None = None


@dataclass
class ProvisioningIpv4(DataClassDictMixin):
    """IPv4 provisioning details."""

    address: str | None = None
    defaultGateway: str | None = None
    dnsServers: list[str] | None = None
    leaseTime: int | None = None
    expireTime: int | None = None


@dataclass
class ProvisioningDsLite(DataClassDictMixin):
    """DS-Lite provisioning details."""

    enable: bool | None = None


@dataclass
class Provisioning(DataClassDictMixin):
    """Gateway provisioning from /system/gateway/provisioning."""

    mode: str | None = None
    macAddress: str | None = None
    ipv4: ProvisioningIpv4 | None = None
    dsLite: ProvisioningDsLite | None = None


@dataclass
class PonInterface(DataClassDictMixin):
    """PON interface data from /pon/status."""

    transceiverTemp: float | None = None
    transceiverVoltage: str | None = None
    laserBiasCurrent: str | None = None
    transmitOpticalLevel: str | None = None
    opticalSignalLevel: str | None = None


@dataclass
class PonStatusInfo(DataClassDictMixin):
    """PON status info."""

    status: str | None = None
    connectionMode: str | None = None
    ipv4Firewall: bool | None = None
    ipData: str | None = None
    ipVoip: str | None = None


@dataclass
class PonStatus(DataClassDictMixin):
    """PON status from /pon/status."""

    interface: PonInterface | None = None
    status: PonStatusInfo | None = None


@dataclass
class PonState(DataClassDictMixin):
    """PON state from /pon/state."""

    status: str | None = None
    standardCompliance: str | None = None
    serialNumber: str | None = None
    upTime: int | None = None
    accessAllowed: bool | None = None


@dataclass
class LedLight(DataClassDictMixin):
    """LED light status from /network/ledlight."""

    value: int | None = None


@dataclass
class LanStatus(DataClassDictMixin):
    """LAN status from /network/ipv4/info."""

    lanIpAddress: str | None = None
    lanSubnet: str | None = None
    lanSubnetMask: str | None = None


@dataclass
class DhcpAllowedIp(DataClassDictMixin):
    """Allowed IP entry in DHCP config."""

    lanAllowedSubnetIp: str | None = None
    lanAllowedSubnetMask: str | None = None


@dataclass
class DhcpBlockedIp(DataClassDictMixin):
    """Blocked IP entry in DHCP config."""

    lanBlockedSubnetIp: str | None = None
    lanBlockedSubnetMask: str | None = None


@dataclass
class DhcpConfig(DataClassDictMixin):
    """DHCP configuration from /network/ipv4/dhcp."""

    enable: bool | None = None
    minAddress: str | None = None
    maxAddress: str | None = None
    subnetMask: str | None = None
    leaseTime: int | None = None
    maxIps: int | None = None
    allowedIps: list[DhcpAllowedIp] | None = None
    blockedIps: list[DhcpBlockedIp] | None = None


@dataclass
class Dmz(DataClassDictMixin):
    """DMZ configuration from /network/ipv4/dmz."""

    enable: bool | None = None
    internalIp: str | None = None


@dataclass
class Firewall(DataClassDictMixin):
    """Firewall settings from /network/ipv4/firewall or /network/ipv6/firewall."""

    enable: bool | None = None
    blockFragmentedIpPackets: bool | None = None
    portScanProtect: bool | None = None
    ipFloodDetect: bool | None = None


@dataclass
class Upnp(DataClassDictMixin):
    """UPnP configuration from /network/upnp."""

    enable: bool | None = None


@dataclass
class HostIpv4(DataClassDictMixin):
    """IPv4 info for a connected host."""

    address: str | None = None
    leaseTimeRemaining: int | None = None


@dataclass
class HostWifi(DataClassDictMixin):
    """WiFi info for a connected host."""

    band: str | None = None
    rssi: int | None = None
    ssid: str | None = None


@dataclass
class HostEthernet(DataClassDictMixin):
    """Ethernet info for a connected host."""

    port: int | None = None


@dataclass
class HostConfig(DataClassDictMixin):
    """Configuration of a connected host."""

    connected: bool | None = None
    deviceName: str | None = None
    deviceType: str | None = None
    hostname: str | None = None
    interface: str | None = None
    speed: float | None = None
    ipv4: HostIpv4 | None = None
    wifi: HostWifi | None = None
    ethernet: HostEthernet | None = None


@dataclass
class Host(DataClassDictMixin):
    """A connected host from /network/hosts."""

    macAddress: str | None = None
    config: HostConfig | None = None


@dataclass
class WifiSsid(DataClassDictMixin):
    """WiFi SSID configuration."""

    ssid: str | None = None
    broadcastSsid: bool | None = None
    securityType: str | None = None
    passphrase: str | None = None
    rekeyInterval: int | None = None
    encryptionType: str | None = None


@dataclass
class WifiRadio(DataClassDictMixin):
    """WiFi radio configuration."""

    channelMode: bool | None = None
    channel: int | None = None
    bandwidth: str | None = None


@dataclass
class WifiConfig(DataClassDictMixin):
    """WiFi band configuration from /wifi/band{2g,5g}/config."""

    enable: bool | None = None
    ssid: WifiSsid | None = None
    radio: WifiRadio | None = None


@dataclass
class WifiState(DataClassDictMixin):
    """WiFi band state from /wifi/band{2g,5g}/state."""

    enable: bool | None = None
    status: str | None = None


@dataclass
class WpsConfig(DataClassDictMixin):
    """WPS configuration from /wifi/band{2g,5g}/wps/config."""

    enable: bool | None = None


@dataclass
class WpsPairingJobs(DataClassDictMixin):
    """WPS pairing jobs from /wifi/band{2g,5g}/wps/pairing/jobs."""

    pairingJobs: list[dict] | None = None


@dataclass
class MtaLine(DataClassDictMixin):
    """MTA line info."""

    enable: bool | None = None
    operational: bool | None = None


@dataclass
class MtaLineEntry(DataClassDictMixin):
    """MTA line entry from /mta/lines."""

    id: int | None = None
    line: MtaLine | None = None


@dataclass
class UiScreenEntry(DataClassDictMixin):
    """A single UI screen toggle."""

    display: bool | None = None
    editable: bool | None = None
    disable: bool | None = None


@dataclass
class UiScreens(DataClassDictMixin):
    """UI screen configuration."""

    screens: dict[str, UiScreenEntry] | None = None
