# They Bricked My Radio, So I Built a Raspberry Pi One They Can't — Build Guide

The written companion to the video. A Tangent Quattro internet radio died in 2021 when Reciva shut down its station directory. This guide puts a Raspberry Pi inside it. The Pi runs Bob Rathbone's open-source **radiod** and gets its stations from **radio-browser.info**, an open, volunteer-run directory that no company owns.

**As built:** Raspberry Pi 5 · Raspberry Pi OS Lite 64-bit (Trixie) · radiod 8.3 · Adafruit Speaker Bonnet · 2× KY-040 rotary encoders · TJC 3.5" serial screen (TJC4832T135_011).

**Files for this build** (screen file, driver, install script): **[REPO LINK]**

---

## Why it can't be bricked

- A station directory tells a radio where each stream lives. Reciva's directory was private: one owner, one off-switch.
- **radio-browser.info** is open, free and mirrored on many servers.
- The radio rebuilds its station list from radio-browser every week, and keeps the list **on its own SD card**. If the directory ever disappears, the radio keeps its last list and keeps playing.
- All the software is open source: Raspberry Pi OS, MPD, radiod, and the add-ons in this guide.

---

## Parts

| Part | Notes |
|---|---|
| Raspberry Pi 5 (any RAM size) + official 27 W USB-C supply + microSD card | |
| **Adafruit Speaker Bonnet** | Amplifier, stereo 3 W per channel, for 4–8 Ω speakers. It drives the radio's original speaker directly. |
| **2× KY-040 rotary encoder** | One for volume (push = mute), one for tuning (push = menu). |
| **TJC 3.5" serial screen, TJC4832T135_011** | Serial (UART) screen: 5V, TX, RX, GND. Mine came from an MMDVM ham radio hotspot. |
| 40-pin GPIO **1-to-2 expansion board** + 2×20 header | The Speaker Bonnet sits on one header; the jumper wires go on the other. |
| Female-female jumper wires | Cheap Dupont wires fail. Keep spares. |
| microSD card for the screen | FAT32, used once to load the screen file. |
| Multimeter | To check pins and voltages. It saved this build twice. |
| A case | I used the dead Tangent Quattro. |

---

## Pin map (physical pin numbers on the Pi header)

| Device | Pin → Pi pin |
|---|---|
| **Speaker Bonnet** | Plugs onto the header. Uses GPIO18, 19 and 21 (I2S audio). |
| **Volume KY-040** | **+ → 1 (3.3 V)** · GND → 9 · SW → 7 (GPIO4) · DT → 10 (GPIO15) · CLK → 8 (GPIO14) |
| **Tuning KY-040** | **+ → 17 (3.3 V)** · GND → 14 · SW → 11 (GPIO17) · DT → 18 (GPIO24) · CLK → 16 (GPIO23) |
| **TJC screen** | 5V → 4 · GND → 6 · TX → 33 (GPIO13, RXD4) · RX → 32 (GPIO12, TXD4) |

> ⚠️ **KY-040 `+` goes to 3.3 V only.** On 5 V, the encoder's pull-up resistors put 5 V onto the Pi's GPIO pins.
> ⚠️ **Find power pins with a multimeter before you power any new board.** I connected a 1.8" screen backwards from memory and killed it.

---

## 1. Flash Raspberry Pi OS

1. Open **Raspberry Pi Imager**. Select **Raspberry Pi 5**, then **Raspberry Pi OS (other) → Raspberry Pi OS Lite (64-bit)**.
2. In the settings, set:
   - hostname **WebRadio**
   - your user and password
   - **SSH** on
   - your Wi-Fi name and password
   - your Wi-Fi country and time zone
3. Write the card. Boot the Pi.
4. From your computer:

   ```bash
   ssh hrw3@webradio.local
   ```

   Use your own user name. If you reflashed an older Pi with the same name, first run `ssh-keygen -R webradio.local` on the computer.
5. Update the Pi:

   ```bash
   sudo apt update && sudo apt -y upgrade
   ```

> ⚠️ Bob Rathbone's warning for Trixie: **never** run `apt full-upgrade`, `rpi-update` or `apt autoremove` on the radio.

**If `nmcli dev status` shows `wlan0 unavailable`,** the Wi-Fi country is not set:

