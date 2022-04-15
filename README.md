Fuckbot
=======

Another fucking Discord robot.


## Commands

The default command prefix is the tilde character, `~`.

For a complete list of commands, run the `~help` command.

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
logfile                  | /var/log/fuckbot/fuckbot.log | Logfile path.
syslog                   | false                        | Enables logging to the syslog via the LOG\_DAEMON facility


## Installation

From within the repository root directory, `pip install .`, preferably from
within a virtualenv.

For distro-specific packages, refer to the documentation provided by your
distribution.
