# The Forever Radio — Detailed Shot List & Filming Plan

**Rule:** every visual is real — your screen recordings, your filmed hardware, or your phone. No AI-generated b-roll.

## Capture settings
- Record 4K, deliver 1080p; screen recordings at 110–125% zoom so labels read on a phone.
- Blur any real IPs/network names in screen recordings.
- This is a STORY video — the hardware and your hands matter more than menus. Film the physical build lovingly.
- Lower-thirds only for the first ~90 seconds; keep it moving.

Legend — **Type:** CAM = you on camera · HW = filmed hardware/hands · SCR = screen recording · DIA = motion graphic · PHONE = filmed phone.

---

## COLD OPEN — 0:00–0:15  (film FIRST — the emotional hook)

**Shot 1 — The dead radio** · HW · ~9s
Capture: the old Reciva (or any dead internet radio) on the bench — power it on to a blank/frozen/error screen. Hold on the dead screen. If you still have YOUR actual bricked unit, this is the shot of the whole video.
On-screen text: **BRICKED — 2021**
Edit note: no music under it at first; let it feel like a loss.

**Shot 2 — "So I built one they can't"** · CAM/HW · ~6s
Capture: you on camera holding the dead radio, then gesturing to the new Pi radio you'll build. Deliver the promise line.

---

## THE BETRAYAL — 0:15–1:30

**Shot 3 — The story, to camera** · CAM · ~45s
Capture: you to camera telling the Reciva story — favorite radio, put them in waiting rooms, recommended them, then bricked overnight.
On-screen text: lower-third name/handle
Edit note: this is personal — let it breathe, don't rush.

**Shot 4 — How it worked (and failed)** · DIA · ~30s
Capture: simple motion graphic — radio → arrow → "COMPANY SERVER (the brains)" → a big X over the server → radio goes dark.
On-screen text: **BRAINS ON THEIR SERVER = THEIR OFF-SWITCH**

---

## THE PROMISE — 1:30–2:15

**Shot 5 — The finished radio tease** · HW · ~45s
Capture: quick, pretty beauty shots of the finished build you're about to make — knob turning, screen showing a station, speaker playing. (Shoot this after the build; place it here in the edit.)
On-screen text: **A RADIO THEY CAN'T SWITCH OFF**

---

## WHY THIS CAN'T BE BRICKED — 2:15–3:15  (the thesis)

**Shot 6 — Private vs open directory** · DIA · ~60s
Capture: motion graphic — left: "RECIVA — private directory, 1 owner, 1 off-switch." right: "radio-browser — open, community-run, mirrored everywhere." Our radio points at the open one.
On-screen text: **OPEN + COMMUNITY-RUN = NO OFF-SWITCH**
Edit note: this is the single most important idea — make it crisp.

---

## WHAT YOU NEED — 3:15–4:15

**Shot 7 — Parts laid out** · HW · ~60s
Capture: the parts on the bench — Pi, SD card, DAC/USB speaker, small screen, rotary encoder, a case. Pick each up as you name it.
On-screen text: **PI · DAC · SCREEN · KNOB · CASE**
Edit note: call the knob "the magic" here to set up the payoff later.

---

## FLASH THE PI — 4:15–5:15

**Shot 8 — Raspberry Pi Imager + the gear settings** · SCR · ~45s
Capture: in Raspberry Pi Imager, select **Raspberry Pi OS** → open the **gear / edit settings** → show setting a hostname, enabling SSH, entering Wi-Fi + region → write → boot → SSH in from the computer.
On-screen text: **DON'T SKIP THE GEAR: hostname · SSH · Wi-Fi**
Edit note: hold on the gear screen — it's the step that saves viewers hours.

---

## SET UP YOUR SOUND — 5:15–5:50

**Shot 9 — Enable the DAC / amp HAT (first!)** · SCR/HW · ~30s
Capture: the HAT seated on the Pi, then adding the board's `dtoverlay=` line to the Pi config, reboot, and `aplay -l` showing the card. Stress: do this BEFORE the radio software.
On-screen text: **ENABLE THE HAT FIRST**

---

## INSTALL THE RADIO SOFTWARE — 5:50–7:00

