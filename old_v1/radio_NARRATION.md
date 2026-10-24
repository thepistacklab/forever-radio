# The Forever Radio — Narration Script (conversational)
Target runtime: 10–12 minutes. Spoken, warm, like talking a friend through it over coffee. Personal — this one's your story.
Pronunciation notes: Reciva = "reh-SEE-vah", Raspberry Pi = "raspberry pie", radio-browser = "radio browser", MPD = "M-P-D", DAC = "dack" (digital-to-analog converter), HiFiBerry = "hi-fi-berry", Volumio = "vo-LOO-mee-oh", moOde = "mode", GPIO = "G-P-I-O", OTA n/a.

— — —

**COLD OPEN (0:00–0:15)**

This was my favorite thing in the house. An internet radio — I'd wake up to it, I put them in waiting rooms, I told people it was the best free alternative to those paid background-music services. And then one morning in 2021, it just… stopped. Not broke. The company flipped off a server, and every one of these radios on earth turned into a paperweight at the same instant. Mine. The ones I'd recommended. All of them. So I built one they can never do that to again. Let me show you.

— — —

**THE BETRAYAL (0:15–1:30)**

Let me tell you what actually happened, because it still kind of makes me mad. The brand was Reciva. For years they ran the thing that made these radios work — a big directory in the cloud that knew where every station lived. The radio itself was just a dumb little screen and a speaker; all the brains were on their server. And that was fine… right up until it wasn't.

In 2021 they shut that directory down. And here's the part that stings: there was nothing wrong with the radios. The hardware was perfect. But because the brains lived on somebody else's computer, the second they turned it off, thousands of perfectly good radios became junk. No warning that mattered, no fix, no "here's how to keep yours working." Just — done.

And I felt that one twice over, because I'd been the guy telling friends and little businesses, "get one of these, it's great, it's free." So when they bricked, that was on my recommendation. That's the day I stopped trusting any gadget whose brain lives on a company's server. And it's the whole reason this channel exists.

— — —

**THE PROMISE (1:30–2:15)**

So here's what we're building today, and why it's different. A Raspberry Pi internet radio — looks like a radio, works like a radio, you turn a knob and stations change — but with one crucial difference under the hood: there is no company in the middle. Nobody owns the switch that can turn it off.

By the end of this you'll have a little radio appliance playing any of tens of thousands of stations from around the world, and the day some corporation decides to shut their service down? Yours just keeps playing. That's the promise. Let me show you how it's possible, because the "how" is the whole point.

— — —

**WHY THIS ONE CAN'T BE BRICKED (2:15–3:15)**

Here's the key idea, and if you take one thing from this video, take this. The reason the Reciva died is that it depended on one company's private directory. One server, one owner, one off-switch.

What we're using instead is an open, community-run directory called radio-browser. Think of it like Wikipedia, but for radio stations — it's maintained by volunteers, the data is free and public, anyone can mirror it, and no single company owns it. So our radio asks that open directory "where's this station?" instead of asking some corporation's private server.

And that's the whole trick. Because it's open and community-run, there's no boardroom that can vote to shut it off and brick your radio. Even if one copy of it went down, the data's mirrored all over. That is the difference between something you own and something you're just renting until a company changes its mind.

— — —

**WHAT YOU NEED (3:15–4:15)**

Let me keep the shopping list honest and short.

The brain is a Raspberry Pi — nothing fancy, even a modest one is plenty for playing audio. You need power and an SD card, like always.

For sound, you've got choices. The Pi's headphone jack works in a pinch, but it sounds a little thin, so I'd add a cheap USB speaker or — if you care about sound like I do — a little DAC, a digital-to-analog converter, either a HAT that sits right on the Pi or a USB one. That's what takes it from "computer noise" to "actually enjoyable."

And then the part that makes it feel like a radio instead of a web page: a small screen, and a knob or a couple of buttons. That's optional — you can run the whole thing from your phone — but honestly the knob is the magic. Turning a physical dial to change the station is the whole vibe. I'll show you both ways.

— — —

**FLASH THE PI (4:15–5:15)**

Let me name exactly what we're loading, because this is the part that actually matters. The base is just Raspberry Pi OS — the plain one. On top of it we install a free, open-source package built specifically for this: Bob Rathbone's Raspberry Pi Radio. It's been around for years, it runs on a music player called MPD underneath, and — here's why we're using it — it already knows how to drive a physical knob and a little screen. That's the piece that turns this into a real radio instead of a web page.

So, first, flash the card. Open the Raspberry Pi Imager, choose Raspberry Pi OS, and — do not skip this — click the little gear, the "edit settings," before you hit write. In there you set a hostname so you can find the Pi, switch on SSH so you can log into it from your computer, and type in your Wi-Fi name and password and your region. That one screen saves you a world of headache. Write the card, pop it in the Pi, power it up.

