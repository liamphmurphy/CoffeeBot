# Massive thanks to Cormac o-brien's tutorial for helping me understand how IRC networking works.
# Tutorial link: http://www.instructables.com/id/Twitchtv-Moderator-Bot/

import socket, re, os, sys
import cfg
import time
import requests, json

# Send a normal chat message for various scenarios
def chat (sock, msg):
    sock.send("PRIVMSG #{} :{}\r\n".format(cfg.CHAN, msg).encode("utf-8"))

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

def current_game(sock, game):
    chat(sock, "{} is currently playing {}.".format(cfg.CHAN, game))

def main():
    s = socket.socket()
    s.connect((cfg.HOST,cfg.PORT))

    s.send("PASS {}\r\n".format(cfg.BOT_PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(cfg.BOT_NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(cfg.CHAN).encode("utf-8"))

    
    #url = "https://api.twitch.tv/kraken/channels/lphm/follows"
    headers = {"Client-ID": "mj1k7s4wfaeb4rwfojwu5jjgjotn19"}
    #print(result.json())

    chat_msg=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    bot_start = time.time() # init start time for the bot for bot_uptime later on. Outside while so it doesn't keep resetting.

    while True:
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            bot_uptime = time.time() - bot_start
            username = re.search(r"\w+", response).group(0)
            message = chat_msg.sub("", response)
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
                    message = message.replace("\r\n", "") # IRC syntax causes \r\n to get appended to the message. Below gets rid of it.
                    bot_command(s, message)
                    break
            if "!addcommand" in message:
                print("Stuff should be here, but it isn't yet. :(")
            
           
            if "!botrestart" in message:  # If user types !bot_restart, the bot will restart itself. Mainly to check for updates in cfg.py
                chat(s, "Bleep bloop! I am restarting.\r\n")
                os.execv(sys.executable, ['python'] + sys.argv)
                break
            
            if "!botuptime" in message:
                bot_uptime = str(round(bot_uptime, 2)) # Not sure how 'efficient' this is, but here we use round to reduce the float decimal points to 2 points.
                uptime_check(s, bot_uptime)
                
            if "!currentgame" in message:
                url = "https://api.twitch.tv/kraken/channels/{}".format(cfg.CHAN)
                result = requests.get(url, headers=headers)
                json_response = result.json()
                game_data = json_response['game']
                current_game(s, game_data)

            # Some command line arguments
            if len(sys.argv) > 1:
                if "--log" in sys.argv:
                    with open('chatlog.txt', 'ab') as f:
                        f.write((username +": " + message+"\n").encode("utf-8"))

if __name__ == "__main__":
    main()
