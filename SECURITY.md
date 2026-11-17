# Security

## Intended use

GWAY is meant for a trusted home network. The web interface on port 8480 has **no login**: anyone who can reach it can switch Wi-Fi off, add or delete port forwarding rules and reboot the router.

- Never expose port 8480 to the internet (no port forwarding, no public reverse proxy).
- If you need remote access, use a VPN into your home network.
- The router password is stored in the add-on configuration by Home Assistant and is never sent to the browser.

## Reporting a vulnerability

Please do not open a public issue. Use GitHub's private vulnerability reporting instead:
**Security → Report a vulnerability** in this repository.

Fixes are released as a new patch version and noted in the [changelog](src/CHANGELOG.md).
