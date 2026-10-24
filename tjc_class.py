#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# TJC / Nextion serial HMI display driver for Bob Rathbone's radiod
# Forever Radio build - The Pi Stack Lab
#
# radiod has no driver for serial HMI screens, so this class offers the same
# interface as radiod's ST7789TFT driver. The one-line st7789tft_class.py shim
# imports it, and display_type=ST7789TFT in /etc/radiod.conf selects it.
#
# The screen's .tft file only has to contain three fonts (ids 0, 1, 2) and an
# empty page - no objects. Everything is drawn from here with the TJC's
# built-in xstr (text) and fill (rectangle) commands:
#   line 1  time/date or menu heading   small font,  grey
#   line 2  station name                big font,    amber  (scrolls if long)
#   line 3  track title / stream info   medium font, white  (scrolls if long)
#   line 4  "Station 3/40 Jazz"         small font,  grey
#   line 5  bit rate or "Muted"         small font,  grey
#   volume  0-100                       amber bar along the bottom
#
# Test without radiod:  python3 tjc_class.py

import threading
import time
import unicodedata

import serial

PORT = "/dev/ttyAMA4"   # UART4 on GPIO12/13 (dtoverlay=uart4-pi5)
BAUD = 9600
ENCODING = "utf-8"      # must match the encoding the fonts were made with
END = b"\xff\xff\xff"   # every TJC command ends with three 0xFF bytes

# RGB565 colours
BLACK, WHITE = 0, 65535
GREY, AMBER, DARK = 42260, 64896, 6339

# line: (x, y, w, h, font id, colour)
LAYOUT = {
    1: (8, 6, 372, 36, 0, GREY),
    2: (8, 52, 464, 60, 2, AMBER),
    3: (8, 122, 464, 50, 1, WHITE),
    4: (8, 184, 464, 36, 0, GREY),
    5: (8, 228, 464, 36, 0, GREY),
}
FONT_PX = {0: 24, 1: 32, 2: 40}     # height of each font in the .tft
NET_BOX = (388, 6, 84, 36)          # top-right corner: LAN / WiFi / No net
VOLUME_BAR = (8, 280, 464, 28)
SCROLL_DELAY = 0.4      # seconds per scroll step
SCROLL_GAP = "     "    # space between the end and the restart of a scrolling line
REFRESH = 10            # seconds between full redraws

# Approximate Arial character widths, as a fraction of the font height. Text that
# is too wide would wrap onto a second, cut-off line, so it is scrolled instead.
NARROW = set("iljtfrI1.,:;!|'`()[]-")
WIDE = set("MWmw@%")


def char_width(ch):
    if ch == " ":
        return 0.28
    if ch in NARROW:
        return 0.32
    if ch in WIDE:
        return 0.86
    if ch.isupper():
        return 0.70
    return 0.56


def fit(text, font, width):
    """Longest start of text that fits in width pixels."""
    used, px = 0.0, FONT_PX[font]
    for i, ch in enumerate(text):
        used += char_width(ch) * px
        if used > width:
            return text[:i]
    return text


def network_label():
    def read(path):
        try:
            with open(path) as f:
                return f.read().strip()
        except OSError:
            return ""
    if read("/sys/class/net/eth0/carrier") == "1" and read("/sys/class/net/eth0/operstate") == "up":
        return "LAN"
    if read("/sys/class/net/wlan0/operstate") == "up":
        return "WiFi"
    return "No net"


def no_interrupt():
    return False


