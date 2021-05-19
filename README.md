Fuckbot
=======

Another fucking Discord robot.


## Commands

### Audio Player

- `add` - Adds a track to the queue.
- `clear` - Clears/empties the queue.
- `join` - Joins the bot to your current audio channel.
- `pause` - Pauses audio playback.
- `play` - Play from given URL immediately, otherwise, resumes playing from the queue.
- `queue` - Displays the current queue as a series of embeds.
- `skip` - Skips the current track in the queue.
- `stop` - Stops audio playback.
- `leave` - Parts the bot from voice chat.

### Triggers

- `tr-del` - Deletes an existing trigger.
- `tr-add` - Creates a new message-based trigger.
- `tr-list` - Lists all triggers.

### Blacklist

- `bl-add` - Adds users to a blacklist which prevents all interaction with the bot.
- `bl-list` - Lists all blacklisted users.
- `bl-del` - Removes users from the blacklist.

### Misc

- `interject` - Interjects for a moment.
- `ping` - Pong.
- `roll` - Simulates a dice roll described by `<num>d<sides>[+<add>]`. e.g `2d20` or `4d6+4`.
- `version` - Prints version information.


## Dependencies

- discord.py
- pynacl
- tabulate
- youtube\_dl


## Configuration

Fuckbot looks for an INI-formatted configuration file at the path given in the
`FUCKBOT_CONFIG` environment variable, or at a path specified with the `-c`
option. Below is a table of config file section and directives and what they
do.

Directive                | Default                      | Description
:----------------------: | :--------------------------: | :------------------------------------------------
[fuckbot]                |                              | 
api\_key\_path           | /etc/fuckbot/api.key         | Path to a file containing the discord API key.
debug                    | false                        | Enables debug-level logging. *Very* verbose.
logfile                  | /var/log/runbmc/runbmc.log   | Logfile path.
syslog                   | false                        | Enables logging to the syslog via the LOG\_DAEMON facility


## Installation

From within the repository root directory, `pip install .`, preferably from
within a virtualenv.

For distro-specific packages, refer to the documentation provided by your
distribution.
