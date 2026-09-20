# GWAY

A lightweight, private web UI for the TP-Link Archer NX500 (5G router) as a Home Assistant add-on.

![Screenshot](docs/screenshot.png)

## Features

- Live traffic with history, hover details, and averages
- Overview of connected devices, CPU, memory, and 5G signal
- Device list and static IP assignments
- Toggle Wi-Fi bands and reboot the router
- Light and dark mode, including mobile support

## Installation

1. In Home Assistant: Settings → Add-ons → Add-on Store → ⋮ → Repositories
2. Add `https://github.com/K0RBI02/GWAY`
   (or click: [Add repository](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FK0RBI02%2FGWAY))
3. Install GWAY, enter the router address and password in the configuration, then start it.
4. Open `http://<home-assistant-ip>:8480`.

See [src/DOCS.md](src/DOCS.md) for details and the [Changelog](src/CHANGELOG.md) for changes.

## Security

This interface has no login. It is intended for local home use only; do not expose the port to the internet.

## Notes

- Unofficial and not affiliated with TP-Link. Router access uses [`tplinkrouterc6u`](https://github.com/AlexandrErohin/TP-Link-Archer-C6U).
- Tested only with the Archer NX500. Other models may require a different client class.
- The router allows only one admin session at a time.
