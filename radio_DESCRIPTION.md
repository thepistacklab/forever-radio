# Title (locked)
**They Bricked My Radio, So I Built a Raspberry Pi One They Can't** (vidIQ 94)

**Thumbnail concept:**

- **Image:** the dark, dead radio (Reciva-era screen) beside the same radio glowing with the new amber TJC screen.
- **Text:** **CAN'T BRICK THIS**
- **Must match:** shot 1 of the video (dark radio → knob turn → screen lights up).

> Only the text between the "=====" lines counts toward YouTube's 5,000-character limit. Don't use the `<` or `>` characters in it: YouTube rejects them.
> Replace [GUIDE LINK] and [REPO LINK] before you publish.

============================ PASTE-READY DESCRIPTION ============================

In 2021 Reciva switched off its station directory, and thousands of internet radios died overnight, including my Tangent Quattro. The hardware was fine. The brains lived on a company's server. So I put a Raspberry Pi inside it. Now it plays thousands of stations from an open directory nobody owns, with two real knobs, a 3.5" screen and its original speaker. No company can switch this one off.

📄 Full written guide (every command and pin): [GUIDE LINK]
💾 Screen file, driver and one-command installer: [REPO LINK]

🔧 THE BUILD
• Raspberry Pi 5 + Raspberry Pi OS Lite 64-bit (Trixie)
• Bob Rathbone's radiod 8.3 on MPD (open source)
• Adafruit Speaker Bonnet driving the radio's original speaker
• 2× KY-040 rotary encoders: volume + tuning (push for mute and menus)
• TJC 3.5" serial screen (TJC4832T135), rescued from a ham radio hotspot
• Stations from radio-browser.info, rebuilt every week and stored on the radio

🧩 WHAT I ADDED (one install script)
• A screen driver: the Pi draws the station, song, playlist, volume bar and LAN/WiFi status
• A grouped station dial: Country, Decade, Genre, News, refreshed every Sunday
• A watchdog: stations that go silent reconnect by themselves
• Wi-Fi setup from your phone: no network, so the radio makes a setup hotspot

💥 WHAT BROKE (so you skip it)
• I wired a 1.8" screen backwards and killed it. Find power pins with a multimeter first.
• Wi-Fi said "unavailable": the Wi-Fi country was not set
• A white, dead-looking screen was one loose jumper wire
• Stations said "playing" but were silent: the watchdog fixes it
• KY-040 + pin goes to 3.3 V, never 5 V

⏱️ CHAPTERS
0:00 Bricked in 2021, playing again
0:45 Why the radio died
1:30 Why this one can't be bricked
2:15 What you need
3:00 Flash the Pi
3:45 Install radiod + Speaker Bonnet
4:40 Wire the knobs
5:30 The screen (and the one I killed)
7:00 One-command add-ons
7:20 The station dial
8:00 The watchdog
8:40 Wi-Fi from your phone
9:20 Into the case
9:50 Listen
10:15 One honest note

⚠️ BUSINESS USE
At home it's all yours. Playing music in a business (shop, clinic, waiting room) usually needs a music license. Check before you use it commercially.

📚 SOURCES & DOCUMENTATION
Bob Rathbone radiod + Constructor's Manual: https://bobrathbone.com/raspberrypi/pi_internet_radio.html
radio-browser: https://www.radio-browser.info/
Music Player Daemon: https://www.musicpd.org/
Adafruit Speaker Bonnet: https://learn.adafruit.com/adafruit-speaker-bonnet-for-raspberry-pi
TJC USART HMI: http://wiki.tjc1688.com/
NetworkManager nmcli: https://networkmanager.dev/

Did a company ever switch off something you bought? Tell me in the comments. I read all of them.

#raspberrypi #internetradio #reciva

================================================================================

## Tags (paste into the tag field)
raspberry pi internet radio, reciva, reciva shutdown, reciva radio fix, bricked internet radio, tangent quattro, diy internet radio, raspberry pi 5 project, raspberry pi radio, bob rathbone radiod, radiod, mpd raspberry pi, radio-browser, adafruit speaker bonnet, ky-040 rotary encoder, nextion display raspberry pi, tjc display, rotary encoder radio, right to repair, own your hardware, homelab
