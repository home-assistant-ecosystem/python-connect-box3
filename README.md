# connect-box3

Python API Client to interact with a Connect Box 3 modem/router. 

***For older hardware revisions (e. g., UPC Connect Box 2), please use [connect-box](https://github.com/home-assistant-ecosystem/python-connect-box)***

The device could be provided under different names by various ISP in Europe.

Currently tested with:

| Provider | Name | Model |
|----------|------|-------|
| Sunrise | Connect Box 3 | F5685LGB |

This module is not official, developed, supported or endorsed by Sunrise, UPC, Unitymedia or Compal.

## Installation

`connect-box3` is available on [PyPI](https://pypi.org/project/connect-box3/).

```bash
pip3 install connect-box3
```

For NixOS, the package is available in the [nixos.python3Packages.connect-box3](https://search.nixos.org/packages?channel=unstable&query=connect-box3) repository.

```bash
nix-env -iA nixos.python3Packages.connect-box3
```

## Usage

`connect-box` is a CLI application that show-cases the functionality of the module.

```bash
connect-box system --password xxx --host 192.168.1.1
              system               
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Field           ┃ Value         ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ modelName       │ F5685LGB      │
│ softwareVersion │ 4.11.1-2309.6 │
│ hardwareVersion │ 1.2.1b        │
└─────────────────┴───────────────┘
```

See also `example.py` for usage examples.

## License

Licensed under MIT. See LICENSE for details.
