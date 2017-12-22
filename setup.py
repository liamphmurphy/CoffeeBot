from pathlib import Path
import time

print("\n\nWelcome to the setup for CoffeeBot. You can either use this little script to configure your bot,"
    "or you can jump straight to samplecfg.py and manually do it. Feel free to exit with ctrl-c or continue!")
time.sleep(1)
print("\n\nWARNING: IF YOU HAVE A CFG.PY FILE ALREADY, THIS SCRIPT MAY DELETE IT.")
time.sleep(1)
continue_prompt = input("Continue? y for Yes, n for No: ")
if continue_prompt == "y":
    #cfg_file = Path("cfg.py")

    with open('cfg.py', 'wb') as f:
        f.write("HOST = 'irc.chat.twitch.tv'".encode("utf-8"))
        f.write("\nPORT = 6667".encode("utf-8"))
    
    print("\nFirst, please type in the twitch username of your bot. It is highly recommended that this is not your main channel.")
    bot_name = input("Bot username: ")
    with open('cfg.py', 'ab') as f:
        f.write(("\nBOT_NICK = " + "'" + bot_name + "'").encode("utf-8")) 
    
    print("\nTwitch needs to confirm who the bot is. We need an oauth token. In your browser, "
            "sign in to twitch with your bot account and go here: https://twitchapps.com/tmi/"
            "Follow the instructions, and copy the key including the 'oauth' part.")

    bot_oauth = input("\nPlease paste your oauth here (do not share it with anyone!): ")
    with open('cfg.py', 'ab') as f:
        f.write(("\nBOT_PASS = "+"'" + bot_oauth + "'").encode("utf-8"))

    stream_user = input("\nLast, type in the exact username of your primary streaming account: ")
    with open('cfg.py', 'ab') as f:
        f.write(("\nCHAN = " + "'" + stream_user + "'").encode("utf-8"))
        f.write("\n\n\n\n".encode("utf-8"))
        f.write("GOOFY_WORDS = [] # This list will have the bot repeat what a user says if it's in this list.".encode("utf-8"))
        f.write("\n\n".encode("utf-8"))
        f.write("UPPERCASE_TIMEOUT = 20 # If message from user contains more than this number, give a 1 second timeout.".encode("utf-8"))
        f.write("\n\n".encode("utf-8"))
        f.write("TIMEOUT_WORDS = []".encode("utf-8"))
        f.write("\n\n".encode("utf-8"))
        f.write("BAN_WORDS = []".encode("utf-8"))
        f.write("\n\n".encode("utf-8"))
        f.write("COMMANDS = {'!help' :'This is a test help command!',}".encode("utf-8"))

    print("\n\nCongrats! The basics have been setup. If you want to customize further with "
            "custom commands and more, open the file up in a text editor and go crazy!")

