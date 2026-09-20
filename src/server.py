#!/usr/bin/env python3
"""
GWAY - Backend
Keeps ONE session to the TP-Link Archer NX500 (only one admin session allowed),
polls in the background, and provides the current state as JSON.
Actions (Wi-Fi band, reboot) use the same session.
"""

import json
import os
from importlib.metadata import version as pkg_version
import signal
import threading
import time
from collections import deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import requests
import urllib3
from tplinkrouterc6u import Connection, TPLinkEXClient
from tplinkrouterc6u.common.exception import AuthorizeError, ClientException

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PORT = 8480  # Container port; the host port is defined in config.yaml
STATIC = Path(__file__).parent / "static"
ICON = Path(__file__).parent / "icon.png"
BANDS = {"2g": Connection.HOST_2G, "5g": Connection.HOST_5G, "guest2g": Connection.GUEST_2G, "guest5g": Connection.GUEST_5G}
DHCP_EVERY = 60  # Seconds between DHCP queries


def load_options():
    p = Path("/data/options.json")
    if p.exists():
        return json.loads(p.read_text())
    return {
        "router_host": os.environ.get("ROUTER_HOST", ""),
        "router_password": os.environ.get("ROUTER_PASSWORD", ""),
        "poll_seconds": int(os.environ.get("POLL_SECONDS", "8")),
    }


def classify(e):
    """General error category for the UI: unreachable, auth, session, or other."""
    if isinstance(e, AuthorizeError):
        return "auth"
    if isinstance(e, (requests.exceptions.ConnectionError, requests.exceptions.Timeout, OSError)):
        return "unreachable"
    if isinstance(e, ClientException):
        return "session"
    return "other"


def enum_val(x):
    return str(getattr(x, "value", x))


class Poller(threading.Thread):
    def __init__(self, opts):
        super().__init__(daemon=True)
        self.opts = opts
        self.client = None
        self.firmware = None
        self.stop_event = threading.Event()
        self.lock = threading.Lock()  # Protects self.state
        self.io = threading.RLock()  # Serializes all router access
        self.history = deque(maxlen=90)
        # Running totals since add-on startup (constant memory usage regardless of runtime)
        self.sums = {"rx": 0.0, "tx": 0.0}
        self.counts = {"rx": 0, "tx": 0}
        self.started = None
        self.dhcp = []
        self.dhcp_at = 0
        self.paused_until = 0
        self.state = {"ok": False, "error": "Noch keine Daten", "kind": "starting", "updated": None}

    def connect(self):
        c = TPLinkEXClient(self.opts["router_host"], self.opts["router_password"], verify_ssl=False)
        c.authorize()
        self.client = c
        fw = c.get_firmware()
        self.firmware = {"model": fw.model, "hardware": fw.hardware_version, "firmware": fw.firmware_version}

    def drop(self):
        if self.client:
            try:
                self.client.logout()
            except Exception:
                pass
        self.client = None

    def load_dhcp(self):
        try:
            self.dhcp = [
                {"name": r.hostname or "", "ip": str(r.ipaddr), "mac": str(r.macaddr), "enabled": bool(r.enabled)}
                for r in self.client.get_ipv4_reservations()
            ]
            self.dhcp_at = time.time()
        except Exception:
            pass  # Keep the previous list

    def poll(self):
        with self.io:
            if self.client is None:
                self.connect()
            st = self.client.get_status()
            lte = self.client.get_lte_status()
            if time.time() - self.dhcp_at > DHCP_EVERY:
                self.load_dhcp()

        now = int(time.time())
        self.history.append((now, lte.cur_rx_speed, lte.cur_tx_speed))
        if self.started is None:
            self.started = now
        for key, val in (("rx", lte.cur_rx_speed), ("tx", lte.cur_tx_speed)):
            if val is not None:  # Do not count missing values as zero
                self.sums[key] += val
                self.counts[key] += 1
        snap = {
            "ok": True,
            "error": None,
            "kind": None,
            "updated": int(time.time()),
            "firmware": self.firmware,
            "overview": {
                "clients_total": st.clients_total,
                "wired": st.wired_total,
                "wifi": st.wifi_clients_total,
                "guest": st.guest_clients_total,
                "cpu": st.cpu_usage,
                "mem": st.mem_usage,
                "wan_ip": str(st.wan_ipv4_addr),
                "wifi_2g": st.wifi_2g_enable,
                "wifi_5g": st.wifi_5g_enable,
                "guest_wifi_2g": st.guest_2g_enable,
                "guest_wifi_5g": st.guest_5g_enable,
            },
            "lte": {
                "network": lte.network_type_info,
                "isp": lte.isp_name,
                "rsrp": lte.rsrp,
                "snr": lte.snr,
                "rx": lte.cur_rx_speed,
                "tx": lte.cur_tx_speed,
            },
            "devices": [
                {"name": d.hostname or "", "ip": str(d.ipaddr), "mac": str(d.macaddr), "type": enum_val(d.type)}
                for d in st.devices
            ],
            "reservations": self.dhcp,
            "avg": {
                "rx": self.sums["rx"] / self.counts["rx"] if self.counts["rx"] else None,
                "tx": self.sums["tx"] / self.counts["tx"] if self.counts["tx"] else None,
                "since": self.started,
            },
        }
        with self.lock:
            self.state = snap

    def act(self, body):
        action = body.get("action")
        with self.io:
            if action == "wifi":
                band = BANDS.get(body.get("band"))
                if band is None:
                    raise ValueError("Unknown Wi-Fi band")
                if self.client is None:
                    self.connect()
                self.client.set_wifi(band, bool(body.get("enable")))
                self.poll()
            elif action == "reboot":
                if self.client is None:
                    self.connect()
                self.client.reboot()
                self.drop()
                self.paused_until = time.time() + 120
                with self.lock:
                    self.state = {**self.state, "ok": False, "kind": "reboot", "error": "Router is restarting, this takes about 2 minutes"}
            else:
                raise ValueError("Unknown action")

    def run(self):
        interval = max(4, int(self.opts.get("poll_seconds", 8)))
        while not self.stop_event.is_set():
            if time.time() >= self.paused_until:
                try:
                    self.poll()
                except Exception as e:
                    with self.io:
                        self.drop()
                    with self.lock:
                        self.state = {**self.state, "ok": False, "kind": classify(e), "error": f"{type(e).__name__}: {e}"}
            self.stop_event.wait(interval)

    def snapshot(self):
        with self.lock:
            return {**self.state, "history": list(self.history)}


