#!/usr/bin/env python3
"""Stand-alone test for the 1.8" ST7735 TFT (128x160) - no radiod needed.

Wiring (physical pins): LED->17 (3.3V)  RESET->13 (GPIO27)  DC->22 (GPIO25)
                        SDA->19 (MOSI)  SCL->23 (SCLK)  CS->24 (CE0)
                        VCC->2 (5V)     GND->20
Needs:  sudo apt install -y python3-spidev python3-gpiozero
        SPI enabled (sudo raspi-config nonint do_spi 0)
Run:    python3 tft_test.py            (or: python3 tft_test.py bgr)
"""
import sys
import time

import spidev
from gpiozero import DigitalOutputDevice

WIDTH, HEIGHT = 128, 160
DC_PIN, RST_PIN = 25, 27
BGR = len(sys.argv) > 1 and sys.argv[1].lower() == "bgr"

dc = DigitalOutputDevice(DC_PIN)
rst = DigitalOutputDevice(RST_PIN, initial_value=True)
spi = spidev.SpiDev()
spi.open(0, 0)              # SPI0, CE0
spi.max_speed_hz = 16000000
spi.mode = 0


def command(cmd, data=None):
    dc.off()
    spi.writebytes([cmd])
    if data:
        dc.on()
        spi.writebytes2(bytes(data))


def init():
    rst.off(); time.sleep(0.02); rst.on(); time.sleep(0.15)   # hardware reset
    command(0x01); time.sleep(0.15)        # software reset
    command(0x11); time.sleep(0.25)        # sleep out
    command(0x3A, [0x05])                  # 16-bit colour
    command(0x36, [0x08 if BGR else 0x00]) # memory access / colour order
    command(0x20)                          # inversion off
    command(0x13); time.sleep(0.01)        # normal display on
    command(0x29); time.sleep(0.1)         # display on


def rgb565(r, g, b):
    v = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
    return bytes([v >> 8, v & 0xFF])


def window(x0, y0, x1, y1):
    command(0x2A, [0, x0, 0, x1])
    command(0x2B, [0, y0, 0, y1])
    command(0x2C)


def rect(x0, y0, x1, y1, color):
    window(x0, y0, x1, y1)
    dc.on()
    spi.writebytes2(color * ((x1 - x0 + 1) * (y1 - y0 + 1)))


def fill(color):
    rect(0, 0, WIDTH - 1, HEIGHT - 1, color)


init()
for name, col in (("RED", (255, 0, 0)), ("GREEN", (0, 255, 0)),
                  ("BLUE", (0, 0, 255)), ("WHITE", (255, 255, 255))):
    print("Screen should be", name)
    fill(rgb565(*col))
    time.sleep(2)

print("Black screen with a white 1-pixel border on all four edges")
fill(rgb565(0, 0, 0))
white = rgb565(255, 255, 255)
rect(0, 0, WIDTH - 1, 0, white)
rect(0, HEIGHT - 1, WIDTH - 1, HEIGHT - 1, white)
rect(0, 0, 0, HEIGHT - 1, white)
rect(WIDTH - 1, 0, WIDTH - 1, HEIGHT - 1, white)
print("Done - the border stays on screen.")
spi.close()
