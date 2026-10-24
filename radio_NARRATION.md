# They Bricked My Radio, So I Built a Raspberry Pi One They Can't — Narration

**Plot promise:** A radio that a company killed comes back to life on a Raspberry Pi, and no company can kill it again.
Target runtime: 10–11 minutes (~1,600 words). Voice: "Chuck" on Epidemic Sound. Written in ASD-STE100 for the steps.
Pronunciation: Reciva = "reh-SEE-vah" · Raspberry Pi = "raspberry pie" · radiod = "radio-dee" · M-P-D · G-P-I-O · K-Y oh-four-oh · T-J-C · S-S-H · Wi-Fi · radio-browser = "radio browser" · Tangent Quattro = "TAN-jent KWAH-troh".
Do not read the `[on screen: …]` notes aloud.

— — —

COLD OPEN

[on screen: the Tangent Quattro on the bench, dark. A hand turns the knob. The 3.5-inch screen lights up: station name in amber, song title, volume bar. Music starts. Text: "BRICKED IN 2021 → PLAYING AGAIN"]

In 2021, a company switched off a server, and this radio died.

Today it plays again. And this time, no company can switch it off.

[on screen: quick cuts — knob turning through "Genre Jazz", "Country Japan", "Decade 80s"; the phone joining "ForeverRadio-Setup"]

Inside is a Raspberry Pi. It finds stations in an open directory that nobody owns. Two knobs, a real screen, and its own speaker.

[on screen: the white, dead 1.8-inch screen; the terminal line "stream stalled (silence), reconnecting"]

It was not easy. I killed one screen. And some stations went silent until I taught the radio to fix itself. I show you all of it, so you do not lose the same afternoon.

— — —

WHY IT DIED

This is a Tangent Quattro. Inside, it used a Reciva module. Reciva ran the station directory for thousands of radios like this one.

In 2021, Reciva shut that directory down. The hardware was perfect. But the radio asked one company's server where every station was. When the server stopped, every radio stopped.

I used to recommend these radios. So this one is personal.

— — —

WHY THIS ONE CANNOT BE BRICKED

This build asks a different directory. It is called radio-browser. Volunteers run it. The data is free, and copies run on many servers. No single company owns it.

Every week, the radio gets a fresh station list from radio-browser and keeps it on its own memory card. If the directory goes away one day, the radio keeps its last list and keeps playing.

The software is also open. It is Bob Rathbone's radio package, called radiod, on top of a music player called M-P-D. Nothing in this radio needs a company's permission.

— — —

WHAT YOU NEED

Here is the parts list. Exact models are in the guide.

A Raspberry Pi 5, a power supply, and a memory card.

An Adafruit Speaker Bonnet. It is a small amplifier board. It drives the radio's original speaker directly.

Two K-Y oh-four-oh rotary encoders. One is the volume knob. One is the tuning knob. Both also push in, like buttons.

A 3.5-inch T-J-C serial screen. Mine came out of an old ham radio hotspot.

A G-P-I-O expansion board, so the Speaker Bonnet and the wires can share the Pi's pins. And some jumper wires.

— — —

FLASH THE PI

Open Raspberry Pi Imager. Select Raspberry Pi 5. Select Raspberry Pi OS Lite, sixty-four-bit.

In the settings, set the hostname to WebRadio. Set a user and a password. Turn on S-S-H. Type your Wi-Fi name and password.

Write the card. Put it in the Pi. Turn it on.

On my Pi, Wi-Fi did not start. The Wi-Fi status said "unavailable". The cause was the Wi-Fi country. It was not set. One command sets the country, and the guide has it. If your Wi-Fi does not start, try this first.

Connect with S-S-H. Update the Pi with apt upgrade. Do not use full-upgrade. Bob Rathbone warns that it can break the radio software on this version of the OS.

— — —

INSTALL THE RADIO SOFTWARE

Install M-P-D. Then download Bob's radiod package and install it. The commands are in the guide.

The installer asks questions. Here are my answers.

User interface: rotary encoders.

Wiring: the forty-pin version.

Encoder type: K-Y oh-four-oh, with no resistor R-one. This choice works on every K-Y oh-four-oh board.

Display: no display, for now. We add the screen later.

Audio: Adafruit Speaker Bonnet.

Reboot. The radio plays from the Speaker Bonnet.

— — —

WIRE THE KNOBS

