# The Forever Radio — Build a Raspberry Pi Internet Radio That Can't Be Bricked

The written companion to the video. We build an internet radio on a Raspberry Pi that runs on an **open, community-run station directory** (radio-browser) instead of a proprietary aggregator — so no company can ever shut it off the way Reciva did in 2021.

**Why this matters:** In 2021 the Reciva platform shut down its cloud directory and instantly bricked thousands of internet radios worldwide. The hardware was fine — but the "brains" lived on the company's server. This build puts the brains on open infrastructure nobody owns.

---

## The idea in one line

A radio station directory tells your device where each stream lives. Reciva's was private (one owner, one off-switch). **radio-browser.info** is open, free, community-maintained, and mirrored — so it can't be switched off out from under you.

---

## Parts list

- **Raspberry Pi** — any modern model; even a Pi Zero 2 W or a Pi 3/4 is plenty for audio. (Pi + power supply + microSD card.)
- **Audio out** — pick one:
  - Pi's 3.5mm jack (works, a bit thin) — Pi 4/earlier; Pi 5 has no jack.
  - **USB DAC** or **USB speaker** (cheap, easy, good).
  - **DAC HAT** (e.g. HiFiBerry-style) for the best sound.
- **Speaker** — powered speaker, or an amp + passive speaker.
- *(For the "real radio" feel — optional but recommended):*
  - **Small display** — I2C OLED/LCD or a small HAT screen (or an e-ink panel).
  - **Rotary encoder** (the "tuning knob") and/or a couple of push buttons.
  - **A case** — 3D-printed, a project box, or gut an old radio and refit it.

---

## Build it — Raspberry Pi OS + Bob Rathbone's radiod (the knob-and-screen path)

This is the path that gives you a **real physical knob + screen**, not just a web app. It's an open-source package built specifically for a Pi internet radio: **MPD** underneath, with built-in support for rotary encoders, buttons, and small displays. Project site: **bobrathbone.com** (it has an installer and a full **constructor's manual** — link both in the description).

> **Alternative (no physical controls):** if you only ever want to control it from a phone/browser, a ready-made music OS like **Volumio** or **moOde audio** stands up faster and plays web radio out of the box. But bolting a physical rotary encoder + LCD onto those is extra, fiddly work — so for a gut-and-refit with a real dial, use radiod below.

### 1. Flash Raspberry Pi OS
- Use **Raspberry Pi Imager**. Choose **Raspberry Pi OS** (Lite is fine — it runs headless).
- Before writing, open the **gear / "edit settings"** and set: a **hostname** (e.g. `radio`), **enable SSH**, your **Wi-Fi SSID + password**, and your **locale/region**. This one screen saves a lot of pain.
- Write the card, boot the Pi, then SSH in from your computer: `ssh <user>@<hostname>.local`.
- Update first: `sudo apt update && sudo apt full-upgrade`.

### 2. Enable your DAC / amp HAT — do this BEFORE the radio software
- Most HATs need a device-tree overlay line in `/boot/firmware/config.txt` (older OS: `/boot/config.txt`); the board maker gives the exact line (e.g. each HiFiBerry board has its own `dtoverlay=...`). Disable onboard audio if the maker says to.
- Reboot and confirm the card appears (`aplay -l`). Get sound working here first, so the radio software picks the right output when you configure it.

### 3. Install Bob Rathbone's radio package
- Follow his **current install instructions** and **constructor's manual** (links in the description). Versions change, so use his latest steps rather than a command pasted here.
- The package installs a service called **`radiod`** that runs the radio.

### 4. Run the configuration script
- The package includes an interactive **configuration script** that asks your **display type**, whether you have a **rotary encoder or push buttons**, and your **audio device**. Answer for your build; it writes the config for you.
- `radiod` is set to **start on boot**, so the finished radio powers straight into being a radio — no login, no keyboard.

### 5. Match the config to your wiring — the #1 gotcha
- Settings live in **`/etc/radiod.conf`**. That's where you set the **GPIO pins** for your rotary encoder and buttons, plus your **display type/address**.
- Enter the **exact pins you wired** (your reused Reciva encoder, or a KY-040). If the pins in the file don't match your wiring, the knob does nothing — the classic "it's broken" that isn't.
- Save, restart the service (`sudo systemctl restart radiod`), and the knob changes stations while the screen shows now-playing.

### 6. Load stations from the open directory (radio-browser)
- Build your **station list** from **radio-browser.info**: search by country / genre / language, grab each station's **stream URL**, and add it to radiod's station list (the package has a tool / web page for managing stations — see the manual).
- Your list is now plain open stream links stored **on the radio**, pulled from a directory nobody owns. That's the whole un-brickable point: no company in the middle, no private server.

---

## Put it in a case

