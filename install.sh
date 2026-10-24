#!/bin/bash
# Forever Radio add-ons for Bob Rathbone's radiod (install radiod first).
# Copy this whole folder to the Pi, then from inside it run:  sudo bash install.sh
#   - TJC 3.5" serial screen driver (tjc_class.py) on UART4, GPIO12/13
#   - radiod waits for the network at boot; web interface fix for Python 3.13
#   - stream watchdog: reconnects stations that stall into silence
#   - weekly station dial rebuilt from radio-browser.info (dial.conf)
#   - WiFi setup from a phone when no network is found (wifi_setup.py)
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
if [ "$(id -u)" -ne 0 ]; then echo "Please run: sudo bash install.sh"; exit 1; fi
case "$DIR" in *" "*) echo "Move this folder to a path without spaces (e.g. ~/forever-radio)"; exit 1;; esac

# Files copied from Windows can carry CRLF line endings
sed -i 's/\r$//' "$DIR"/*.sh "$DIR"/*.py "$DIR"/*.conf "$DIR"/*.service "$DIR"/*.timer
chmod +x "$DIR/refresh_dial.sh" "$DIR/stream_watchdog.py"

echo "== Packages"
apt-get install -y python3-serial python3-legacy-cgi dnsmasq-base

echo "== TJC screen driver"
RADIO=/usr/share/radio
[ -f "$RADIO/st7789tft_class.py.orig" ] || cp "$RADIO/st7789tft_class.py" "$RADIO/st7789tft_class.py.orig"
cp "$DIR/tjc_class.py" "$DIR/st7789tft_class.py" "$RADIO/"
sed -i 's/^display_type=.*/display_type=ST7789TFT/' /etc/radiod.conf
REBOOT=no
if ! grep -q '^dtoverlay=uart4-pi5' /boot/firmware/config.txt; then
    echo 'dtoverlay=uart4-pi5' >> /boot/firmware/config.txt
    REBOOT=yes
fi

echo "== radiod waits for the network at boot"
mkdir -p /etc/systemd/system/radiod.service.d
printf '[Unit]\nWants=network-online.target\nAfter=network-online.target\n' \
    > /etc/systemd/system/radiod.service.d/wait-online.conf

echo "== WiFi setup hotspot: every web address leads to the setup page"
mkdir -p /etc/NetworkManager/dnsmasq-shared.d
echo "address=/#/10.42.0.1" > /etc/NetworkManager/dnsmasq-shared.d/forever-radio-setup.conf

echo "== Watchdog, WiFi setup and weekly dial refresh"
for unit in forever-radio-dial.service forever-radio-dial.timer \
            forever-radio-watchdog.service forever-radio-wifi-setup.service; do
    sed "s|@DIR@|$DIR|g" "$DIR/$unit" > "/etc/systemd/system/$unit"
done
systemctl daemon-reload
systemctl enable --now forever-radio-dial.timer forever-radio-watchdog.service \
                       forever-radio-wifi-setup.service

echo "== Building the station dial now (a few minutes)"
"$DIR/refresh_dial.sh"

echo
echo "Forever Radio add-ons installed."
[ "$REBOOT" = yes ] && echo "Reboot once to enable the screen's serial port:  sudo reboot"
exit 0
