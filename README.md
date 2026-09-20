# GWAY

Eigene, ruhige Web-Oberfläche für den **TP-Link Archer NX500** (5G-Router) als Home-Assistant-Add-on.

![Screenshot](docs/screenshot.png)

## Was es kann

- Live-Traffic mit Verlauf, Hover-Anzeige und Durchschnitt
- Übersicht mit verbundenen Geräten, CPU, Arbeitsspeicher und 5G-Empfang
- Geräteliste und feste IP-Adressen
- WLAN-Bänder ein- und ausschalten, Router neu starten
- Hell und dunkel, auch fürs Handy

## Installation

1. In Home Assistant: **Einstellungen → Add-ons → Add-on-Store → ⋮ → Repositories**
2. Diese URL hinzufügen: `https://github.com/K0RBI02/GWAY`
   (oder mit einem Klick: [Repository hinzufügen](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FK0RBI02%2FGWAY))
3. **GWAY** installieren, unter *Konfiguration* Router-Adresse und Passwort eintragen, starten.
4. Die Oberfläche läuft auf `http://<home-assistant-ip>:8480`.

Ausführliche Hinweise stehen in [src/DOCS.md](src/DOCS.md), Änderungen im [Changelog](src/CHANGELOG.md).

## Sicherheit

Die Oberfläche hat keinen Login. Sie ist nur für das Heimnetz gedacht, den Port niemals ins Internet freigeben.

## Hinweise

- Inoffiziell und nicht mit TP-Link verbunden. Der Router-Zugriff läuft über die Bibliothek [`tplinkrouterc6u`](https://github.com/AlexandrErohin/TP-Link-Archer-C6U).
- Getestet nur mit dem Archer NX500. Andere Modelle brauchen evtl. eine andere Client-Klasse der Bibliothek.
- Der Router lässt nur eine Admin-Session gleichzeitig zu.

## Entstehung

Entstanden in Zusammenarbeit mit Claude (Anthropic).