- 3D-printed enclosure, a wooden project box, or **gut a dead/old radio and refit the Pi inside** (great on camera, and poetic if it's the bricked one).
- Mount the screen and knob on the front; bring the speaker out. Done.

---

## Option A — Gut-and-refit a dead radio (e.g. the bricked Reciva)

The most satisfying version of this build: strip the dead radio down to its shell + speaker + front-panel controls, and drop the Pi brain inside. What's dead is only the original controller board and display; the physical parts are reusable.

### Sound: use an amp HAT (DAC + amp in one)
The radio's built-in speaker is a **passive driver** — a DAC HAT alone (line-level only) won't drive it. Use an **amplifier HAT**, which has the DAC *and* the amp on one board and wires straight to the passive speaker. (An amp HAT *replaces* the plain DAC HAT — you don't use both.)

- **Small / right-sized for a little radio speaker (~3W):** Pimoroni **pHAT BEAT** (stereo, with VU-meter LEDs — fun on a radio), Pimoroni **Audio Amp SHIM** (mono 3W — a clean match for the Reciva's single speaker), Adafruit **Speaker Bonnet** (stereo 2×3W).
- **More power + powers the Pi from one supply:** **HiFiBerry Amp2** (~2×30W), **HiFiBerry Amp4 / Amp4 Pro** (Pi 4/5 form factor), **HiFiBerry Amp100** (~2×100W), or the official **Raspberry Pi DigiAMP+** (~2×35W, formerly IQaudio).
- The Reciva speaker is **mono** (one driver): with a stereo board, use one channel or sum to mono. A small amp (3–15W) is plenty; match the speaker's impedance (usually 4 or 8 Ω).
- HAT availability comes and goes — HiFiBerry and the official DigiAMP+ are the most reliably in stock.

### Reuse the original knobs and buttons
The Reciva's knobs and buttons are **dumb electromechanical parts** — none of the dead proprietary firmware is in them, so they're reusable. Only the controller board and display are junk.

- A **rotary encoder** outputs simple digital pulses the Pi reads on GPIO. Free it from the dead board (desolder, or tap its pins), identify the pins with a multimeter (two signal pins A/B, a common/ground, and two more for the push switch), then wire A + B + common to three GPIO pins and the switch to a fourth. The Pi's internal pull-ups handle the electrical side — encoders are passive, so there's no voltage/level worry on 3.3V GPIO.
- Plain **pushbuttons** (presets, power) are simple momentary switches — wire them to GPIO the same way.
- **Check: encoder vs potentiometer.** The Pi has **no analog input**, so it cannot read a potentiometer directly. The tuning/select knob is almost always a real encoder (reuse it). A **volume** knob is sometimes an analog **pot** — if so, either swap in an encoder, or do volume in software mapped to an encoder. Quick tell: an encoder clicks in detents and spins endlessly; a pot turns smoothly and stops at both ends.
- **Volume is done in software** on the Pi (the audio mixer), driven by encoder turns — you don't need a volume pot at all.

### Need to buy an encoder?
The standard hobby part is a **KY-040 rotary encoder module** — a small breakout with the encoder, pull-up resistors, a built-in push switch, and labeled pins (CLK, DT, SW, +, GND) that wire straight to the Pi. A few dollars, usually in multipacks. Sources: Amazon, Adafruit, SparkFun, Pimoroni, Mouser/DigiKey (name-brand), or AliExpress (cheap). The bare encoder underneath is typically an **EC11** if you want to buy just that and reuse a panel knob. KY-040 uses a standard D-shaft, so most knobs — possibly the Reciva's original — press right on, keeping the authentic look.

### Refit checklist
- Amp HAT sized to the speaker (mono is fine for the Reciva).
- One power supply if the amp HAT can also power the Pi (tidiest); otherwise Pi 5V + amp power.
- Reused encoder(s) + buttons wired to GPIO (or a KY-040 if the original was a pot).
- Small screen mounted behind an existing panel cutout for now-playing.
- Standoffs to hold the Pi, short speaker wire with the right connector, a few jumper wires.

---

## ⚠️ Honest note: commercial / business use

Running this at **home** — living room, workshop, garage — is all yours, no issue.

Running it in a **business** (shop, clinic, waiting room) as background music is different: **public performance of music in a business usually requires a proper music license.** That's exactly what paid background-music services sell — the licensing, not the music. Many internet stations are cleared for personal listening only. If you want this in a commercial space, look into proper licensing first. (This is the real-world catch behind the old "free Muzak alternative" idea.)

---

## Troubleshooting

**No sound / wrong output** → Set the correct audio output device in the OS settings (HDMI vs jack vs USB/DAC). On a DAC HAT, enable its overlay/driver per its instructions.
**Station won't play / buffers** → The stream URL may be dead or geo-blocked; pick another from radio-browser. Check the Pi's internet connection.
**Thin/quiet audio off the 3.5mm jack** → Expected; move to a USB DAC or DAC HAT.
**Knob skips or jumps stations** → Rotary encoder debounce; check wiring and the encoder step setting in the script.
**Screen blank** → Wrong I2C address or interface not enabled; enable I2C (raspi-config) and confirm the address.

---

## Quick reference

```text
IDEA:  station directory = where streams live.  Reciva's was private (bricked).
       radio-browser.info is OPEN + community-run + mirrored = can't be switched off.

BUILD (knob + screen path = Bob Rathbone radiod):
  1. Flash Raspberry Pi OS with Raspberry Pi Imager. In the gear/settings:
       set hostname, enable SSH, Wi-Fi SSID+password, locale. Boot, SSH in, apt update/upgrade.
  2. Enable your DAC/amp HAT FIRST (dtoverlay line in /boot/firmware/config.txt); reboot; aplay -l.
  3. Install Bob Rathbone's radio package (radiod) per his current install steps + manual (bobrathbone.com).
  4. Run its configuration script: answer display type, encoder/buttons, audio device.
  5. Edit /etc/radiod.conf: set the GPIO pins to MATCH your wiring + your display type. Restart radiod.
       (pins not matching wiring = knob does nothing — #1 gotcha)
  6. Build the station list from radio-browser.info (stream URLs) — stored locally on the radio.
  7. Case it up (3D print, project box, or refit the old radio).

  Alt (no physical knob): Volumio or moOde web OS — faster, but controlled by phone/browser only.

AUDIO:  amp HAT (DAC+amp) for a passive built-in speaker; USB DAC/DAC HAT beats the 3.5mm jack.

BUSINESS USE:  public music in a business needs a proper license — home use is fine.
```

---

*Companion guide for The Pi Stack Lab. Own the thing, don't rent it. Questions in the comments — I read all of them.*
