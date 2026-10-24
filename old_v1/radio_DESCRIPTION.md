# Title options (vidIQ-scored)
1. **Build a Forever Internet Radio: Never Get Bricked Again** — 91 (recommended)
2. Why I Built My Own Radio: Anti-Obsolescence Raspberry Pi Project — 90
3. The Last Internet Radio You'll Ever Need: Raspberry Pi Build — 90
4. Reciva Shutdown? Build a Better Raspberry Pi Internet Radio — 84 (best for catching Reciva refugees in search)

> Recommended play: use #1 as the title, and put "Reciva" in the first line, the thumbnail, and the tags to
> catch both the broad audience and people still searching the shutdown.
> Only text between the "=====" lines counts toward YouTube's 5,000-char limit. No `<` or `>` (illegal in YouTube descriptions); menus use "→".

============================ PASTE-READY DESCRIPTION ============================

In 2021, the Reciva platform shut down its servers and instantly bricked thousands of internet radios worldwide — including mine, and ones I'd recommended to businesses. The hardware was perfect; the problem was the brains lived on a company's server. So I built one they can never switch off. This is a Raspberry Pi internet radio that runs on an OPEN, community-run station directory — any station in the world, a real tuning knob, great sound, and no company holding the off-switch.

📄 Full written build guide (parts, wiring, links): [GIST LINK]

🧠 WHY THIS ONE CAN'T BE BRICKED
A station directory tells the radio where each stream lives. Reciva's was private — one owner, one off-switch. This build uses radio-browser (open, free, community-maintained, mirrored), so no single company can shut it down. Own the thing, don't rent it.

🛒 WHAT YOU NEED
• Raspberry Pi (any modern model — even a Pi Zero 2 W) + power + microSD
• Audio out: a USB DAC or DAC HAT (much better than the 3.5mm jack) + a powered speaker
• For the "real radio" feel: a small I2C screen + a rotary encoder (tuning knob)
• A case: 3D-printed, a project box, or gut an old radio and refit it

🔧 THE BUILD (the knob + screen path = Bob Rathbone's radiod)
Flash Raspberry Pi OS with the Pi Imager (set hostname, SSH, and Wi-Fi in the gear menu). Enable your DAC/amp HAT. Install Bob Rathbone's radio package (radiod) per his current installer + manual, run its config script (it asks your display, encoder/buttons, and audio device), then set your GPIO pins in /etc/radiod.conf to match your wiring. Prefer no physical knob? Volumio or moOde is a faster web-only route.

📻 POINT IT AT THE OPEN DIRECTORY
Add the radio-browser source, search by country / genre / language, and save favorites as presets. Presets live on YOUR radio, not on anyone's server.

🎛️ MAKE IT A REAL RADIO
Wire a small display + a rotary encoder to the Pi's GPIO: knob = change station, screen = now playing. Everyone knows how to turn a knob — that's what makes it the kitchen radio instead of a Pi project. (Exact wiring in the guide.)

⚠️ HONEST NOTE — BUSINESS USE
Home use is all yours. But playing music publicly in a business (shop, clinic, waiting room) usually needs a proper music license — that's what paid background-music services actually sell. Build this for home freely; for a business, sort out licensing first.

⏱️ CHAPTERS
0:00 The day my radio got bricked
0:15 What Reciva did (and why it stung)
1:30 What we're building
2:15 Why THIS one can't be shut off
3:15 What you need
4:15 Flash the Pi (Raspberry Pi OS)
5:15 Set up your sound (DAC/amp HAT)
5:50 Install the radio software (Bob Rathbone radiod)
7:00 Match it to your knob and screen (the config)
8:00 Load stations from the open directory
8:50 Listen
9:30 Honest note: the waiting-room story
10:30 Own it, don't rent it

📺 MORE FROM THE PI STACK LAB
Own-your-stuff builds on one Raspberry Pi — media, photos, storage, and more. Start with the "build your own Netflix" video to see where this all goes.

Questions in the comments. I read all of them.

================================================================================

## Tags (paste into the tag field)
raspberry pi internet radio, internet radio, reciva, reciva shutdown, diy internet radio, how to make internet radio, raspberry pi music player, radio-browser, volumio, moode audio, raspberry pi radio, mpd raspberry pi, rotary encoder radio, raspberry pi project, self hosted, homelab, right to repair, planned obsolescence, raspberry pi 5, own your hardware, streaming radio diy
