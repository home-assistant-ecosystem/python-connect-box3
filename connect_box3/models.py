"""Data models for Connect Box 3."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from mashumaro.mixins.dict import DataClassDictMixin


@dataclass
class SystemInfo(DataClassDictMixin):
    """System information from /system/info."""

    modelName: Optional[str] = None
    softwareVersion: Optional[str] = None
    hardwareVersion: Optional[str] = None


@dataclass
class Localization(DataClassDictMixin):
    """Localization from /system/localization."""

    modelName: Optional[str] = None
    productName: Optional[str] = None
    skin: Optional[str] = None


@dataclass
class ModemMode(DataClassDictMixin):
    """Modem mode from /system/modemmode."""

    enable: Optional[bool] = None


@dataclass
class FirstInstall(DataClassDictMixin):
    """First install status from /system/firstinstall."""

    complete: Optional[bool] = None


@dataclass
class Languages(DataClassDictMixin):
    """Available languages from /system/languages."""

    languages: Optional[List[str]] = None


@dataclass
class SoftwareUpdate(DataClassDictMixin):
    """Software update status from /system/softwareupdate."""

    status: Optional[str] = None


@dataclass
class LoginDetails(DataClassDictMixin):
    """Login details from GET /user/login."""

    numberOfContiguousFailures: Optional[str] = None
    lockoutTime: Optional[str] = None


@dataclass
class UserLanguage(DataClassDictMixin):
    """User language from /user/3/language."""

    language: Optional[str] = None


@dataclass
class ProvisioningIpv4(DataClassDictMixin):
    """IPv4 provisioning details."""

    address: Optional[str] = None
    defaultGateway: Optional[str] = None
    dnsServers: Optional[List[str]] = None
    leaseTime: Optional[int] = None
    expireTime: Optional[int] = None


@dataclass
class ProvisioningDsLite(DataClassDictMixin):
    """DS-Lite provisioning details."""

    enable: Optional[bool] = None


@dataclass
class Provisioning(DataClassDictMixin):
    """Gateway provisioning from /system/gateway/provisioning."""

    mode: Optional[str] = None
    macAddress: Optional[str] = None
    ipv4: Optional[ProvisioningIpv4] = None
    dsLite: Optional[ProvisioningDsLite] = None


@dataclass
class PonInterface(DataClassDictMixin):
    """PON interface data from /pon/status."""

    transceiverTemp: Optional[float] = None
    transceiverVoltage: Optional[str] = None
    laserBiasCurrent: Optional[str] = None
    transmitOpticalLevel: Optional[str] = None
    opticalSignalLevel: Optional[str] = None


@dataclass
class PonStatusInfo(DataClassDictMixin):
    """PON status info."""

    status: Optional[str] = None
    connectionMode: Optional[str] = None
    ipv4Firewall: Optional[bool] = None
    ipData: Optional[str] = None
    ipVoip: Optional[str] = None


@dataclass
class PonStatus(DataClassDictMixin):
    """PON status from /pon/status."""

    interface: Optional[PonInterface] = None
    status: Optional[PonStatusInfo] = None


@dataclass
class PonState(DataClassDictMixin):
    """PON state from /pon/state."""

    status: Optional[str] = None
    standardCompliance: Optional[str] = None
    serialNumber: Optional[str] = None
    upTime: Optional[int] = None
    accessAllowed: Optional[bool] = None


@dataclass
class LedLight(DataClassDictMixin):
    """LED light status from /network/ledlight."""

    value: Optional[int] = None


@dataclass
class LanStatus(DataClassDictMixin):
    """LAN status from /network/ipv4/info."""

    lanIpAddress: Optional[str] = None
    lanSubnet: Optional[str] = None
    lanSubnetMask: Optional[str] = None


@dataclass
class DhcpAllowedIp(DataClassDictMixin):
    """Allowed IP entry in DHCP config."""

    lanAllowedSubnetIp: Optional[str] = None
    lanAllowedSubnetMask: Optional[str] = None


@dataclass
class DhcpBlockedIp(DataClassDictMixin):
    """Blocked IP entry in DHCP config."""

    lanBlockedSubnetIp: Optional[str] = None
    lanBlockedSubnetMask: Optional[str] = None


@dataclass
class DhcpConfig(DataClassDictMixin):
    """DHCP configuration from /network/ipv4/dhcp."""

    enable: Optional[bool] = None
    minAddress: Optional[str] = None
    maxAddress: Optional[str] = None
    subnetMask: Optional[str] = None
    leaseTime: Optional[int] = None
    maxIps: Optional[int] = None
    allowedIps: Optional[List[DhcpAllowedIp]] = None
    blockedIps: Optional[List[DhcpBlockedIp]] = None


@dataclass
class Dmz(DataClassDictMixin):
    """DMZ configuration from /network/ipv4/dmz."""

    enable: Optional[bool] = None
    internalIp: Optional[str] = None


@dataclass
class Firewall(DataClassDictMixin):
    """Firewall settings from /network/ipv4/firewall or /network/ipv6/firewall."""

    enable: Optional[bool] = None
    blockFragmentedIpPackets: Optional[bool] = None
    portScanProtect: Optional[bool] = None
    ipFloodDetect: Optional[bool] = None


@dataclass
class Upnp(DataClassDictMixin):
    """UPnP configuration from /network/upnp."""

    enable: Optional[bool] = None


@dataclass
class HostIpv4(DataClassDictMixin):
    """IPv4 info for a connected host."""

    address: Optional[str] = None
    leaseTimeRemaining: Optional[int] = None


@dataclass
class HostWifi(DataClassDictMixin):
    """WiFi info for a connected host."""

    band: Optional[str] = None
    rssi: Optional[int] = None
    ssid: Optional[str] = None


@dataclass
class HostEthernet(DataClassDictMixin):
    """Ethernet info for a connected host."""

    port: Optional[int] = None


@dataclass
class HostConfig(DataClassDictMixin):
    """Configuration of a connected host."""

    connected: Optional[bool] = None
    deviceName: Optional[str] = None
    deviceType: Optional[str] = None
    hostname: Optional[str] = None
    interface: Optional[str] = None
    speed: Optional[float] = None
    ipv4: Optional[HostIpv4] = None
    wifi: Optional[HostWifi] = None
    ethernet: Optional[HostEthernet] = None


@dataclass
class Host(DataClassDictMixin):
    """A connected host from /network/hosts."""

    macAddress: Optional[str] = None
    config: Optional[HostConfig] = None


@dataclass
class WifiSsid(DataClassDictMixin):
    """WiFi SSID configuration."""

    ssid: Optional[str] = None
    broadcastSsid: Optional[bool] = None
    securityType: Optional[str] = None
    passphrase: Optional[str] = None
    rekeyInterval: Optional[int] = None
    encryptionType: Optional[str] = None


@dataclass
class WifiRadio(DataClassDictMixin):
    """WiFi radio configuration."""

    channelMode: Optional[bool] = None
    channel: Optional[int] = None
    bandwidth: Optional[str] = None


@dataclass
class WifiConfig(DataClassDictMixin):
    """WiFi band configuration from /wifi/band{2g,5g}/config."""

    enable: Optional[bool] = None
    ssid: Optional[WifiSsid] = None
    radio: Optional[WifiRadio] = None


@dataclass
class WifiState(DataClassDictMixin):
    """WiFi band state from /wifi/band{2g,5g}/state."""

    enable: Optional[bool] = None
    status: Optional[str] = None


@dataclass
class WpsConfig(DataClassDictMixin):
    """WPS configuration from /wifi/band{2g,5g}/wps/config."""

    enable: Optional[bool] = None


@dataclass
class WpsPairingJobs(DataClassDictMixin):
    """WPS pairing jobs from /wifi/band{2g,5g}/wps/pairing/jobs."""

    pairingJobs: Optional[List[dict]] = None


@dataclass
class MtaLine(DataClassDictMixin):
    """MTA line info."""

    enable: Optional[bool] = None
    operational: Optional[bool] = None


@dataclass
class MtaLineEntry(DataClassDictMixin):
    """MTA line entry from /mta/lines."""

    id: Optional[int] = None
    line: Optional[MtaLine] = None


@dataclass
class UiScreenEntry(DataClassDictMixin):
    """A single UI screen toggle."""

    display: Optional[bool] = None
    editable: Optional[bool] = None
    disable: Optional[bool] = None


@dataclass
class UiScreens(DataClassDictMixin):
    """UI screen configuration."""

    screens: Optional[Dict[str, UiScreenEntry]] = None