class TJC:
    nlines = 5
    nchars = 40

    def __init__(self, show_network=True):
        self.show_network = show_network    # wifi_setup.py turns the corner label off
        self.lock = threading.Lock()
        self.port = None
        self.callback = None
        self.TextLines = [""] * (self.nlines + 1)
        self.scrolling = {}     # line -> [text, position]
        self.saved_volume = -1

    def init(self, callback=None, flip=False):
        self.callback = callback
        self._open()
        self._send("")      # a bare terminator flushes any half-received command
        self.clear()
        self._draw_network()
        threading.Thread(target=self._scroller, daemon=True).start()

    def _open(self):
        try:
            self.port = serial.Serial(PORT, BAUD, timeout=0.2)
        except (serial.SerialException, OSError) as e:
            print("TJC: cannot open", PORT, e)
            self.port = None

    def _send(self, cmd):
        # radiod and the scroller thread both draw, so serialise the writes
        with self.lock:
            if self.port is None:
                self._open()
                if self.port is None:
                    return
            try:
                self.port.write(cmd.encode(ENCODING, errors="replace") + END)
            except (serial.SerialException, OSError) as e:
                print("TJC: write failed", e)
                self.port = None

    @staticmethod
    def _ascii(text):
        # The fonts hold ASCII only, so turn accented letters into plain ones (Ö -> O)
        text = unicodedata.normalize("NFKD", text)
        return "".join(ch for ch in text if " " <= ch <= "~")

    @staticmethod
    def _quote(text):
        return text.replace("\\", "\\\\").replace('"', '\\"')

    def _draw(self, line, text):
        x, y, w, h, font, colour = LAYOUT[line]
        # xstr x,y,w,h,font,text colour,background,left,centre-vertically,solid background,"text"
        self._send('xstr %d,%d,%d,%d,%d,%d,%d,0,1,1,"%s"'
                   % (x, y, w, h, font, colour, BLACK, self._quote(text)))

    def _refresh(self):
        # Redraw everything, so a command the screen dropped is fixed within REFRESH seconds
        for line in range(1, self.nlines + 1):
            if line not in self.scrolling:
                self._draw(line, self._ascii(self.TextLines[line]))
        if self.saved_volume >= 0:
            self._draw_volume(self.saved_volume)
        self._draw_network()

    def _draw_network(self):
        if self.show_network:
            x, y, w, h = NET_BOX
            # right-aligned (xcen=2) in the corner of the clock line
            self._send('xstr %d,%d,%d,%d,0,%d,%d,2,1,1,"%s"'
                       % (x, y, w, h, GREY, BLACK, network_label()))

    def _scroller(self):
        last_refresh = time.time()
        while True:
            time.sleep(SCROLL_DELAY)
            if time.time() - last_refresh >= REFRESH:
                last_refresh = time.time()
                self._refresh()
            for line, state in list(self.scrolling.items()):
                text, pos = state
                _, _, w, _, font, _ = LAYOUT[line]
                loop = text + SCROLL_GAP
                pos = (pos + 1) % len(loop)
                state[1] = pos
                if self.scrolling.get(line) is state:
                    self._draw(line, fit((loop + loop)[pos:], font, w))

    # ---- radiod display interface ----

    def out(self, line, text, interrupt=no_interrupt):
        if line < 1 or line > self.nlines or text == self.TextLines[line]:
            return
        self.TextLines[line] = text
        self.scrolling.pop(line, None)
        _, _, w, _, font, _ = LAYOUT[line]
        plain = self._ascii(text)
        shown = fit(plain, font, w)
        self._draw(line, shown)
        if shown != plain:
            self.scrolling[line] = [plain, 0]

    def volume(self, vol):
        vol = max(0, min(100, int(vol)))
        if vol == self.saved_volume:
            return
        self.saved_volume = vol
        self._draw_volume(vol)

    def _draw_volume(self, vol):
        x, y, w, h = VOLUME_BAR
        filled = w * vol // 100
        if filled > 0:
            self._send("fill %d,%d,%d,%d,%d" % (x, y, filled, h, AMBER))
        if filled < w:
            self._send("fill %d,%d,%d,%d,%d" % (x + filled, y, w - filled, h, DARK))

    def clear(self):
        self.scrolling.clear()
        self._send("cls %d" % BLACK)
        self.TextLines = [""] * (self.nlines + 1)
        self.saved_volume = -1

    def drawSplash(self, image, delay):
        self.out(2, "Forever Radio")
        time.sleep(delay)

    def update(self):
        return              # the TJC draws as soon as it receives a command

    def setScrollSpeed(self, scroll_speed):
        return              # see SCROLL_DELAY

    def setWidth(self, width):
        return self.getWidth()

    def getWidth(self):
        # radiod divides this by 5 to estimate characters per line; 30 keeps
        # line 1 to time/date only (40+ would append the station name to it)
        return 150

    def getLines(self):
        return self.nlines

    def getChars(self):
        return self.nchars

    def hasColor(self):
        return False

    def setFontSize(self, size):
        return

    def setFontScale(self, scale):
        return

    def setFontName(self, name):
        return


if __name__ == "__main__":
    tjc = TJC()
    tjc.init()
    tjc.out(1, "18:30 Wednesday 22 October")
    tjc.out(2, "ROCK ANTENNE Österreich")
    tjc.out(3, "Blondie - Heart of Glass (a long title that should scroll by itself)")
    tjc.out(4, "Station 38/485 Rock")
    tjc.out(5, "Bit rate: 128K")
    for v in range(0, 101, 10):
        tjc.volume(v)
        time.sleep(0.2)
    print("Test screen sent - watching the title scroll for 15 seconds")
    time.sleep(15)