```bash
sudo raspi-config nonint do_wifi_country US && sudo rfkill unblock wifi
sudo nmcli --ask dev wifi connect "YourWiFi" ifname wlan0
sudo nmcli con modify "YourWiFi" 802-11-wireless.powersave 2 && sudo nmcli con up "YourWiFi"
```

Wi-Fi power saving causes stream dropouts, so the last line turns it off.

---

## 2. Install radiod and the Speaker Bonnet

With the Pi off, fit the expansion board, then the Speaker Bonnet, then connect a speaker to the bonnet. Turn the Pi on.

```bash
sudo apt -y install mpd mpc python3-mpd wget
wget https://bobrathbone.com/raspberrypi/packages/radiod_8.3_all.deb
sudo dpkg -i radiod_8.3_all.deb
```

The installer asks questions. My answers:

| Question | Answer |
|---|---|
| User interface | **Rotary encoders** |
| Wiring | **40-pin** version |
| Encoder type | **KY-040 with no resistor R1**. This works on every KY-040 board. |
| Display | **No display**. The add-on installer in step 5 sets up the screen. |
| Configure audio | **Yes**, then **Adafruit Speaker Bonnet** |

Check the audio lines in the boot configuration:

```bash
grep -n -E 'dtoverlay|dtparam=audio' /boot/firmware/config.txt
```

You need `dtparam=audio=off`, and **one** `dtoverlay=hifiberry-dac`. Do **not** also add `dtoverlay=max98357a`, because that is a duplicate overlay. Reboot. Then:

```bash
aplay -l | grep -i card; mpc status
```

The bonnet shows as **card 0: sndrpihifiberry**, and a station shows `[playing]`.

---

## 3. Wire and test the encoders

Turn the Pi **off**. Wire both KY-040s as in the pin map: `+` to **3.3 V** only. Turn the Pi on, then:

```bash
radio-config
```

Open **Diagnostics → Test rotary encoders**. Turn and push each knob. You see `Volume event 1 CLOCKWISE`, `Tuner event 2 ANTICLOCKWISE`, `BUTTON DOWN` and so on. Press Ctrl-C to stop.

- **Wrong direction:** swap that knob's CLK and DT wires.
- **Two events per click:** change `rotary_step_size` in `/etc/radiod.conf` (`half` or `full`).

---

## 4. The TJC screen

radiod has no driver for serial screens. The add-ons include one (`tjc_class.py`). The Pi draws all the text and the volume bar. The screen only needs a file with three fonts.

1. **Check the TX voltage first.** Connect only the screen's 5V (pin 4) and GND (pin 6). Measure the screen's **TX to GND**. About **3.3 V** is safe. If it reads about 5 V, add a resistor divider before you connect TX to the Pi.
2. **Load the screen file.**
   - Copy **ForeverRadio.tft** (from the repo) to the root of a FAT32 microSD card. Put only that file on the card.
   - With the power off, put the card in the **screen's** slot. Turn on.
   - The screen installs the file and shows **"update successed!"**
   - Turn off, **remove the card**, and turn on. The screen is blank.
   - The file is for the **TJC4832T135_011**. For a different TJC or Nextion model, see "Make your own screen file" below.
3. **Wire TX and RX** with the Pi off: screen TX → pin 33, screen RX → pin 32. The wires cross over. If they're swapped, the screen doesn't work, but nothing is damaged.
4. The add-on installer (step 5) turns on the serial port (`dtoverlay=uart4-pi5`) and installs the driver.

---

## 5. Install the Forever Radio add-ons (one command)

Copy the **forever-radio** folder from the repo to the Pi, for example to `~/forever-radio` (no spaces in the path). From Windows PowerShell:

```bash
ssh hrw3@webradio.local "mkdir -p ~/forever-radio"
scp install.sh refresh_dial.sh rb_import.py dial.conf stream_watchdog.py wifi_setup.py tjc_class.py st7789tft_class.py forever-radio-*.service forever-radio-dial.timer hrw3@webradio.local:~/forever-radio/
```

Then **on the Pi**:

```bash
cd ~/forever-radio && sudo bash install.sh
```

It installs:

