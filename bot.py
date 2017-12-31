
# Massive thanks to Cormac o-brien's tutorial for helping me understand how IRC networking works.
# Tutorial link: http://www.instructables.com/id/Twitchtv-Moderator-Bot/

import socket, re, os, sys
import cfg
import time
import requests, json, random, games
from core.irc import IRC

# Send a normal chat message for various scenarios
def chat (sock, msg):
    sock.send("PRIVMSG #{} :{}\r\n".format(cfg.CHAN, msg).encode("utf-8"))

def whisper (sock, user, content):
    chat(sock, "/w {} {}".format(user, cfg.COMMANDS.get(content)))

# BANHAMMER
def sec_timeout (sock, user, secs=1):
    chat(sock, "/timeout {} {}".format(user,secs))

def ten_timeout (sock, user, secs=600):
    chat(sock, "/timeout {} {}".format(user, secs))

def ban (sock, user):
    chat(sock, "/ban {}".format(user))
    chat(sock, "Please watch your language @{}".format(user))
    

# Have the bot print out the result of a command to the channel's chat
def bot_command (sock, cmd):
    sock.send("PRIVMSG #{} : {}\r\n".format(cfg.CHAN, cfg.COMMANDS.get(cmd)).encode("utf-8"))

def add_command(sock, msg):
    print("hi")

def uptime_check(sock, bot_time):
    chat(sock, "The bot has been online for {} seconds.\r\n".format(bot_time))

def main():

    s = socket.socket()
    s.connect((cfg.HOST,cfg.PORT))

    s.send("PASS {}\r\n".format(cfg.BOT_PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(cfg.BOT_NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(cfg.CHAN).encode("utf-8"))
    s.send('CAP REQ :twitch.tv/commands\r\n'.encode("utf-8"))
    s.send('CAP REQ :twitch.tv/membership\r\n'.encode("utf-8"))

    bot_headers = {"Client-ID": "mj1k7s4wfaeb4rwfojwu5jjgjotn19"}

    chat_msg= re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    whisper_msg = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv WHISPER \w+ :")
    bot_start = time.time() # init start time for the bot for bot_uptime later on. Outside while so it doesn't keep resetting.

    while True:
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            bot_uptime = time.time() - bot_start
            username = re.search(r"\w+", response).group(0)
            message = chat_msg.sub("", response)
            whisper_message = whisper_msg.sub("", response)
            print(username + ": " + message)
            for banned_word in cfg.BAN_WORDS:
                if re.match(banned_word, message):
                    ban(s, username)
                    break
            for timeout_word in cfg.TIMEOUT_WORDS:
                if re.match(timeout_word, message):
                    ten_timeout(s, username)

            # Check for too many caps from users
            if message.isupper():
                total_caps = len(re.findall(r'[A-Z]',message))
                print(username + " just typed " + str(total_caps) + " characters")
                if total_caps > cfg.UPPERCASE_TIMEOUT:
                    sec_timeout(s, username)
                                
            for goof in cfg.GOOFY_WORDS:
                if re.match(goof, message):
                    print(cfg.BOT_NICK + ": "+message)
                    chat(s, message)
                    break

            
            for command in cfg.COMMANDS: # Commands utilize a directory system in cfg.py
                if re.match(command, message):
                    print("reached command")
                    message = message.replace("\r\n", "") # IRC syntax causes \r\n to get appended to the message. Below gets rid of it.
                    bot_command(s, message)
                    break
                if re.match(command,whisper_message):
                    whisper_message = whisper_message.replace("\r\n", "")
                    whisper(s, username, whisper_message)

            for quote in cfg.CHANNEL_QUOTES:
                if "!quote" in message:
                    message = message.replace("\r\n", "") 
                    num_quote, chan_quote = random.choice(dict(cfg.CHANNEL_QUOTES.items())) # Select random quote from cfg.py
                    print(chan_quote)
                    chat(s, chan_quote)
                    break
                
            if "!addquote" in message:
                user_quote = message.split("!addquote ")[1] # All text in string after !addquote will be the actual new quote.
                print(user_quote)
                for key in cfg.CHANNEL_QUOTES.copy().keys():
                    cfg.CHANNEL_QUOTES[key] = cfg.CHANNEL_QUOTES.get(0, key) 
                    user_quote = user_quote.replace("\r\n", "")
                    quote_key = key + 1
                    print(quote_key)
                    new_dict = ({quote_key: user_quote})
                    print(new_dict)
                    cfg.CHANNEL_QUOTES.update(new_dict)
                    
            if "!addcommand" in message:
                print("Stuff should be here, but it isn't yet. :(")            
           
            if "!botrestart" in message:  # If user types !bot_restart, the bot will restart itself. Mainly to check for updates in cfg.py
                chat(s, "Bleep bloop! I am restarting.\r\n")
                os.execv(sys.executable, ['python'] + sys.argv)
                break
            
            if "!botuptime" in message:
                bot_uptime = str(round(bot_uptime, 2)) # Not sure how 'efficient' this is, but here we use round to reduce the float decimal points to 2 points.
                uptime_check(s, bot_uptime)
                
            if "!game" in message:
                url = "https://api.twitch.tv/kraken/channels/{}".format(cfg.CHAN)
                result = requests.get(url, headers=bot_headers)
                json_response = result.json()
                print(json_response)
                game_data = json_response['game']
                chat(s, cfg.CHAN + " is currently playing: " + game_data)

            if "!title" in message:
                url = "https://api.twitch.tv/kraken/channels/{}".format(cfg.CHAN)
                result = requests.get(url, headers=bot_headers)
                json_response = result.json()
                print(json_response)
                status_data = json_response['status']
                chat(s, status_data)

            # Some command line arguments
            if len(sys.argv) > 1:
                if "--log" or "-l" in sys.argv:
                    with open('chatlog.txt', 'ab') as f:
                        f.write((username +": " + message+"\n").encode("utf-8"))

if __name__ == "__main__":
    main()
