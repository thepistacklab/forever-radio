#!/usr/bin/env python3
"""Forever Radio WiFi setup from a phone.

When the radio has no network (no cable, no known WiFi) it stops radiod,
opens an open WiFi hotspot called ForeverRadio-Setup and shows instructions
on the TJC screen. Joining the hotspot pops up a setup page on the phone
(captive portal) listing the WiFi networks the radio can see; pick one, type
the password, and the radio connects and starts playing again.

Plugging in an Ethernet cable ends setup at once. While the setup screen is
up, known networks are retried every RETRY seconds.
Test without unplugging anything:  sudo touch /run/forever-radio-setup
Runs as the forever-radio-wifi-setup systemd service.
"""
import html
import os
import re
import subprocess
import sys
import threading
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

from tjc_class import TJC

AP_NAME = "ForeverRadio-Setup"
AP_ADDR = "10.42.0.1"           # NetworkManager's address in hotspot (shared) mode
TRIGGER = "/run/forever-radio-setup"
GRACE = 90      # seconds after start-up before judging the network
NO_NET = 45     # seconds without any network before setup starts
RETRY = 300     # while in setup, retry known networks this often
# Stopped during setup, in this order, and started again in reverse. The whole
# audio chain goes down together: leaving MPD running with radiod stopped (and the
# watchdog poking it) left the sound card's dmix layer stuck until a reboot.
# mpd.socket is stopped too, or any connection would start MPD again.
# apache2/lighttpd: radiod's web interface also wants port 80.
PAUSE = ("radiod", "forever-radio-watchdog", "mpd", "mpd.socket", "apache2", "lighttpd")


def run(*args, timeout=60):
    try:
        return subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(args, 1, "", "timeout")


def nm_fields(line):
    # nmcli -t separates fields with ':' and escapes a literal ':' as '\:'
    return [f.replace("\\:", ":") for f in re.split(r"(?<!\\):", line)]


def online():
    """True when Ethernet or WiFi is connected (our own hotspot doesn't count)."""
    out = run("nmcli", "-t", "-f", "TYPE,STATE,CONNECTION", "device").stdout
    for line in out.splitlines():
        fields = nm_fields(line) + ["", "", ""]
        kind, state, conn = fields[:3]
        if kind in ("ethernet", "wifi") and state == "connected" and conn != AP_NAME:
            return True
    return False


def scan():
    """WiFi networks in range, strongest first: [(ssid, signal, secured)]."""
    out = run("nmcli", "-t", "-f", "SSID,SIGNAL,SECURITY", "dev", "wifi",
              "list", "--rescan", "yes").stdout
    best = {}
    for line in out.splitlines():
        fields = nm_fields(line) + ["", "", ""]
        ssid, signal, security = fields[:3]
        if not ssid or ssid == AP_NAME:
            continue
        signal = int(signal) if signal.isdigit() else 0
        if ssid not in best or signal > best[ssid][0]:
            best[ssid] = (signal, security not in ("", "--"))
    return sorted(((s, sig, sec) for s, (sig, sec) in best.items()), key=lambda n: -n[1])


def start_hotspot():
    run("nmcli", "con", "delete", AP_NAME)
    run("nmcli", "con", "add", "type", "wifi", "ifname", "wlan0", "con-name", AP_NAME,
        "autoconnect", "no", "ssid", AP_NAME, "802-11-wireless.mode", "ap",
        "802-11-wireless.band", "bg", "ipv4.method", "shared")
    run("nmcli", "con", "up", AP_NAME)


def stop_hotspot():
    run("nmcli", "con", "down", AP_NAME)


def forget(ssid):
    """Delete saved profiles for this network, so the password just typed is the one used."""
    for line in run("nmcli", "-t", "-f", "NAME,TYPE", "con", "show").stdout.splitlines():
        name, kind = (nm_fields(line) + ["", ""])[:2]
        if kind in ("802-11-wireless", "wifi") and name != AP_NAME:
            saved = run("nmcli", "-g", "802-11-wireless.ssid", "con", "show", name).stdout.strip()
            if saved == ssid:
                run("nmcli", "con", "delete", name)


def connect(ssid, password):
    forget(ssid)
    args = ["nmcli", "--wait", "30", "dev", "wifi", "connect", ssid, "ifname", "wlan0"]
    if password:
        args += ["password", password]
    for attempt in range(1, 4):
        # Straight after the hotspot stops, the WiFi hasn't scanned yet and
        # nmcli reports the network as not found - so rescan first
        run("nmcli", "dev", "wifi", "rescan", "ifname", "wlan0")
        time.sleep(5)
        result = run(*args, timeout=45)
        print("wifi_setup: attempt %d to join %s: %s %s" % (attempt, ssid,
              result.stdout.strip(), result.stderr.strip()), flush=True)
        if result.returncode == 0:
            # Power saving causes stream dropouts; the new profile is named after the SSID
            run("nmcli", "con", "modify", ssid, "802-11-wireless.powersave", "2")
            return True
    return False


def recover():
    """Undo a setup that was interrupted (service restart, crash): hotspot off, radio back on."""
    stop_hotspot()
    run("nmcli", "con", "delete", AP_NAME)
    enabled = [s for s in reversed(PAUSE)
               if run("systemctl", "is-enabled", "--quiet", s).returncode == 0]
    if enabled:
        run("systemctl", "start", "--no-block", *enabled)


# ---- setup web page ----

