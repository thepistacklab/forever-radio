# Forever Radio

Add-ons that turn a Raspberry Pi 5 and Bob Rathbone's **radiod** into an internet radio that no company can switch off.

> **Pi 5 or Pi 3B+.** The defaults here are for the Pi 5. A Pi 3B+ works too, but the pinout and serial port differ (screen on `/dev/serial0` with `enable_uart=1` and `dtoverlay=disable-bt`, volume encoder on GPIO5/6). The [build guide](https://pidiylab.com/they-bricked-my-radio-so-i-built-a-raspberry-pi-one-they-cant-build-guide/) lists the changes.

Built for the video [*They Bricked My Radio, So I Built a Raspberry Pi One They Can't*](https://youtu.be/8f99HTn9JsE) on [The Pi Stack Lab](https://www.youtube.com/@thepistacklab).

- Station list comes from the open **radio-browser.info** directory, not a company server.
- Written guide with every command and pin: [pidiylab.com build guide](https://pidiylab.com/they-bricked-my-radio-so-i-built-a-raspberry-pi-one-they-cant-build-guide/)

## What is in this repo

| File | What it does |
|---|---|
| `install.sh` | One-command installer for everything below. Run it with `sudo`. |
| `tjc_class.py`, `st7789tft_class.py` | Display driver for a TJC / Nextion 3.5" serial screen (UART4, GPIO12/13 on a Pi 5; see the note above for a Pi 3B+). |
| `ForeverRadio.tft` | The screen file for the TJC4832T135_011. Copy it to a FAT32 microSD card and load it into the screen. |
| `tjc_layout.md` | How to make the screen's `ForeverRadio.tft` file (one time only). |
| `dial.conf`, `rb_import.py`, `refresh_dial.sh` | Build the station dial (Country, Decade, Genre) from radio-browser. |
| `forever-radio-dial.service` / `.timer` | Refresh the dial every week. |
| `stream_watchdog.py`, `forever-radio-watchdog.service` | Reconnects a station that goes silent. |
| `wifi_setup.py`, `forever-radio-wifi-setup.service` | Set up Wi-Fi from your phone when the radio finds no network. |

## Install

1. Build the radio first with radiod, as the guide shows (Raspberry Pi OS Lite 64-bit, radiod 8.3, Adafruit Speaker Bonnet, two KY-040 encoders).
2. Copy this folder to the Pi. Use a path with no spaces, for example `~/forever-radio`.
3. Run:

```bash
cd ~/forever-radio
sudo bash install.sh
sudo reboot
```

## Credits

- [Bob Rathbone's Raspberry Pi Radio (radiod)](https://bobrathbone.com), the software this builds on.
- [radio-browser.info](https://www.radio-browser.info), the open station directory.

## License

GPL-3.0, the same family of license as radiod. See `LICENSE`.

Use at home. Playing music in a business usually needs a music license.