| Add-on | What it does |
|---|---|
| **Screen driver** | `tjc_class.py`, plus a one-line shim that uses radiod's ST7789TFT display slot (`display_type=ST7789TFT`). Bob's original file is kept as `st7789tft_class.py.orig`. |
| **Network wait** | radiod waits for the network at boot (`radiod.service.d/wait-online.conf`). |
| **Web-interface fix** | `python3-legacy-cgi` (Python 3.13 removed the `cgi` module). |
| **Station dial** | `rb_import.py` + `dial.conf` + `refresh_dial.sh`. It builds grouped playlists from radio-browser now, then every Sunday at 04:00 (`forever-radio-dial.timer`). |
| **Stream watchdog** | `stream_watchdog.py`. It reconnects a station that is silent for 15 seconds. |
| **Wi-Fi setup** | `wifi_setup.py`. With no network, the radio becomes a hotspot and you set up Wi-Fi from your phone. |

The dial build takes a few minutes. If the script says so, reboot once.

> After a radiod update, run `sudo bash install.sh` again. The update puts back Bob's ST7789 file.

---

## 6. Use it

**Screen:**

- Line 1: time and date (menu headings appear here too). The top-right corner shows **LAN**, **WiFi** or **No net**.
- Line 2: station, large and amber.
- Line 3: song title.
- Line 4: `Station 3/40 Genre Jazz`.
- Line 5: bit rate, or "Muted".
- Bottom: the volume bar.

Long lines scroll. The screen redraws everything every 10 seconds, so a dropped command fixes itself.

**Knobs:** volume (push = mute). Tuning changes station; push it to step through the menus: **Search → Input Source → Options**.

**Change playlist:** push the tuning knob until **Input Source** shows, turn to a playlist, then push.

**Station dial** (`~/forever-radio/dial.conf`). One line per playlist, in the form `Name | radio-browser search`:

```text
Country Japan     | countrycode=JP limit=25
Decade 80s        | tag=80s limit=30
Genre Jazz        | tag=jazz limit=40
News US           | tag=news countrycode=US limit=25
```

radiod lists playlists **alphabetically**, with no sub-menus, so a shared first word keeps groups together. Useful filters are `tag=`, `countrycode=`, `language=`, `name=` and `limit=`. To apply changes now:

```bash
sudo ~/forever-radio/refresh_dial.sh
```

If a search fails, that playlist keeps its old stations.

**Watchdog log:**

```bash
journalctl -u forever-radio-watchdog -f
```

It shows lines like `stream stalled (silence), reconnecting`. Some stations drop on a timer; one of my news stations drops every ~10 minutes.

**Wi-Fi from your phone:**

1. With no cable and no known Wi-Fi for about 45 seconds, the screen shows **"No network – WiFi setup / ForeverRadio-Setup"**.
2. On the phone, join **ForeverRadio-Setup** (open network). If the phone says "no internet", select **stay connected**.
3. The setup page opens by itself. If it doesn't, open **http://10.42.0.1**.
4. Select your network, type the password, and select **Connect**.
5. The screen shows **Connected!**, and the radio plays.

Notes:

- The first network scan can take about a minute ("Searching…").
- Plugging in a network cable ends setup immediately.
- To test without unplugging anything: `sudo touch /run/forever-radio-setup`.
- The hotspot is open, and exists only while the setup screen is showing.

---

## 7. Into the case (the gut-and-refit)

- Remove the dead Reciva board. Keep the case, the **speaker**, and the knob holes.
- **Speaker:** read the label on the magnet. The Speaker Bonnet suits **4–8 Ω**. For a single (mono) speaker, use one channel.
- **Knobs:** mount the KY-040s through the original holes. Their shafts take standard knobs; the original knobs may fit.
- **Screen:** cut a window for the 3.5" screen's visible area. Measure the screen itself; don't use a datasheet.
- **Power:** one 27 W USB-C supply powers the Pi, the bonnet and the screen.
- Hold the Pi on standoffs. Keep the jumper wires short, and check every pin after you close the case.

---

## Make your own screen file (other TJC / Nextion models)

Only needed if your screen is not a TJC4832T135_011. Use TJC's **USART HMI** editor (download from wiki.tjc1688.com). Nextion screens use the Nextion Editor, and the same idea applies.

1. **New project.** Select your **exact model**: toolbar **设备 (Device)**. The editor defaulted to a T035 for me; a file for the wrong model is rejected. Landscape, encoding **utf-8**.
2. **Tools (工具) → Font generator (字库制作).** Make three fonts, **in this order**, with range **ASCII (ASCII字符)**:
   - ID 0 = 24 px
   - ID 1 = 32 px
   - ID 2 = 40 px
