import json
import logging
import os
import threading
import time
import urllib.request
import urllib.error

import paho.mqtt.client as mqtt


LOG = logging.getLogger("gway.mqtt")

SUPERVISOR_URL = "http://supervisor/services/mqtt"

DISCOVERY_PREFIX = "homeassistant"
BASE_TOPIC = "gway"
STATE_TOPIC = f"{BASE_TOPIC}/state"
AVAILABILITY_TOPIC = f"{BASE_TOPIC}/availability"

DEVICE = {
    "identifiers": ["gway"],
    "name": "GWAY",
    "manufacturer": "GWAY",
    "model": "TP-Link Archer NX500",
}


class MQTT:
    def __init__(self):
        self.client = None
        self.connected = False
        self.lock = threading.Lock()
        self.started = False

    # ------------------------------------------------------------------
    # Supervisor MQTT service
    # ------------------------------------------------------------------

    def _get_service(self):
        token = os.environ.get("SUPERVISOR_TOKEN")

        if not token:
            LOG.warning("SUPERVISOR_TOKEN not available")
            return None

        req = urllib.request.Request(
            SUPERVISOR_URL,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                payload = json.loads(
                    response.read().decode("utf-8")
                )

            if payload.get("result") != "ok":
                LOG.warning(
                    "Supervisor MQTT service unavailable: %s",
                    payload.get("message", payload),
                )
                return None

            service = payload.get("data")

            if not service:
                LOG.warning("Supervisor MQTT service returned no data")
                return None

            return service

        except Exception as exc:
            LOG.warning(
                "Could not get MQTT service from Supervisor: %s",
                exc,
            )
            return None

    # ------------------------------------------------------------------
    # MQTT callbacks
    # ------------------------------------------------------------------

    def _on_connect(self, client, userdata, flags, reason_code, properties=None):
        if reason_code == 0:
            self.connected = True
            LOG.info("MQTT connected")
            self._publish_availability("online")
            self._publish_discovery()
        else:
            self.connected = False
            LOG.error("MQTT connection failed: %s", reason_code)

    def _on_disconnect(self, client, userdata, disconnect_flags, reason_code, properties=None):
        self.connected = False

        if reason_code != 0:
            LOG.warning("MQTT disconnected: %s", reason_code)
        else:
            LOG.info("MQTT disconnected")

    def _on_publish(self, client, userdata, mid, reason_code=None, properties=None):
        pass

    # ------------------------------------------------------------------
    # Start / stop
    # ------------------------------------------------------------------

    def start(self):
        with self.lock:
            if self.started:
                return self.connected

            self.started = True

        service = self._get_service()

        if not service:
            LOG.warning("MQTT service unavailable - continuing without MQTT")
            return False

        try:
            host = service["host"]
            port = int(service.get("port", 1883))
            username = service.get("username")
            password = service.get("password")
            use_tls = bool(service.get("ssl", False))

            self.client = mqtt.Client(
                mqtt.CallbackAPIVersion.VERSION2,
                client_id="gway",
            )

            self.client.on_connect = self._on_connect
            self.client.on_disconnect = self._on_disconnect
            self.client.on_publish = self._on_publish

            if username:
                self.client.username_pw_set(username, password)

            if use_tls:
                self.client.tls_set()

            self.client.reconnect_delay_set(min_delay=2, max_delay=30)

            LOG.info(
                "Connecting to MQTT broker %s:%s%s",
                host,
                port,
                " (TLS)" if use_tls else "",
            )

            self.client.connect_async(host, port, keepalive=60)
            self.client.loop_start()

            return True

        except Exception as exc:
            LOG.exception("Could not start MQTT: %s", exc)
            self.client = None
            return False

    def stop(self):
        client = self.client

        if not client:
            return

        try:
            if self.connected:
                self._publish_availability("offline")

            client.disconnect()
            client.loop_stop()
        except Exception:
            LOG.exception("Error stopping MQTT")

        self.connected = False
        self.client = None
        self.started = False

    # ------------------------------------------------------------------
    # Publishing
    # ------------------------------------------------------------------

    def _publish(self, topic, payload, retain=False, qos=1):
        client = self.client

        if not client or not self.connected:
            return False

        try:
            result = client.publish(
                topic,
                payload,
                qos=qos,
                retain=retain,
            )

            return result.rc == mqtt.MQTT_ERR_SUCCESS

        except Exception as exc:
            LOG.warning("MQTT publish failed for %s: %s", topic, exc)
            return False

    def _publish_availability(self, state):
        self._publish(
            AVAILABILITY_TOPIC,
            state,
            retain=True,
            qos=1,
        )

    # ------------------------------------------------------------------
    # Home Assistant MQTT Discovery
    # ------------------------------------------------------------------

    @staticmethod
    def _value_template(path):
        expression = "value_json"

        for part in path.split("."):
            expression += f"['{part}']"

        return "{{ " + expression + " }}"

    def _sensor(
        self,
        object_id,
        name,
        value_path,
        *,
        unit=None,
        device_class=None,
        state_class=None,
        icon=None,
        precision=None,
    ):
        config = {
            "unique_id": f"gway_{object_id}",
            "object_id": f"gway_{object_id}",
            "name": name,
            "state_topic": STATE_TOPIC,
            "availability_topic": AVAILABILITY_TOPIC,
            "payload_available": "online",
            "payload_not_available": "offline",
            "value_template": self._value_template(value_path),
            "device": DEVICE,
        }

        if unit is not None:
            config["unit_of_measurement"] = unit

        if device_class is not None:
            config["device_class"] = device_class

        if state_class is not None:
            config["state_class"] = state_class

        if icon is not None:
            config["icon"] = icon

        if precision is not None:
            config["suggested_display_precision"] = precision

        topic = f"{DISCOVERY_PREFIX}/sensor/gway/{object_id}/config"

        self._publish(
            topic,
            json.dumps(config, separators=(",", ":")),
            retain=True,
            qos=1,
        )

    def _publish_discovery(self):
        LOG.info("Publishing Home Assistant MQTT discovery")

        self._sensor(
            "clients",
            "Clients",
            "overview.clients_total",
            icon="mdi:devices",
        )

        self._sensor(
            "wired_clients",
            "Wired Clients",
            "overview.wired",
            icon="mdi:ethernet",
        )

        self._sensor(
            "wifi_clients",
            "Wi-Fi Clients",
            "overview.wifi",
            icon="mdi:wifi",
        )

        self._sensor(
            "guest_clients",
            "Guest Clients",
            "overview.guest",
            icon="mdi:wifi-lock",
        )

        self._sensor(
            "cpu",
            "CPU Usage",
            "overview.cpu",
            unit="%",
            icon="mdi:cpu-64-bit",
            precision=1,
        )

        self._sensor(
            "memory",
            "Memory Usage",
            "overview.mem",
            unit="%",
            icon="mdi:memory",
            precision=1,
        )

        self._sensor(
            "wan_ip",
            "WAN IP",
            "overview.wan_ip",
            icon="mdi:ip-network",
        )

        self._sensor(
            "network",
            "Network",
            "lte.network",
            icon="mdi:signal-5g",
        )

        self._sensor(
            "isp",
            "ISP",
            "lte.isp",
            icon="mdi:office-building-network",
        )

        self._sensor(
            "rsrp",
            "RSRP",
            "lte.rsrp",
            unit="dBm",
            device_class="signal_strength",
            icon="mdi:signal-cellular-3-bar",
        )

        self._sensor(
            "snr",
            "SNR",
            "lte.snr",
            unit="dB",
            icon="mdi:signal",
            precision=1,
        )

        # server.py exposes these values in bytes/s.
        # HA will therefore receive the same raw values.
        self._sensor(
            "download",
            "Download",
            "lte.rx",
            unit="B/s",
            state_class="measurement",
            icon="mdi:download",
        )

        self._sensor(
            "upload",
            "Upload",
            "lte.tx",
            unit="B/s",
            state_class="measurement",
            icon="mdi:upload",
        )

        self._sensor(
            "average_download",
            "Average Download",
            "avg.rx",
            unit="B/s",
            state_class="measurement",
            icon="mdi:download-network",
            precision=0,
        )

        self._sensor(
            "average_upload",
            "Average Upload",
            "avg.tx",
            unit="B/s",
            state_class="measurement",
            icon="mdi:upload-network",
            precision=0,
        )

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------

    @staticmethod
    def _percent(value):
        """The router reports CPU/memory as a fraction (0.22 = 22 %).
        Same rule as the web UI: values up to 1 are fractions."""
        if value is None:
            return None

        try:
            value = float(value)
        except (TypeError, ValueError):
            return None

        return round(value * 100 if value <= 1 else value, 1)

    @staticmethod
    def _prepare(state):
        """Copy of the state with values converted for Home Assistant.
        The original state (used by the web UI) is never modified."""
        out = dict(state)

        overview = state.get("overview")

        if isinstance(overview, dict):
            overview = dict(overview)
            overview["cpu"] = MQTT._percent(overview.get("cpu"))
            overview["mem"] = MQTT._percent(overview.get("mem"))
            out["overview"] = overview

        lte = state.get("lte")

        if isinstance(lte, dict):
            lte = dict(lte)

            # Raw SNR is tenths of a dB (same assumption as the web UI).
            try:
                if lte.get("snr") is not None:
                    lte["snr"] = round(float(lte["snr"]) / 10, 1)
            except (TypeError, ValueError):
                lte["snr"] = None

            out["lte"] = lte

        avg = state.get("avg")

        if isinstance(avg, dict):
            avg = dict(avg)

            for key in ("rx", "tx"):
                if avg.get(key) is not None:
                    avg[key] = round(avg[key])

            out["avg"] = avg

        return out

    def publish_state(self, state):
        if not state:
            return

        payload = json.dumps(
            self._prepare(state),
            separators=(",", ":"),
            ensure_ascii=False,
        )

        self._publish(
            STATE_TOPIC,
            payload,
            retain=True,
            qos=1,
        )

    def publish_offline(self):
        self._publish_availability("offline")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    mqtt_bridge = MQTT()

    if mqtt_bridge.start():
        LOG.info("MQTT test running for 10 seconds")
        time.sleep(10)
        mqtt_bridge.stop()
    else:
        LOG.error("MQTT test could not connect")