Give it a minute to boot, then from your computer you log in over SSH — the address is just that hostname you picked, dot local. First thing, run the update-and-upgrade to get it current. The exact commands are in the guide — I'm not going to make you watch me type.

— — —

**SET UP YOUR SOUND (5:15–5:50)**

Quick one, but do it in this order. Tell the Pi about your audio board before you install the radio software. If you went with a DAC or amp HAT like we talked about, you enable it so sound comes out of that board instead of the Pi's little jack. On most HATs that's a single line added to the Pi's config file — the board's maker gives you the exact line, and I've got the common ones in the guide. Reboot, and your good audio path is live. Get this right first so the radio software sees the correct output when we set it up.

— — —

**INSTALL THE RADIO SOFTWARE (5:50–7:00)**

Now the heart of it — installing Bob Rathbone's radio package. You grab it by following his current install instructions; he keeps an installer and a full constructor's manual on his site, and I'll link both down in the description. Follow his current steps rather than something I read out today, because versions move and I want you on the latest.

Once it's installed, you run its configuration script, and this is the part I genuinely love: it just asks you questions. What kind of display do you have? Do you have a rotary encoder, or push buttons? Which audio device? You answer for your build, and it writes the settings for you — no guesswork. The program that runs the whole radio is a service called radiod, and once it's set up it starts on its own every time the Pi powers on. So your finished radio just boots straight into being a radio. No screen, no keyboard, no logging in — plug it in and it plays.

— — —

**MATCH IT TO YOUR KNOB AND SCREEN (7:00–8:00)**

Here's where your actual wiring meets the software, and it's the number-one thing people trip on, so listen up. All the radio's settings live in one file — it's called radiod-dot-conf. That's where you tell it which GPIO pins your knob and your buttons are really connected to, and what kind of screen you've got.

So whatever pins you used when you wired up that reused Reciva encoder — or your KY-040 — you put those exact pin numbers into that config file. They have to match your wiring, or you'll turn the knob and nothing happens and you'll swear it's broken when it isn't. Set your display type in that same file, save it, restart radiod — and now the knob changes stations and the screen shows what's playing. The guide spells out the exact settings. You do it once and forget it.

And here's why all this fuss over a knob is worth it: my wife is never going to open a web app to change the radio. Nobody's grandma is. But everybody on earth knows how to turn a knob. The moment this thing has a real dial and a screen, it stops being "my Raspberry Pi project" and becomes "the radio in the kitchen" that anyone can walk up and use.

— — —

**LOAD STATIONS FROM THE OPEN DIRECTORY (8:00–8:50)**

Last piece — and this is the one that makes the whole thing un-brickable. The radio plays from a station list, and we build that list from the open community directory, radio-browser. You search it for the stations you want — by country, by genre, by language — grab their stream links, and load them into your radio's station list. There's a simple way to do that right in the package, and it's in the guide.

And that's the payoff of the entire design: your stations are now just a plain list of open stream links, sitting on your radio, pulled from a directory nobody owns. No company in the middle, no private server. That is the thing the Reciva could never give me — these don't vanish when somebody in a boardroom has a bad quarter.

— — —

**LISTEN (8:50–9:30)**

Let's turn it on. Give the knob a turn — station changes, the screen updates, and there's the sound filling the room. That right there is the payoff. A radio you built, playing anything in the world, that answers to you and nobody else.

Spend a minute just tuning around. Honestly this is the part where I lost an afternoon the first time — there's something genuinely fun about spinning through little stations from the other side of the planet on a thing you made with your own hands.

— — —

**THE HONEST PART — THE WAITING-ROOM STORY (9:30–10:30)**

Now I owe you a straight talk, because I brought up putting these in businesses.

Back in the day I'd set these radios up in waiting rooms as a free stand-in for the paid background-music services. And this Pi version does that job beautifully at home. But if you're thinking of running one in an actual business — a shop, a clinic, a waiting room — I have to be honest with you: playing music publicly in a business usually needs a proper music license. That's literally what those paid services are selling you — not the music, the license. A lot of internet stations are fine for your living room but not cleared for a commercial space, and that's a real legal thing, not me being fussy.

So: build this for your home, your workshop, your garage, all day long. For a business, look into proper licensing first. I learned the shape of that the hard way, and I'd rather you hear it from me.

— — —

**CLOSE (10:30–11:05)**

So that's it — the radio they can't brick. Any station in the world, a real knob you can turn, sound that actually sounds good, and no company anywhere holding the off-switch. It cost a fraction of a fancy internet radio, and unlike the one I lost in 2021, this one's going to still be playing long after the company that made your old one is a memory.

That's really the whole idea behind everything on this channel — own the thing, don't rent it. If this one struck a nerve, tell me in the comments: did you get burned when Reciva went dark, or some other gadget that got shut down out from under you? I read every one. And if you want to build the rest of your own stuff that nobody can switch off, start with the video on screen now. See you in the next one.

— — —