poller = None


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json", cache="no-store"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", cache)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/api/state":
            self._send(200, json.dumps(poller.snapshot()).encode())
        elif path in ("/", "/index.html"):
            self._send(200, (STATIC / "index.html").read_bytes(), "text/html; charset=utf-8")
        elif path in ("/icon.png", "/favicon.ico") and ICON.exists():
            self._send(200, ICON.read_bytes(), "image/png", "max-age=86400")
        else:
            self._send(404, b"Not found", "text/plain; charset=utf-8")

    def do_POST(self):
        # This header forces a CORS preflight; external websites cannot trigger actions.
        if self.path != "/api/action" or self.headers.get("X-Requested-With") != "router-ui":
            return self._send(403, b'{"error":"Not allowed"}')
        try:
            n = int(self.headers.get("Content-Length") or 0)
            poller.act(json.loads(self.rfile.read(n) or b"{}"))
            self._send(200, b'{"ok":true}')
        except Exception as e:
            self._send(500, json.dumps({"error": f"{type(e).__name__}: {e}"}).encode())

    def log_message(self, *args):
        pass



def main():
    global poller
    opts = load_options()
    if not opts.get("router_host") or not opts.get("router_password"):
        print("ERROR: set router_host and router_password in the add-on configuration.", flush=True)
    poller = Poller(opts)
    poller.start()

    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)

    def stop(*_):
        threading.Thread(target=server.shutdown).start()

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)

    try:
        print(f"tplinkrouterc6u {pkg_version('tplinkrouterc6u')}", flush=True)
    except Exception:
        pass
    print(f"GWAY is running on port {PORT}", flush=True)
    try:
        server.serve_forever()
    finally:
        poller.stop_event.set()
        poller.join(5)
        with poller.io:
            poller.drop()  # Log out cleanly; otherwise a ghost session remains


if __name__ == "__main__":
    main()
