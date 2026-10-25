"""CLI tool for Connect Box 3."""

import asyncio
import json
from dataclasses import asdict, fields
from getpass import getpass
from typing import Optional

from cyclopts import App
from rich.console import Console
from rich.table import Table

from connect_box3 import ConnectBox
from connect_box3.exceptions import ConnectBoxError

app = App(name="connect-box", help="CLI tool for Connect Box 3 devices.")
console = Console()


def _prompt(host: str | None, password: str | None) -> tuple[str, str]:
    """Prompt for host and password if not provided."""
    if not host:
        host = input("Host [192.168.0.1]: ").strip() or "192.168.0.1"
    if not password:
        password = getpass("Password: ")
    return host, password


def _run(coro):
    """Run an async coroutine synchronously."""
    return asyncio.run(coro)


async def _call(host: str, password: str, method: str, **kwargs):
    """Login, call a method on the client and logout."""
    host, password = _prompt(host, password)
    async with ConnectBox(password, host=host) as client:
        await client.login(password)
        result = await getattr(client, method)(**kwargs)
        await client.logout()
        return result


def _format_value(value):
    """Format a value for display in a table cell."""
    if value is None:
        return "[dim]—[/dim]"
    if isinstance(value, bool):
        return "[green]✓[/green]" if value else "[red]✗[/red]"
    if isinstance(value, dict):
        return _make_subtable("", value)
    if isinstance(value, list):
        if value and isinstance(value[0], dict):
            return _make_list_subtable(value)
        return json.dumps(value)
    return str(value)


def _make_subtable(title: str, data: dict) -> Table:
    """Create a nested key/value table (no outer border)."""
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column(style="bold")
    table.add_column()
    for key, value in data.items():
        table.add_row(key, _format_value(value))
    return table


def _make_list_subtable(items: list[dict]) -> Table:
    """Create a nested columnar table for a list of dicts."""
    columns = list(items[0].keys())
    table = Table(show_header=True, box=None, padding=(0, 1))
    for col in columns:
        table.add_column(col, style="bold" if col == columns[0] else "")
    for item in items:
        table.add_row(*(_format_value(item.get(c)) for c in columns))
    return table


def _print_table(title: str, data: dict):
    """Print a dict as a rich key/value table with nested sub-tables."""
    table = Table(title=title, show_header=True, title_style="bold cyan")
    table.add_column("Field", style="bold")
    table.add_column("Value")
    for key, value in data.items():
        table.add_row(key, _format_value(value))
    console.print(table)


def _print_list_table(title: str, items: list[dict]):
    """Print a list of dicts as a rich table with columns."""
    if not items:
        console.print(f"[dim]{title}: (empty)[/dim]")
        return
    columns = list(items[0].keys())
    table = Table(title=title, show_header=True, title_style="bold cyan")
    for col in columns:
        table.add_column(col, style="bold" if col == columns[0] else "")
    for item in items:
        table.add_row(*(_format_value(item.get(c)) for c in columns))
    console.print(table)


def _print(result, *, raw: bool = False, title: str = ""):
    """Pretty-print a dataclass, list of dataclasses, or dict."""
    if raw:
        if isinstance(result, list):
            print(json.dumps([asdict(item) for item in result], indent=2))
        elif isinstance(result, dict):
            print(json.dumps(result, indent=2))
        elif result is not None:
            print(json.dumps(asdict(result), indent=2))
        return

    if isinstance(result, list) and result:
        items = [asdict(item) for item in result]
        _print_list_table(title, items)
    elif isinstance(result, dict):
        _print_table(title, result)
    elif result is not None:
        _print_table(title, asdict(result))


