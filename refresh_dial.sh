#!/bin/bash
# Rebuild the Forever Radio dial from the open radio-browser directory.
#   1. Import every playlist in dial.conf into /var/lib/radiod/stationlist
#   2. Rebuild radiod's radio playlists (non-interactive)
#   3. Restart radiod so the knob sees the new playlists
#   4. Keep only the newest 10 station-list backups
# Run as root (the systemd timer does this weekly), or: sudo ./refresh_dial.sh
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"

echo "== Importing dial from $DIR/dial.conf"
python3 "$DIR/rb_import.py" --config "$DIR/dial.conf"

echo "== Rebuilding radiod playlists"
cd /usr/share/radio
./create_stations.py --delete_old

echo "== Restarting radiod"
systemctl restart radiod

echo "== Pruning old station-list backups (keeping 10)"
ls -1t /var/lib/radiod/stationlist.bak-* 2>/dev/null | tail -n +11 | xargs -r rm -f

echo "== Dial refresh finished"