3. Leave the page **empty**.
4. **Compile (编译):** 0 errors. Then **File → Open build folder**, and copy the `.tft` file.
5. If your screen is not 480×320, change `LAYOUT`, `NET_BOX` and `VOLUME_BAR` at the top of `tjc_class.py`.

---

## Troubleshooting (all of these happened on this build)

| Symptom | Cause and fix |
|---|---|
| `wlan0 unavailable` | Wi-Fi country not set. See step 1. |
| No sound: `Failed to open ALSA device "plug:softvol": Invalid argument` / `dmix … unable to open slave` | The sound card's sharing layer got stuck after services stopped in the wrong order. **Reboot.** The Wi-Fi setup now stops radiod, the watchdog and MPD together, to prevent it. |
| Station silent, but `mpc` says `[playing]`, and the log shows `Decoder is too slow; playing silence` | The station's server stopped sending. The watchdog reconnects it automatically. Before the watchdog, turning the knob away and back fixed it. |
| MPD freezes on BBC stations | BBC streams are HLS (`.m3u8`). `rb_import.py` skips HLS stations by default. |
| Screen stays white / ignores commands | Check the jumper wires first: a loose pin did exactly this. Then test the speeds: `cls` at 9600 and 115200. |
| Song title doesn't update | The screen sometimes drops a command; the 10-second redraw fixes it. Update `tjc_class.py` if your copy is older. |
| Long titles wrap onto a cut-off second line | Fixed in the driver: it measures each line's width and scrolls it instead. |
| Web interface: `select_source.cgi` internal error | `sudo apt install python3-legacy-cgi` (included in `install.sh`). |
| `scp: Could not resolve hostname c:` | You ran `scp` on the Pi. Run it in **PowerShell on the PC**. |
| `Host key verification failed` after a reflash | `ssh-keygen -R webradio.local` and `ssh-keygen -R <ip>` on the PC. |

---

## ⚠️ Honest note: business use

At home, this radio is all yours. In a business (shop, clinic, waiting room), playing music to the public usually needs a **music license**. That's what paid background-music services sell. Check licensing before you use this commercially.

---

## Sources and documentation

- Bob Rathbone, Raspberry Pi Internet Radio (radiod) and the Constructor's Manual: https://bobrathbone.com/raspberrypi/pi_internet_radio.html
- radio-browser API: https://api.radio-browser.info/
- Music Player Daemon: https://www.musicpd.org/doc/
- Adafruit Speaker Bonnet guide: https://learn.adafruit.com/adafruit-speaker-bonnet-for-raspberry-pi
- TJC USART HMI editor and instruction set: http://wiki.tjc1688.com/
- NetworkManager `nmcli`: https://networkmanager.dev/docs/api/latest/nmcli.html

---

## Quick reference

```text
FLASH   Pi OS Lite 64-bit (Trixie), hostname WebRadio, SSH on. No full-upgrade/rpi-update/autoremove.
WIFI    wlan0 unavailable -> raspi-config nonint do_wifi_country US; rfkill unblock wifi
RADIOD  apt install mpd mpc python3-mpd; dpkg -i radiod_8.3_all.deb
        answers: rotary encoders / 40-pin / KY-040 no R1 / no display / Adafruit Speaker Bonnet
PINS    vol  +1(3.3V) GND9 SW7 DT10 CLK8      tune +17(3.3V) GND14 SW11 DT18 CLK16
        TJC  5V4 GND6 TX->33 RX->32 (UART4)    KY-040 + on 3.3 V ONLY
SCREEN  ForeverRadio.tft on FAT32 microSD -> screen slot -> "update successed!" -> remove card
ADDONS  ~/forever-radio: sudo bash install.sh
DIAL    edit dial.conf -> sudo ~/forever-radio/refresh_dial.sh   (auto: Sundays 04:00)
LOGS    journalctl -u forever-radio-watchdog -f | journalctl -u forever-radio-wifi-setup
WIFI UI no network 45 s -> join ForeverRadio-Setup -> http://10.42.0.1
```

*Companion guide for The Pi Stack Lab. Own the thing, don't rent it.*
