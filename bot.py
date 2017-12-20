# Massive thanks to Cormac o-brien's tutorial for helping me understand how IRC networking works.
# Tutorial link: http://www.instructables.com/id/Twitchtv-Moderator-Bot/

import cfg
import socket, re
from time import sleep

# Send a normal chat message for various scenarios
def chat (sock, msg):
    sock.send("PRIVMSG {} :{}\r\n".format(cfg.CHAN, msg).encode("utf-8"))

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
    sock.send("PRIVMSG {} : {}\r\n".format(cfg.CHAN, cfg.COMMANDS.get(cmd)).encode("utf-8"))

def add_command(sock, msg):
    print("hi")

def main():
    s = socket.socket()
    s.connect((cfg.HOST,cfg.PORT))

    s.send("PASS {}\r\n".format(cfg.BOT_PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(cfg.BOT_NICK).encode("utf-8"))
    s.send("JOIN {}\r\n".format(cfg.CHAN).encode("utf-8"))

    chat_msg=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

    while True:
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = re.search(r"\w+", response).group(0)
            message = chat_msg.sub("", response)
            print(username + ": " + message)
            for pattern in cfg.BAN_WORDS:
                if re.match(pattern, message):
                    print(username)
                    ban(s, username)
                    break
            for goof in cfg.GOOFY_WORDS:
                if re.match(goof, message):
                    print(cfg.BOT_NICK + ": "+message)
                    chat(s, message)
                    break

            # Commands utilize a directory system in cfg.py
            for command in cfg.COMMANDS:
                if re.match(command, message):
                    # IRC syntax causes \r\n to get appended to the message. Below gets rid of it.
                    message = message.replace("\r\n", "")
                    bot_command(s, message)
                    break
                '''if message.isupper():
                    if (message, sum(message for u in message if u.isupper() > 10)):
                        print(username)
                        sec_timeout(s, username)
                        print("User has been timed out.")
                        break'''
            if "!add_command" in message:
                print("Suh dude")
                #add_command()
            if "!restart_bot" in message:
                chat(s, "Bleep bloop! I am restarting.")
                main()
            

if __name__ == "__main__":
    main()