Turn off the Pi before you connect any wire.

Each K-Y oh-four-oh has five pins: ground, plus, switch, D-T, and C-L-K. The guide has a table with each pin.

One rule is very important. Connect the plus pin to three point three volts. Never connect it to five volts. Five volts goes straight into the Pi's G-P-I-O pins.

Turn on the Pi. Open radio-config, and run the rotary encoder test. Turn each knob and push each knob. Each action shows on the screen as an event. Mine worked the first time.

— — —

THE SCREEN — AND THE ONE I KILLED

radiod has no driver for these small color screens. So I wrote one.

My first screen was a 1.8-inch board. I told myself pin one was at one end of the connector. It was at the other end. I connected it backwards. Five volts went into its ground pin, and the screen died.

[on screen: the white screen; multimeter on the regulator]

Here is the lesson. Before you power a new board, find its power pins with a multimeter. Do not trust a pin diagram from memory.

So I used my T-J-C screen. This screen has its own small computer. The Pi sends short text commands on two wires, and the screen draws the text.

But the screen needs one file with fonts. You make that file one time, in T-J-C's editor. I already made it. It is in my repository. You copy it to a micro S-D card, put the card in the screen, and turn it on. The screen says "update successed". Then remove the card.

The Pi draws everything else: the station, the song, the time, the playlist, the bit rate, and the volume bar. In the corner, it shows "LAN" or "WiFi".

Then the screen stopped. It showed only white. I tested every speed. Nothing worked. The cause was one loose jumper wire. Check your wires before you check your code.

— — —

THE ADD-ONS — ONE COMMAND

I put all the extras in one folder, with one install script. Copy the folder to the Pi. Run the script with sudo.

The script installs the screen driver. It builds your station dial from radio-browser. It adds a weekly refresh, a watchdog, and Wi-Fi setup from your phone. I explain each one now.

— — —

THE STATION DIAL

radiod shows playlists in alphabetical order. It has no sub-menus. So I group the playlists by name.

All the countries start with "Country". All the decades start with "Decade". All the genres start with "Genre".

Push the tuning knob until the screen says "Input Source". Turn the knob. You go through Country Brazil, Country Japan, Decade Eighties, Genre Jazz, and more. Push the knob to select.

To change the dial, edit one text file. Each line is a name and a radio-browser search. Every Sunday morning, the radio gets the newest stations for each line.

— — —

THE WATCHDOG

Some stations went silent. The screen still said "playing". But no sound came out.

The log showed the cause. The station's server stopped sending audio. M-P-D played silence and did not try again. When I turned the knob away and back, the station connected again.

So the radio now does that itself. A small watchdog checks every five seconds. After fifteen seconds of silence, it connects the station again. One news station drops every ten minutes. Now I almost do not notice it.

— — —

WI-FI FROM YOUR PHONE

A radio must work in a new place. This screen is not a touch screen, so you cannot type a password on it.

So when the radio finds no network, it makes its own Wi-Fi network. The screen tells you its name: ForeverRadio-Setup. Join it on your phone. A setup page opens. Select your Wi-Fi. Type the password. Select Connect.

The screen says "Connected", and the music starts again.

A network cable always works too. Connect the cable, and the radio uses it.

— — —

INTO THE CASE

Now the Pi goes into the radio that died.

Remove the old Reciva board. Keep the case, the speaker, and the knob holes. Connect the Speaker Bonnet to the original speaker. Put the encoders through the original knob holes. Cut a window for the screen.

[on screen: the cut window; the screen behind it; the knobs on the front]

The old radio looks almost the same from the front. But now it has a Raspberry Pi inside.

— — —

LISTEN

[on screen: hand turns the tuning knob; the screen changes; sound fills the room]

Turn the knob. The station changes. The screen updates. The speaker plays.

Japan. Brazil. A jazz station somewhere in Europe. All on a radio that a company said was dead.

— — —

ONE HONEST NOTE

I used to put these radios in waiting rooms. At home, this radio is all yours. In a business, music usually needs a license. That is what paid background-music services sell. So check the license before you use this in a shop or a clinic.

— — —

CLOSE

This radio died once because its brain lived on someone else's server. Now the brain sits inside the radio, and the station list comes from a directory that nobody owns.

The guide, the screen file, and the install script are linked below.

Did a company ever switch off something you bought? Tell me in the comments. I read all of them.
