import argparse
import discord
import logging
import os

from pprint import pprint

from .client import FuckbotClient
from .config import Config
#from .db import db_init
from .log import log_init

config = Config()

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Fuck")
    parser.add_argument("-c", "--config", default="", help="Path to the Fuckbot configuration file")
    args = parser.parse_args()

    # Initialize logging
    log_init()

    # Parse config file. Config file path passed via env takes precedence.
    if os.environ.get(Config._Config__CONFIG_ENV):
        Config.config_init(os.environ.get(Config._Config__CONFIG_ENV))
    else:
        Config.config_init(args.config)

    # Warning: this will print the API key to stdout
    if config["DEBUG"]:
        pprint(config.items())

    # Initialize logging again, but with the user's config this time
    log_init(config["LOGFILE"], config["SYSLOG"], config["DEBUG"])

    logging.info("----- FUCKBOT ONLINE AND READY TO FUCK -----")

    # Main event loop
    client = FuckbotClient(intents=discord.Intents.all())
    client.run(config["API_KEY"])
