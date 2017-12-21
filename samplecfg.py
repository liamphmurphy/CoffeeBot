# configuration

HOST = "irc.chat.twitch.tv"
PORT = 6667
# Name of your bot
BOT_NICK = ""
#Get Auth key from https://twitchapps.com/tmi
# Copy the whole text, including oauth:

BOT_PASS = ""
# Channel that the bot should moderate
CHAN = ""



# Syntax: ["Noob", "Bruh", "Cake"]
# This Syntax will watch out for the words "Noob", "Bruh" and "Cake" in the corresponding list.

# Absolutely pointless, but this list will have the bot repeat what a user says
# if the user says something from this list.

GOOFY_WORDS = []

# TIMEOUT WORDS

UPPERCASE_TIMEOUT = 20 # If message from user contains more than this number, give a 1 sec timeout.

TIMEOUT_WORDS = []

# BANNABLE WORDS

BAN_WORDS = []

# COMMANDS

# THIS SYNTAX IS A LITTLE MORE COMPLICATED. THIS IS A PYTHON DIRECTORY
# INSIDE THE {}: '!commandname' : 'Result of the command!',
# An example is below

COMMANDS = {'!bot' :'Hello, I am a bot. Bleep bloop! MrDestructoid',
            }
