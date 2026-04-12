"""Get the data from an UPC Connect Box."""

import asyncio
from pprint import pprint

from connect_box3 import ConnectBox
from connect_box3.exceptions import ConnectBoxError

HOST = "192.168.1.1"
PASSWORD = "Netzgesichert123"


async def main():
    """Sample code to retrieve the data from an UPC Connect Box."""
    print("Endpoints that do not require authentication:")
    async with ConnectBox("", host=HOST) as no_auth_client:
        endpoints = [
            ("localization", no_auth_client.get_localization),
            ("ui/screens", no_auth_client.get_ui_screens),
            ("modemmode", no_auth_client.get_modem_mode),
            ("firstinstall", no_auth_client.get_first_install),
            ("languages", no_auth_client.get_languages),
            ("login status", no_auth_client.get_login_status),
        ]

        for name, fn in endpoints:
            print(f"-- Data from endpoint {no_auth_client.host}/{name}")
            try:
                print()
                pprint(await fn())
            except ConnectBoxError as error:
                print(f"Skipping ({error}) ...")

    print()
    print("Endpoints that require authentication:")
    async with ConnectBox(PASSWORD, host=HOST) as auth_client:
        print("-- login")
        pprint(await auth_client.login(PASSWORD))

        auth_endpoints = [
            ("system/info", auth_client.get_system_info),
            ("user language", auth_client.get_user_language),
            ("provisioning", auth_client.get_provisioning),
            ("softwareupdate", auth_client.get_software_update),
            ("network/hosts", auth_client.get_hosts),
            ("network/ipv4/dhcp", auth_client.get_dhcp),
            ("network/ipv4/info", auth_client.get_lanstatus),
            ("network/ipv4/dmz", auth_client.get_dmz),
            ("network/ipv4/firewall", auth_client.get_ipv4_firewall),
            ("network/ipv6/firewall", auth_client.get_ipv6_firewall),
            ("network/upnp", auth_client.get_upnp),
            ("led", auth_client.get_led),
            ("mta/lines", auth_client.get_mta_lines),
            ("wifi/band2g/state", auth_client.get_wifi_band2g_state),
            ("wifi/band5g/state", auth_client.get_wifi_band5g_state),
            ("wifi/band2g/config", auth_client.get_wifi_band2g_config),
            ("wifi/band5g/config", auth_client.get_wifi_band5g_config),
            ("wifi/band2g/wps/config", auth_client.get_wifi_band2g_wps_config),
            ("wifi/band5g/wps/config", auth_client.get_wifi_band5g_wps_config),
            ("wifi/band2g/wps/pairing/jobs", auth_client.get_wifi_band2g_wps_jobs),
            ("wifi/band5g/wps/pairing/jobs", auth_client.get_wifi_band5g_wps_jobs),
            ("pon/status", auth_client.get_pon_status),
            ("pon/state", auth_client.get_pon_state),
        ]

        for name, fn in auth_endpoints:
            print(f"-- Data from endpoint {auth_client.host}/{name}")
            try:
                print()
                pprint(await fn())
            except ConnectBoxError as error:
                print(f"Skipping ({error}) ...")

        print("-- logout")
        await auth_client.logout()

    print()
    print("Accessing stored class objects after fetching:")
    async with ConnectBox(PASSWORD, host=HOST) as client:
        await client.login(PASSWORD)

        # Fetch data — results are stored on the instance automatically
        await client.get_system_info()
        await client.get_lanstatus()
        await client.get_led()
        await client.get_pon_status()
        await client.get_pon_state()
        await client.get_hosts()

        # Access the stored objects directly without another API call
        print(f"Model: {client.system_info.modelName}")
        print(f"Firmware: {client.system_info.softwareVersion}")
        print(f"LAN IP: {client.lanstatus.lanIpAddress}")
        print(f"LED brightness: {client.led.value}")
        print(f"PON serial: {client.pon_state.serialNumber}")
        print(f"PON status: {client.pon_status.status.status}")
        print(f"Connected hosts: {len(client.hosts)}")

        for host in client.hosts:
            print(f" - {host.macAddress}")

        await client.logout()


if __name__ == "__main__":
    asyncio.run(main())
