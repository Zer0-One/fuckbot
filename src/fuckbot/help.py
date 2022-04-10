CMDLIST = """```
To get help for a particular command, use: ~help cmd

Audio Commands:
add   - Adds a track to the queue
clear - Clears/empties the queue
join  - Joins the bot to your current audio channel
pause - Pauses audio playback
play  - Plays from the given URL immediately; otherwise resumes playing from the queue
queue - Displays the queue
skip  - Skips the current track in the queue
stop  - Stops audio playback
leave - Parts the bot from voice chat

Triggers:
tr-add  - Creates a new message-based trigger
tr-del  - Deletes an existing trigger
tr-list - Lists all triggers

Blacklist:
bl-add  - Adds users to the blacklist, preventing all interaction with the bot
bl-del  - Removes users from the blacklist
bl-list - Lists all blacklisted users

Misc:
interject - Interjects for a moment
ping      - Pong
roll      - Simulates a dice roll
version   - Prints version and license information
```"""

HELPSYNTAX = {
    'add': "add <URL>",
    'clear': "clear",
    'join': "join",
    'pause': "pause",
    'play': "play [<URL>]",
    'queue': "queue",
    'skip': "skip",
    'stop': "stop",
    'leave': "leave",

    'tr-add': "tr-add [case] [full]",
    'tr-del': "tr-del <index>",
    'tr-list': "tr-list",

    'bl-add': "bl-add <@user> [<@user>]...",
    'bl-del': "bl-del <index>",
    'bl-list': "bl-list",

    'roll': 'roll <num>d<sides>[+<add>]'
}
HELPDESC = {
    'add': "Adds a track to the queue. Currently, only youtube URLs are supported.",
    'clear': "Empties the queue.",
    'join': "Causes the bot to join the audio channel you are currently in.",
    'pause': "Pauses audio playback. You can resume playback with the 'play' command.",
    'play': "Resumes stopped or paused audio playback. If a URL is given, plays from that URL immediately.",
    'queue': "Displays the audio queue as a series of embeds.",
    'skip': "Skips the current (first) track in the queue.",
    'stop': "Stops audio playback. Does not change the queue. Restarting playback will start the current track from the beginning.",
    'leave': "Causes the bot to leave voice chat.",

    'tr-add': "Creates a new message-based trigger via dialog with the bot. To complete the dialog, you must use the reply feature to reply to the bot's messages.\n\nBy default, matches are case-insensitive. To force case-sensitivity, add the 'case' argument. Similarly, by default, substring matches are performed. To match an entire message, add the 'full' argument.",
    'tr-del': "Removes the trigger at the given index. Use 'tr-list' to index triggers.",
    'tr-list': "Lists all triggers, with indexes in the leftmost column.",

    'bl-add': "Adds one or more users to a bot blacklist which prevents the bot from interacting with them. The arguments must be actual user mentions, not just usernames or IDs.",
    'bl-del': "Removes the user at the given index from the blacklist.",
    'bl-list': "Lists all blacklisted users, with indexes in the leftmost column.",

    'roll': "Simulates a dice roll. e.g '2d20' or '4d6+4'."
}

def help(cmd):
    if cmd not in HELPSYNTAX or cmd not in HELPDESC:
        return "There is no help for this command"

    return "```Usage: " + HELPSYNTAX[cmd] + "\n\n" + HELPDESC[cmd] + "```"
