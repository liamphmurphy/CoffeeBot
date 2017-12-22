# CoffeeBot
An IRC bot for Twitch.tv written in python. 

This runs on Linux, Windows and Mac as long as you have Python 3 installed.

```
python bot.py
```

The config file is crucial for this bot to run. In fact, this is the only file that you should backup if you are running this bot for your own stream. If the config file is gone, so will all of your custom preferences. 

Rename samplecfg.py to cfg.py for the program to recognize it.




## Planned Features
### High
- [ ] Add way to make new commands from twitch chat
- [ ] Support whispers to the bot
- [ ] Find a good long-term way to organize the code, not just all in one file (other than cfg).
- [x] Timeout users for too many uppercase characters
- [ ] Setup script that walks a user through a fresh setup. Ask channel name, bot name etc.

### Medium
- [ ] Add minigames
- [ ] Add first time setup (if cfg.py doesn't exist is the general idea)
- [ ] quote system (Streamers can say funny things. When user types !quote, a random quote that the streamer/mods entered is printed)
- [ ] Add uptime counter

### Low

- Web Server / UI?
