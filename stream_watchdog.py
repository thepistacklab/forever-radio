#!/usr/bin/env python3
"""Forever Radio stream watchdog.

Internet stations sometimes stall: MPD keeps saying "playing", but no audio
arrives ("Decoder is too slow; playing silence" in mpd.log), and it never
reconnects by itself. Turning the tuner away and back fixes it because that
reconnects. This does the same automatically when either sign of a stall
lasts STALL seconds:
  - the play time stops moving, or
  - mpd.log keeps reporting "Decoder is too slow".
Runs as the forever-radio-watchdog systemd service.
"""
import os
import time

from mpd import MPDClient

MPD_LOG = "/var/log/mpd/mpd.log"
CHECK = 5       # seconds between checks
STALL = 15      # seconds of stall before reconnecting


def connect():
    client = MPDClient()
    client.timeout = 10
    client.connect("localhost", 6600)
    return client


class LogTail:
    """Returns only the mpd.log lines written since the last call."""

    def __init__(self, path):
        self.path = path
        self.pos = os.path.getsize(path) if os.path.exists(path) else 0

    def new_lines(self):
        try:
            size = os.path.getsize(self.path)
            if size < self.pos:         # log was rotated
                self.pos = 0
            with open(self.path, errors="replace") as f:
                f.seek(self.pos)
                text = f.read()
                self.pos = f.tell()
            return text.splitlines()
        except OSError:
            return []


def main():
    client = None
    log = LogTail(MPD_LOG)
    last_progress, last_change = None, time.time()
    silent_checks = 0

    while True:
        time.sleep(CHECK)
        try:
            if client is None:
                client = connect()
            status = client.status()
        except Exception as e:
            print("watchdog: MPD not reachable:", e, flush=True)
            client = None
            continue

        too_slow = any("Decoder is too slow" in line for line in log.new_lines())
        silent_checks = silent_checks + 1 if too_slow else 0

        if status.get("state") != "play" or "song" not in status:
            last_progress, last_change, silent_checks = None, time.time(), 0
            continue

        progress = (status.get("songid"), status.get("elapsed"))
        if progress != last_progress:
            last_progress, last_change = progress, time.time()

        frozen = time.time() - last_change >= STALL
        silent = silent_checks * CHECK >= STALL
        if frozen or silent:
            print("watchdog: stream stalled (%s), reconnecting position %s"
                  % ("frozen" if frozen else "silence", status["song"]), flush=True)
            try:
                client.play(int(status["song"]))
            except Exception as e:
                print("watchdog: reconnect failed:", e, flush=True)
                client = None
            last_progress, last_change, silent_checks = None, time.time(), 0


if __name__ == "__main__":
    main()