# Commands: (cli_name, method_name, help_text)
COMMANDS = [
    ("dhcp", "get_dhcp", "Get IPv4 DHCP configuration."),
    ("dmz", "get_dmz", "Get DMZ configuration."),
    ("first-install", "get_first_install", "Get first install status."),
    ("ipv4-firewall", "get_ipv4_firewall", "Get IPv4 firewall settings."),
    ("ipv6-firewall", "get_ipv6_firewall", "Get IPv6 firewall settings."),
    ("languages", "get_languages", "Get available languages."),
    ("lanstatus", "get_lanstatus", "Get LAN status (IPv4 info)."),
    ("led", "get_led", "Get LED brightness."),
    ("localization", "get_localization", "Get system localization settings."),
    ("modem-mode", "get_modem_mode", "Get modem mode."),
    ("mta-lines", "get_mta_lines", "Get MTA lines information."),
    ("provisioning", "get_provisioning", "Get gateway provisioning information."),
    ("software-update", "get_software_update", "Get software update status."),
    ("state", "get_pon_state", "Get PON state."),
    ("status", "get_pon_status", "Get PON status."),
    ("system", "get_system_info", "Get system information."),
    ("ui-screens", "get_ui_screens", "Get UI screens configuration."),
    ("upnp", "get_upnp", "Get UPnP configuration."),
    ("user-language", "get_user_language", "Get user language preference."),
    ("wifi-2g-config", "get_wifi_band2g_config", "Get 2.4GHz WiFi band configuration."),
    ("wifi-2g-state", "get_wifi_band2g_state", "Get 2.4GHz WiFi band state."),
    ("wifi-5g-config", "get_wifi_band5g_config", "Get 5GHz WiFi band configuration."),
    ("wifi-5g-state", "get_wifi_band5g_state", "Get 5GHz WiFi band state."),
    (
        "wifi-2g-wps-config",
        "get_wifi_band2g_wps_config",
        "Get 2.4GHz WiFi WPS configuration.",
    ),
    (
        "wifi-5g-wps-config",
        "get_wifi_band5g_wps_config",
        "Get 5GHz WiFi WPS configuration.",
    ),
]

for _cli_name, _method, _help in COMMANDS:

    def _make_cmd(method=_method, help_text=_help, cli_name=_cli_name):
        """Factory to create CLI command functions."""

        def cmd(
            *, host: str | None = None, password: str | None = None, json: bool = False
        ):
            """Get data from the device."""
            _print(_run(_call(host, password, method)), raw=json, title=cli_name)

        cmd.__doc__ = help_text
        return cmd

    app.command(name=_cli_name)(_make_cmd())


@app.command
def login_status(*, host: str | None = None, json: bool = False):
    """Get current login status (no auth required)."""
    if not host:
        host = input("Host [192.168.0.1]: ").strip() or "192.168.0.1"

    async def _get(host):
        """Get login status without authentication."""
        async with ConnectBox("", host=host) as client:
            """Just call the method without logging in."""
            return await client.get_login_status()

    _print(_run(_get(host)), raw=json, title="login-status")


@app.command
def hosts(
    *,
    host: str | None = None,
    password: str | None = None,
    connected_only: bool = True,
    json: bool = False,
):
    """Get network hosts."""
    _print(
        _run(_call(host, password, "get_hosts", connected_only=connected_only)),
        raw=json,
        title="hosts",
    )


@app.command
def set_led(
    brightness: int,
    *,
    host: str | None = None,
    password: str | None = None,
    json: bool = False,
):
    """Set LED brightness."""
    _print(
        _run(_call(host, password, "set_led", brightness=brightness)),
        raw=json,
        title="led",
    )


@app.command
def reboot(*, host: str | None = None, password: str | None = None):
    """Reboot the device."""
    host, password = _prompt(host, password)

    async def _reboot(host, password):
        """Login, reboot and logout."""
        async with ConnectBox(password, host=host) as client:
            await client.login(password)
            await client.reboot_device()
            print("Reboot initiated.")

    _run(_reboot(host, password))


@app.command(name="all")
def all_data(
    *, host: str | None = None, password: str | None = None, json_output: bool = False
):
    """Get all data from the device."""
    host, password = _prompt(host, password)

    async def _all(host, password):
        """Get all data by calling all methods."""
        async with ConnectBox(password, host=host) as client:
            await client.login(password)
            results = {}
            for cli_name, method, _ in COMMANDS:
                try:
                    results[cli_name] = await getattr(client, method)()
                except Exception as e:
                    results[cli_name] = f"ERROR: {e}"
            try:
                results["hosts"] = await client.get_hosts()
            except Exception as e:
                results["hosts"] = f"ERROR: {e}"
            await client.logout()
            return results

    results = _run(_all(host, password))
    if json_output:
        combined = {}
        for name, result in results.items():
            if isinstance(result, str):
                combined[name] = result
            elif isinstance(result, list):
                combined[name] = [asdict(item) for item in result]
            else:
                combined[name] = asdict(result)
        print(json.dumps(combined, indent=2))
    else:
        for name, result in results.items():
            if isinstance(result, str):
                console.print(f"\n[bold red]{name}:[/bold red] {result}")
            elif isinstance(result, list):
                _print_list_table(name, [asdict(item) for item in result])
            else:
                _print_table(name, asdict(result))
            console.print()


def main():
    """Run the CLI app."""
    try:
        app()
    except ConnectBoxError as error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
