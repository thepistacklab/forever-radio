#!/usr/bin/env python3
"""Import stations from the open radio-browser directory into radiod.

Adds (or replaces) named playlists in /var/lib/radiod/stationlist,
using radiod's own format:

    (Playlist Name)
    [Station title] http://stream-url
    <blank line ends the playlist>

One playlist:
    sudo python3 rb_import.py "Jazz USA" tag=jazz countrycode=US limit=25

Every playlist in a dial file (used by the weekly refresh):
    sudo python3 rb_import.py --config dial.conf

Any radio-browser search field works as key=value (tag, countrycode,
language, name, codec ...). Then run create_stations.py to build playlists.
If a search fails, that playlist keeps its previous stations.
"""
import json
import random
import shlex
import shutil
import sys
import time
import urllib.parse
import urllib.request

STATIONLIST = "/var/lib/radiod/stationlist"
UA = {"User-Agent": "ForeverRadio-rb_import/1.1"}
DEFAULTS = {"hidebroken": "true", "order": "clickcount", "reverse": "true", "limit": "25"}


def get_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def pick_server():
    # radio-browser asks clients to choose one of its mirror servers
    servers = get_json("https://all.api.radio-browser.info/json/servers")
    names = sorted({s["name"] for s in servers})
    return random.choice(names)


def clean(title):
    # [ and ] would break radiod's [title] field; keep titles on one line
    for ch in "[]\r\n\t":
        title = title.replace(ch, " ")
    return " ".join(title.split())[:60] or "Station"


def playlist_name(name):
    return clean(name).replace("(", "").replace(")", "")


def parse_filters(args):
    params = dict(DEFAULTS)
    for arg in args:
        if "=" not in arg:
            raise ValueError("Bad filter '%s' - use key=value" % arg)
        key, value = arg.split("=", 1)
        params[key] = value
    return params


def fetch_lines(server, params):
    url = "https://%s/json/stations/search?%s" % (server, urllib.parse.urlencode(params))
    lines, seen = [], set()
    for s in get_json(url):
        stream = (s.get("url_resolved") or s.get("url") or "").strip()
        if not stream.startswith(("http://", "https://")) or " " in stream or stream in seen:
            continue
        # MPD can't play HLS (.m3u8) streams over plain http - they play silence and can stall it
        if str(s.get("hls")) == "1" or ".m3u8" in stream.lower():
            continue
        seen.add(stream)
        lines.append("[%s] %s" % (clean(s.get("name", "")), stream))
    return lines


def read_config(path):
    """Each line: Name | key=value key="value with spaces" ..."""
    jobs = []
    with open(path, encoding="utf-8") as f:
        for n, raw in enumerate(f, 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "|" not in line:
                sys.exit("%s line %d: expected 'Name | key=value ...'" % (path, n))
            name, filters = line.split("|", 1)
            jobs.append((playlist_name(name), parse_filters(shlex.split(filters))))
    return jobs


def write_stationlist(blocks):
    """blocks: {playlist name: [station lines]} - replaces those playlists."""
    with open(STATIONLIST, encoding="utf-8") as f:
        old = f.read().split("\n")

    names = {"(%s)" % n for n in blocks}
    kept, skipping = [], False
    for line in old:
        if line.strip() in names:
            skipping = True
            continue
        if skipping:
            if line.strip() == "":
                skipping = False
            continue
        kept.append(line)
    while kept and kept[-1].strip() == "":
        kept.pop()

    backup = "%s.bak-%s" % (STATIONLIST, time.strftime("%Y%m%d-%H%M%S"))
    shutil.copy2(STATIONLIST, backup)

    out = kept[:]
    for name, lines in blocks.items():
        out += ["", "(%s)" % name] + lines
    out.append("")
    with open(STATIONLIST, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    return backup


def existing_block(name):
    """Current stations of one playlist, used when a search fails."""
    lines, inside = [], False
    with open(STATIONLIST, encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            if line.strip() == "(%s)" % name:
                inside = True
                continue
            if inside:
                if line.strip() == "":
                    break
                lines.append(line)
    return lines


def main():
    args = sys.argv[1:]
    if len(args) == 2 and args[0] == "--config":
        jobs = read_config(args[1])
    elif len(args) >= 2 and not args[0].startswith("--"):
        jobs = [(playlist_name(args[0]), parse_filters(args[1:]))]
    else:
        print(__doc__)
        sys.exit(1)

    server = pick_server()
    blocks, failed = {}, 0
    for name, params in jobs:
        try:
            lines = fetch_lines(server, params)
        except Exception as exc:  # network/API failure: keep the old stations
            lines = []
            print("(%s) search failed: %s" % (name, exc))
        if not lines:
            failed += 1
            lines = existing_block(name)
            print("(%s) no new stations - keeping %d existing" % (name, len(lines)))
            if not lines:
                continue
        else:
            print("(%s) %d stations" % (name, len(lines)))
        blocks[name] = lines
        time.sleep(1)  # be polite to the volunteer-run directory

    if not blocks:
        sys.exit("Nothing to write.")
    backup = write_stationlist(blocks)
    print("Updated %d playlist(s) from %s (%d kept unchanged)" % (len(blocks), server, failed))
    print("Backup of the old station list: %s" % backup)


if __name__ == "__main__":
    main()