STYLE = """<meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{font-family:sans-serif;background:#111;color:#eee;margin:0;padding:16px;max-width:480px}
h1{color:#fb0;font-size:1.4em}label{display:block;padding:10px;margin:6px 0;background:#222;border-radius:8px}
input[type=text],input[type=password]{width:100%;box-sizing:border-box;padding:10px;font-size:1em;margin:6px 0}
button{width:100%;padding:14px;font-size:1.1em;background:#fb0;border:0;border-radius:8px;margin-top:12px}
.note{color:#f66}</style>"""


def form_page(networks, note=""):
    rows = "".join(
        '<label><input type="radio" name="ssid" value="%s"> %s %s <small>(%d%%)</small></label>'
        % (html.escape(s, True), html.escape(s), "&#128274;" if sec else "", sig)
        for s, sig, sec in networks)
    if not rows:
        rows = "<p>No networks found - type the name below.</p>"
    return ("<!doctype html><title>Forever Radio WiFi</title>%s<h1>Forever Radio WiFi</h1>"
            '<p class="note">%s</p><form method="post" action="/connect">%s'
            '<p>Other network: <input type="text" name="other" placeholder="Network name"></p>'
            '<p>Password: <input type="password" name="password" autocomplete="off"></p>'
            "<button>Connect</button></form>" % (STYLE, html.escape(note), rows))


def done_page(ssid):
    return ("<!doctype html><title>Forever Radio WiFi</title>%s<h1>Connecting...</h1>"
            "<p>The radio is joining <b>%s</b>. Your phone will leave %s now - "
            "watch the radio's screen. If the password was wrong, the setup "
            "network comes back in a minute.</p>" % (STYLE, html.escape(ssid), AP_NAME))


class SetupHandler(BaseHTTPRequestHandler):
    # Every address shows the setup page, which makes phones pop it up by themselves

    def do_GET(self):
        self._page(form_page(self.server.networks, self.server.note))

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        form = urllib.parse.parse_qs(self.rfile.read(length).decode("utf-8", "replace"))
        ssid = form.get("other", [""])[0].strip() or form.get("ssid", [""])[0]
        if not ssid:
            self._page(form_page(self.server.networks, "Please choose a network."))
            return
        self.server.request = (ssid, form.get("password", [""])[0])
        self._page(done_page(ssid))

    def _page(self, body):
        data = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        return


# ---- setup mode ----

def show(tjc, *lines):
    for n in range(1, 6):
        tjc.out(n, lines[n - 1] if n <= len(lines) else "")


def show_waiting(tjc, note=""):
    show(tjc, "No network - WiFi setup", AP_NAME, "On your phone, join this WiFi",
         "A setup page will open", note or "or browse to " + AP_ADDR)


def setup_mode():
    stopped = [s for s in PAUSE
               if run("systemctl", "is-active", "--quiet", s).returncode == 0]
    for service in stopped:
        run("systemctl", "stop", service)

    tjc = TJC(show_network=False)
    tjc.init()
    show(tjc, "No network - WiFi setup", "Searching...")
    networks = scan()
    log("paused %s; found %d networks" % (", ".join(stopped), len(networks)))
    start_hotspot()
    log("hotspot %s is up" % AP_NAME)
    show_waiting(tjc)

    server = HTTPServer(("0.0.0.0", 80), SetupHandler)
    server.networks, server.note, server.request = networks, "", None
    threading.Thread(target=server.serve_forever, daemon=True).start()
    started = time.time()

    while True:
        time.sleep(1)
        if server.request:
            ssid, password = server.request
            server.request = None
            show(tjc, "WiFi setup", "Connecting...", ssid)
            time.sleep(3)               # let the phone receive its page first
            stop_hotspot()
            if connect(ssid, password):
                show(tjc, "WiFi setup", "Connected!", ssid, "Starting the radio...")
                time.sleep(3)
                break
            networks = scan()
            server.networks = networks
            server.note = "Could not join %s - check the password." % ssid
            start_hotspot()
            show_waiting(tjc, "Could not join - try again")
            started = time.time()
        elif online():                  # a cable was plugged in
            log("network came back while the hotspot was up")
            show(tjc, "Network found", "Starting the radio...")
            time.sleep(2)
            break
        elif time.time() - started > RETRY:
            stop_hotspot()
            show(tjc, "WiFi setup", "Looking for known WiFi...")
            for _ in range(30):
                time.sleep(1)
                if online():
                    break
            if online():
                break
            networks = scan()
            server.networks, server.note = networks, ""
            start_hotspot()
            show_waiting(tjc)
            started = time.time()

    server.shutdown()
    stop_hotspot()
    run("nmcli", "con", "delete", AP_NAME)
    for service in reversed(stopped):
        run("systemctl", "start", service)
    # Exit so radiod gets the screen's serial port back; systemd restarts this service
    sys.exit(0)


def log(msg):
    print("wifi_setup: " + msg, flush=True)


def main():
    recover()
    # Give NetworkManager time to join known networks, but react to the trigger at once
    for _ in range(GRACE):
        if os.path.exists(TRIGGER):
            break
        time.sleep(1)
    log("watching the network")
    offline_since = None
    while True:
        if os.path.exists(TRIGGER):
            os.remove(TRIGGER)
            log("setup requested by " + TRIGGER)
            setup_mode()
        if online():
            offline_since = None
        else:
            offline_since = offline_since or time.time()
            if time.time() - offline_since >= NO_NET:
                log("no network for %d seconds" % NO_NET)
                setup_mode()
        time.sleep(5)


if __name__ == "__main__":
    main()
