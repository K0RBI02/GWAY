# Changelog

## 0.5.4
- Wi-Fi switches are more compact: by default there is one switch for Wi-Fi and one for guest Wi-Fi (both bands together; "partial" if only one band is on)
- New setting "Wi-Fi switches: Simple / Per band" shows the individual 2.4 and 5 GHz switches as compact chips

## 0.5.3
- Favicon: the add-on icon is now shown in the browser tab
- Click an IP or MAC address in the tables to copy it (also works over plain http)
- Guest Wi-Fi switches for 2.4 and 5 GHz (only shown if the router reports them)
- README screenshot updated (English, light, dark and mobile)

## 0.5.2
- Dark mode: darker background, teal green and wine red accents instead of the previous green and brown-orange
- Dark mode: better contrast for the grey text on the traffic card
- Dark mode: native elements (dialogs, scrollbars, search field) now follow the color scheme
- Mobile browsers get a matching theme color for the browser bar

## 0.5.1
- Mobile: content that scrolls under the collapsed traffic bar no longer shows up again in the gap above it

## 0.5.0
- Mobile: the Wi-Fi switches and the restart button moved into the settings panel on small screens, so the traffic card starts higher
- Graph: fixed scale (as on the desktop layout). A narrower graph, such as the collapsed bar on phones, shows fewer samples instead of squeezing everything; the maximum is 90 samples (about 12 minutes)
- Mobile: the three overview tiles fit in one row
- Touch: slightly larger, invisible hit areas for the gear icon and the settings toggles

## 0.4.2
- SNR (experimental) is now shown with one decimal place: the router reports it as a whole number (e.g. 105), which is treated as tenths of a dB (10.5 dB)

## 0.4.1
- Fixed the add-on linter findings: removed the default values `boot` and `startup` from `config.yaml`
- Replaced the obsolete `watchdog` option with a native Docker `HEALTHCHECK`

## 0.4.0
- Settings panel (gear icon next to the model name): language (German/English), RSRP as number or rating (good/fair/poor), optional experimental SNR display
- The interface is available in English and German; the default follows the browser language
- The `tplinkrouterc6u` library is now pinned in `requirements.txt` for reproducible builds
- Home Assistant watchdog: the add-on is restarted automatically if the web interface stops responding
- Dependabot now watches the Docker base image, the Python dependency and GitHub Actions
- Lint workflow: add-on linter, Python syntax check and Docker build on every push
- Remaining German texts in code and documentation translated to English

## 0.3.0
- Project is now called GWAY (directory structure: add-on is located in `src/`)
- Available as an add-on repository: installation via repository URL, updates directly in the add-on store
- Icon, logo, and German/English translations for the configuration fields
- Neutral default router address in the configuration

## 0.2.9
- Average below the graph without a time indication ("Ø ↓ 2.63 · ↑ 0.22 Mbit/s"); it is still calculated over the entire runtime since the add-on was started

## 0.2.8
- The average below the graph now applies to the entire runtime since the add-on was started (until the next restart), including the duration, e.g. "Ø since 3 hr 12 min"
- Measurements without a value no longer count as 0 and no longer reduce the average

## 0.2.7
- Graph: a hover bubble next to the cursor shows the time as well as download and upload at the hovered point (on mobile, by tapping or swiping)
- Below the graph: time period on the left, download and upload averages on the right; the explanatory sentence has been removed
- Clear error messages instead of technical messages (router unreachable, login failed, admin session occupied, add-on unreachable)

## 0.2.6
- Collapsed bar: arrows (↓ ↑) instead of the "Download/Upload" text, with the unit Mbit/s shown once
- Numbers have a fixed minimum width, so the graph no longer shifts when the number of digits changes
- Changelog added

## 0.2.5
- Graph in the bar fills all the space between the values and the right edge
- Tables: only the name column scrolls for long names, rather than the entire table
- Mobile devices (under 560 px): MAC column hidden to leave more room for names

## 0.2.4
- Traffic card smoothly shrinks into the bar while scrolling (numbers move to the left, graph to the right)
- Nothing protrudes above the model row while scrolling
- Mobile: page was wider than the screen; fixed

## 0.2.3
- Transition to the compact bar with showing and hiding (intermediate version, replaced in 0.2.4)

## 0.2.2
- Compact traffic bar while scrolling (first version)

## 0.2.1
- Names for fixed IP addresses are supplemented from the device list; otherwise "(currently offline)"

## 0.2.0
- Connection type and "Online since" removed, RSRP and SNR instead of signal strength, firmware shortened
- New: fixed IP addresses (DHCP reservations), enable/disable Wi-Fi bands, restart router

## 0.1.0
- Initial version: live traffic, overview, and device list