**Shot 10 — Install radiod + run the config script** · SCR · ~60s
Capture: installing Bob Rathbone's radio package per his current steps (flash his site/manual briefly), then running the **configuration script** and answering the questions — display type, rotary encoder vs buttons, audio device. End on `radiod` running.
On-screen text: **Bob Rathbone radiod · it ASKS, you answer**
Edit note: don't read commands aloud — show them on screen; the voiceover stays conversational.

---

## WIRE + CONFIGURE THE KNOB & SCREEN — 7:00–8:00  (the hero build + the gotcha)

**Shot 11 — Wire the screen + the knob** · HW · ~35s
Capture: clean macro of wiring the small I2C display (power, ground, SDA, SCL) and the rotary encoder (reused Reciva encoder, or a KY-040) to the Pi's GPIO.
On-screen text: **SCREEN + KNOB → GPIO**
Edit note: the "it's a real radio now" turn — shoot it lovingly.

**Shot 12 — /etc/radiod.conf: pins must match wiring** · SCR · ~30s
Capture: open `/etc/radiod.conf`, set the GPIO pin numbers to match how you wired the encoder/buttons, set the display type, save, then `sudo systemctl restart radiod`.
On-screen text: **PINS MUST MATCH YOUR WIRING (#1 gotcha)**
Edit note: call this out hard — wrong pins = a dead knob that looks like a broken build.

---

## LOAD STATIONS FROM THE OPEN DIRECTORY — 8:00–8:50  (the thesis made real)

**Shot 13 — Build the station list from radio-browser** · SCR · ~40s
Capture: search **radio-browser.info** by country/genre/language → grab stream URLs → add them to the radio's station list. Note they're stored locally, pulled from a directory nobody owns.
On-screen text: **radio-browser · YOUR LIST, STORED LOCALLY**

**Shot 14 — Case it up** · HW · ~20s
Capture: mounting it in the case — 3D print / project box / or refitting the old radio shell (bonus poetry if it's the bricked one). (Filmed during the build; placed here.)
On-screen text: **MAKE IT A REAL THING**

---

## LISTEN — 8:50–9:30  (the payoff)

**Shot 15 — Turn the knob, it plays** · HW · ~30s
Capture: hand turns the knob → screen updates to a new station → sound fills the room (show a little speaker-cone or room ambience). Linger.
On-screen text: **TURN IT. IT JUST PLAYS.**
Edit note: this is the emotional opposite of Shot 1. Pay it off.

**Shot 16 — Tune the world** · HW/SCR · ~15s
Capture: quickly spin through a few wildly different stations (a far-away country, a tiny local one).
On-screen text: **ANY STATION, ANYWHERE**

---

## HONEST NOTE — 9:30–10:30

**Shot 17 — The waiting-room caveat** · CAM · ~60s
Capture: you to camera — used to put these in businesses; home use is free and yours, but a business needs a proper music license. Be matter-of-fact, not preachy.
On-screen text: **HOME: YOURS · BUSINESS: GET A LICENSE**

---

## CLOSE — 10:30–11:05

**Shot 18 — Own it, don't rent it** · CAM/HW · ~20s
Capture: you on camera with the finished radio playing beside you; deliver the "still playing long after the company's a memory" line.
On-screen text: "Full build + links ↓"

**Shot 19 — End screen** · SCR/DIA · ~10s
Capture: the "build your own Netflix" / channel starter card center-frame while you invite them to the rest of the series; keep talking over it.
On-screen text: **OWN YOUR STUFF →**

---

## Capture checklist
- [ ] Shot 1 (the dead/bricked radio) filmed first — the emotional hook; use your real Reciva if you have it
- [ ] Shot 6 (private vs open directory) — the thesis graphic, crisp and clear
- [ ] Shot 15 (turn the knob → it plays) — the payoff that mirrors Shot 1
- [ ] Beauty shots (Shot 5) filmed AFTER the build, dropped into the promise section
- [ ] Any real IPs / network names blurred in screen recordings
- [ ] Screen + encoder wiring (Shot 11) shot in clean macro; /etc/radiod.conf pins matching the wiring (Shot 12) held long enough to read
- [ ] Honest licensing beat (Shot 17) included — don't cut it
- [ ] One 30–45s vertical cut earmarked for a Short (Shot 1 → Shot 15)
