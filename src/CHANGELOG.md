# Changelog

## 0.3.0
- Projekt heißt jetzt GWAY (Ordnerstruktur: Add-on liegt in src/)
- Als Add-on-Repository verfügbar: Installation per Repository-URL, Updates direkt im Add-on-Store
- Icon, Logo und deutsche/englische Übersetzung der Konfigurationsfelder
- Neutrale Standard-Router-Adresse in der Konfiguration

## 0.2.9
- Durchschnitt unter dem Graphen ohne Zeitangabe ("Ø ↓ 2,63 · ↑ 0,22 Mbit/s"), berechnet wird er weiterhin über die gesamte Laufzeit seit dem Start des Add-ons

## 0.2.8
- Durchschnitt unter dem Graphen gilt jetzt für die gesamte Laufzeit seit dem Start des Add-ons (bis zum nächsten Neustart), mit Angabe der Dauer, z. B. "Ø seit 3 Std. 12 Min."
- Messungen ohne Wert zählen nicht mehr als 0 und ziehen den Durchschnitt nicht mehr herunter

## 0.2.7
- Graph: Hover-Bubble neben dem Mauszeiger zeigt Uhrzeit sowie Download und Upload am gehoverten Punkt (am Handy per Tippen oder Wischen)
- Unter dem Graphen: Zeitraum links, Durchschnitt für Download und Upload rechts, der Erklärsatz ist weg
- Verständliche Fehlertexte statt technischer Meldungen (Router nicht erreichbar, Anmeldung fehlgeschlagen, Admin-Session belegt, Add-on nicht erreichbar)

## 0.2.6
- Eingeklappte Leiste: Pfeile (↓ ↑) statt "Download/Upload"-Text, dazu einmal die Einheit Mbit/s
- Zahlen haben eine feste Mindestbreite, der Graph wackelt nicht mehr, wenn sich die Stellenzahl ändert
- Changelog hinzugefügt

## 0.2.5
- Graph in der Leiste füllt den ganzen Platz zwischen den Werten und dem rechten Rand
- Tabellen: nur die Namensspalte scrollt bei langen Namen, nicht mehr die ganze Tabelle
- Handy (unter 560 px): MAC-Spalte ausgeblendet, damit die Namen Platz haben

## 0.2.4
- Traffic-Karte schrumpft beim Scrollen fließend zur Leiste (Zahlen wandern nach links, Graph nach rechts)
- Über der Modell-Zeile ragt beim Scrollen nichts mehr hinaus
- Handy: Seite war breiter als der Bildschirm, behoben

## 0.2.3
- Übergang zur kompakten Leiste mit Ein- und Ausblenden (Vorstufe, in 0.2.4 ersetzt)

## 0.2.2
- Kompakte Traffic-Leiste beim Scrollen (erste Version)

## 0.2.1
- Namen bei den festen IP-Adressen werden aus der Geräteliste ergänzt, sonst "(gerade offline)"

## 0.2.0
- Verbindungstyp und "Online seit" entfernt, RSRP und SNR statt Signalstufe, Firmware gekürzt
- Neu: feste IP-Adressen (DHCP-Reservierungen), WLAN-Bänder an/aus, Router neu starten

## 0.1.0
- Erster Stand: Live-Traffic, Übersicht und Geräteliste
