# They Bricked My Radio, So I Built a Raspberry Pi One They Can't — Shot List

**Plot promise:** A radio that a company killed comes back to life on a Raspberry Pi, and no company can kill it again.
**Rules:**

- **Faceless channel:** hands and hardware, no talking head.
- **Every visual is real:** your footage and screen recordings. No AI b-roll.
- **Every on-screen text is short enough to read muted.**
- **No full-screen chapter cards in the first 90 seconds.** Use moving lower-thirds.

**Type legend:** HW = filmed hardware/hands · SCR = screen recording · PHONE = filmed phone screen · DIA = simple motion graphic.

## Capture settings

- Film 4K, deliver 1080p. Screen recordings at 110–125% zoom, so text reads on a phone.
- **Blur:** your Wi-Fi name (SouthernCommand_2G), passwords and IP addresses. Blur the setup page's network list, or film it with a neighbour-free list.
- **Screen glare:** film the TJC screen slightly off-axis, with the room lights low. Lock exposure, or the amber text clips.
- **Already captured:** the failure moments as photos (dead white 1.8" screen, red test screen, first live screen, wrapped title). Re-shoot them on video where you can.

---

## COLD OPEN — 0:00–0:45 (film LAST, after the radio is in the case)

| # | Type | Shot | On-screen text |
|---|---|---|---|
| 1 | HW | **The money shot (0–5 s).** The Quattro on the bench, dark. A hand turns the knob, the screen lights up (amber station, title, volume bar), music starts. It must make sense muted. | **BRICKED IN 2021 → PLAYING AGAIN** |
| 2 | HW | Fast cuts: tuning knob turning through *Genre Jazz → Country Japan → Decade 80s* on the screen. | *Any station. Open directory.* |
| 3 | PHONE | The phone's Wi-Fi list with **ForeverRadio-Setup**; a tap. | *Wi-Fi from your phone* |
| 4 | HW | The dead 1.8" screen glowing white. Hard cut. | **I KILLED THIS ONE** |
| 5 | SCR | Terminal: `stream stalled (silence), reconnecting`. | *It fixes itself* |

---

## WHY IT DIED — 0:45–1:30

| # | Type | Shot | On-screen text |
|---|---|---|---|
| 6 | HW | The Quattro front, powered, showing the dead Reciva display (frozen or error screen, if it still powers). Slow push-in. | lower-third: *Tangent Quattro · Reciva inside* |
| 7 | DIA | Radio → arrow → "RECIVA SERVER" → server goes dark → radio goes dark. | **THEIR SERVER = THEIR OFF-SWITCH** |

## WHY THIS ONE CAN'T BE BRICKED — 1:30–2:15

| # | Type | Shot | On-screen text |
|---|---|---|---|
| 8 | DIA | Left: one Reciva server. Right: radio-browser with many mirrors. The Pi radio points right, and the list is stored on the radio's SD card. | **OPEN DIRECTORY · LIST STORED ON THE RADIO** |
| 9 | SCR | radio-browser.info search page (tag: jazz). | *radio-browser.info — volunteer-run* |

## WHAT YOU NEED — 2:15–3:00 (parts after the payoff)

| # | Type | Shot | On-screen text |
|---|---|---|---|
| 10 | HW | Overhead parts layout. Pick up each part as it's named: Pi 5, Speaker Bonnet, 2 KY-040s, TJC screen, expansion board, jumpers. | **PI 5 · SPEAKER BONNET · 2 KNOBS · 3.5" SCREEN** |
| 11 | HW | The TJC screen still showing the old **MMDVM** hotspot layout. | *Rescued from a ham radio hotspot* |

## FLASH THE PI — 3:00–3:45

| # | Type | Shot | On-screen text |
|---|---|---|---|
| 12 | SCR | Raspberry Pi Imager: Pi 5 → Pi OS Lite 64-bit → settings (hostname, SSH, Wi-Fi). | **Pi OS Lite 64-bit** |
| 13 | SCR | Real failure: `wlan0:unavailable`, then the country fix, then `connected`. | **WI-FI "UNAVAILABLE"? SET THE COUNTRY** |
| 14 | SCR | `sudo apt -y upgrade`. Cross-out graphic over "full-upgrade". | **upgrade ✓ · full-upgrade ✗** |

## INSTALL RADIOD — 3:45–4:40

| # | Type | Shot | On-screen text |
|---|---|---|---|
| 15 | HW | Speaker Bonnet seated on the expansion board; speaker wires into its terminals. | *Speaker Bonnet = DAC + amp* |
| 16 | SCR | `dpkg -i radiod_8.3_all.deb`, then installer screens: Rotary encoders → 40-pin → **KY-040 no R1** → No display → **Adafruit Speaker Bonnet**. | Answers as captions |
| 17 | SCR | `aplay -l` showing **sndrpihifiberry**; `mpc status` **[playing]**. Sound starts. | **FIRST SOUND** |

## WIRE THE KNOBS — 4:40–5:30

| # | Type | Shot | On-screen text |
|---|---|---|---|
| 18 | HW | Macro: KY-040 pin labels (GND + SW DT CLK). | — |
| 19 | HW | Macro: wiring `+` to pin 1. Graphic: red X on pin 2/4 (5 V). | **+ TO 3.3 V ONLY** |
| 20 | SCR+HW | Split: radio-config encoder test events scrolling, and a hand turning and pushing the knob. | **EVERY CLICK = AN EVENT** |

## THE SCREEN — AND THE ONE I KILLED — 5:30–7:00 (the story section)

| # | Type | Shot | On-screen text |
|---|---|---|---|
| 21 | HW | The 1.8" board: back photo (CD4050, regulator), the J1 label, the pins. | *Pin 1 was at the OTHER end* |
| 22 | HW | Multimeter on the regulator: 2.3 V where 3.3 V should be. | **2.3 V = DEAD** |
| 23 | DIA | "Find power pins with a multimeter BEFORE power." | **MEASURE FIRST** |
| 24 | SCR | USART HMI: font generator (ASCII, 24/32/40), Compile → "0 errors". Fast, 5 seconds. | *One-time: fonts only* |
| 25 | HW | microSD into the TJC; screen shows **"update successed!"** | **ONE FILE · DONE** |
| 26 | HW | Real failure: white screen. Hand finds the loose jumper on pin 33. Re-seat → the screen turns **red** (colour test). | **IT WAS A LOOSE WIRE** |
| 27 | HW | First live screen: Arabella, Wham!, volume bar. Then the all-caps title scrolling cleanly. | **THE PI DRAWS THE SCREEN** |
| 28 | HW | Close-up of the **LAN / WiFi** corner indicator. | — |

## ONE-COMMAND ADD-ONS — 7:00–7:20

| # | Type | Shot | On-screen text |
|---|---|---|---|
| 29 | SCR | `cd ~/forever-radio && sudo bash install.sh`, sped up → "Forever Radio add-ons installed." | **ONE COMMAND** |

## THE STATION DIAL — 7:20–8:00

| # | Type | Shot | On-screen text |
|---|---|---|---|
| 30 | HW | Push the tuning knob → "Input Source" → turn through Country… / Decade… / Genre… → push. | **GROUPED BY NAME** |
| 31 | SCR | `dial.conf` in nano: highlight `Genre Jazz | tag=jazz limit=40`. | *Edit one line = new playlist* |

## THE WATCHDOG — 8:00–8:40

| # | Type | Shot | On-screen text |
|---|---|---|---|
| 32 | SCR | Real failure: `mpc status` **[playing]**, plus mpd.log `Decoder is too slow; playing silence`. | **"PLAYING" — BUT SILENT** |
| 33 | SCR | `journalctl -u forever-radio-watchdog -f` with "reconnecting" lines; audio returns. | **IT FIXES ITSELF** |

## WI-FI FROM YOUR PHONE — 8:40–9:20

| # | Type | Shot | On-screen text |
|---|---|---|---|
| 34 | HW | Radio screen: "No network – WiFi setup / ForeverRadio-Setup". | — |
| 35 | PHONE | Join ForeverRadio-Setup → setup page → select network → password (blurred) → Connect. | **NO TOUCH SCREEN NEEDED** |
| 36 | HW | Radio screen: "Connecting… Connected!" → music. | — |

## INTO THE CASE — 9:20–9:50 (film when the refit happens)

| # | Type | Shot | On-screen text |
|---|---|---|---|
| 37 | HW | Opening the Quattro; lifting out the dead Reciva board. | *The dead brain comes out* |
| 38 | HW | Speaker label macro (ohms); bonnet wired to the original speaker. | — |
| 39 | HW | Cutting the screen window; screen mounted behind it; KY-040s through the original knob holes. | — |

## LISTEN — 9:50–10:15 (the payoff, mirrors shot 1)

| # | Type | Shot | On-screen text |
|---|---|---|---|
| 40 | HW | Hand turns the knob; station changes; sound fills the room. Hold. | **TURN IT. IT PLAYS.** |
| 41 | HW | Quick spin: Japan → Brazil → a European jazz station. | **ANY STATION, ANYWHERE** |

## HONEST NOTE + CLOSE — 10:15–10:50

| # | Type | Shot | On-screen text |
|---|---|---|---|
| 42 | HW | The radio playing on a kitchen shelf. | **HOME: YOURS · BUSINESS: GET A LICENSE** |
| 43 | DIA | End screen: guide + repo links, next video. | *Guide · screen file · install script ↓* |

---

## Capture checklist

- [ ] **Shot 1 (cold-open money shot)** filmed in the finished case. It works muted, and matches the thumbnail.
- [ ] Shots 2–5 (front-loaded quality) cut into the first 45 seconds.
- [ ] The real failures, as video where possible:
  - [ ] the 1.8" white screen (shot 4)
  - [ ] 2.3 V on the meter (shot 22)
  - [ ] the loose-wire white screen (shot 26)
  - [ ] "playing but silent" (shot 32)
  - [ ] `wlan0 unavailable` (shot 13)
- [ ] Wi-Fi name, passwords and IPs blurred (shots 13, 35).
- [ ] The phone setup flow (shots 34–36) filmed in one take, phone and radio both in frame if you can.
- [ ] The case refit (shots 37–39) filmed during the build.
- [ ] Payoff (shot 40) mirrors shot 1.
- [ ] Short: shots 1 → 4 → 40, reframed 9:16.
