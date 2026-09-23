# GWAY

A simple web interface for the **TP-Link Archer NX500** 5G router, available at `http://<home-assistant-ip>:8480`.

## Configuration

| Option | Description |
|---|---|
| `router_host` | Router address including `https://` (e.g. `https://192.168.0.1`) |
| `router_password` | Router admin password |
| `poll_seconds` | Polling interval: 4–60 seconds (default: 8) |
| `data_limit_gb` | Monthly mobile data limit in GB for the data usage tile (default: 0 = no limit) |
| `data_reset_day` | Day of the month on which the data counter starts again, 1–28 (default: 1) |

The port can be changed under *Network*.

## Features

- Live download/upload traffic and history
- Connected devices, CPU, memory and 5G signal details
- Data usage of the current period, optionally with a limit and progress bar
- Device list and DHCP reservations
- Toggle Wi-Fi and guest Wi-Fi (if the router reports it) and restart the router
- Click an IP or MAC address to copy it
- Optional MQTT sensors for Home Assistant (automatic discovery)

## Data usage

The tile next to devices, CPU and memory shows the data used in the current period. If you set `data_limit_gb`, it also shows the limit and a bar (the bar turns red from 90 %).

- The volume comes from the router's own counter (`total_statistics`). GWAY assumes it is in bytes (experimental). If the router does not report it, GWAY counts from the current speeds instead, which is less exact.
- The counter starts again on `data_reset_day`. The first period starts when the add-on first sees the counter, so it only covers the time since then.
- Hover over the tile to see when the current period started. `/api/state` shows the raw router value (`lte.total`) and the source used (`data.source`: `router` or `speed`).

## Settings

Click the gear icon next to the model name:

- **Language:** German or English (default: browser language)
- **RSRP display:** show the value in dBm or a rating (good / fair / poor)
- **Wi-Fi:** *Simple* shows one switch for Wi-Fi and one for guest Wi-Fi (both bands together, "partial" if only one band is on). *Band* shows separate 2.4 GHz and 5 GHz switches.
- **Show SNR (experimental):** shows the SNR value. The router reports it as a whole number (probably tenths of a dB), so GWAY divides it by 10. This is not confirmed yet.

Settings are stored in your browser, not in the add-on.

## Storage

The data usage counter and the traffic average are stored in the add-on's `/data` folder, so they survive restarts and updates. The average covers the time since the first start. To start over, uninstall the add-on or delete its data.

## MQTT

If an MQTT broker is available in Home Assistant (for example the Mosquitto add-on), GWAY publishes its values through MQTT discovery: clients, CPU, memory, WAN IP, network, ISP, RSRP, SNR, download, upload, averages and data used. MQTT is optional. Without a broker the web interface works as usual.

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
