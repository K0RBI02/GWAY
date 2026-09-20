# GWAY

Eigene, ruhige Web-Oberfläche für den **TP-Link Archer NX500** (5G-Router). Das Add-on meldet sich am Router an, fragt ihn im Hintergrund ab und zeigt alles unter `http://<home-assistant-ip>:8480`.

## Konfiguration

| Option | Bedeutung |
|---|---|
| `router_host` | Adresse der Router-Weboberfläche, **mit** `https://` (z. B. `https://192.168.0.1`) |
| `router_password` | Admin-Passwort der Router-Weboberfläche |
| `poll_seconds` | Abfrage-Intervall, 4 bis 60 Sekunden (Standard 8) |

Den Port (Standard 8480) kannst du unter *Netzwerk* ändern.

## Funktionen

- Live-Traffic (Download/Upload) mit Verlauf, Hover-Anzeige und Durchschnitt seit Start des Add-ons
- Übersicht: verbundene Geräte, CPU, Arbeitsspeicher, 5G-Empfang (RSRP/SNR)
- Geräteliste und feste IP-Adressen (DHCP-Reservierungen)
- WLAN 2,4 GHz und 5 GHz ein-/ausschalten, Router neu starten

## Wichtig zu wissen

- Der Router erlaubt nur **eine** Admin-Session gleichzeitig. Meldest du dich parallel in der TP-Link-Oberfläche an, wirft das eine die andere raus. Das Add-on meldet sich beim nächsten Abruf wieder an.
- Die Oberfläche hat **keinen Login**. Jeder im Heimnetz kann WLAN abschalten oder den Router neu starten. Gib den Port niemals ins Internet frei.
- Der Router-Zugriff läuft über die inoffizielle Bibliothek `tplinkrouterc6u`. Getestet ist das Add-on nur mit dem Archer NX500.

## Fehlersuche

| Meldung | Bedeutung |
|---|---|
| Router nicht erreichbar | Router aus, falsche Adresse oder nicht im selben Netz |
| Anmeldung am Router fehlgeschlagen | Passwort prüfen |
| Router hat die Anfrage abgelehnt | Gerade ist jemand anderes als Admin angemeldet; kurz warten |
| Keine Verbindung zum Add-on | Läuft das Add-on? Stimmt der Port? |
