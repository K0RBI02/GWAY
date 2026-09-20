# GWAY

A simple web interface for the **TP-Link Archer NX500** 5G router, available at `http://<home-assistant-ip>:8480`.

## Configuration

| Option | Description |
|---|---|
| `router_host` | Router address including `https://` (e.g. `https://192.168.0.1`) |
| `router_password` | Router admin password |
| `poll_seconds` | Polling interval: 4–60 seconds (default: 8) |

The port can be changed under *Network*.

## Features

- Live download/upload traffic and history
- Connected devices, CPU, memory and 5G signal details
- Device list and DHCP reservations
- Toggle 2.4/5 GHz Wi-Fi (including guest Wi-Fi, if the router reports it) and restart the router
- Click an IP or MAC address to copy it

## Settings

Click the gear icon next to the model name:

- **Language:** German or English (default: browser language)
- **RSRP display:** show the value in dBm or a rating (good / fair / poor)
- **Show SNR (experimental):** shows the SNR value. The router reports it as a whole number (probably tenths of a dB), so GWAY divides it by 10. This is not confirmed yet.

Settings are stored in your browser, not in the add-on.

## Notes

- The router allows only one admin session at a time. The add-on reconnects automatically.
- The interface has no login. Anyone on your home network can control Wi-Fi or restart the router. Never expose the port to the internet.
- The container has a health check that queries the web interface, so Home Assistant can detect a hanging add-on.
- Tested only with the Archer NX500. Router access uses the unofficial `tplinkrouterc6u` library.

## Troubleshooting

- **Router unreachable:** Check the address, network connection and whether the router is online.
- **Login failed:** Check the password.
- **Request rejected:** Another admin session may be active; try again later.
- **Add-on unavailable:** Check that it is running and that the port is correct.
