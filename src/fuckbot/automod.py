import json
import logging
import sys

from .config import Config

config = Config()

AUTOMOD_CONF = {}

def automod_save():
    try:
        with open(config["WORKING_DIR"] + "/" + config["AUTOMOD_DB"], 'w') as db:
            json.dump(AUTOMOD_CONF, db, indent=4)
    except Exception as e:
        logging.error(f"Error while opening automod db: {e}")

        sys.exit(-1)

def automod_init():
    global AUTOMOD_CONF

    path = config["WORKING_DIR"] + "/" + config["AUTOMOD_DB"]

    try:
        if os.path.isfile(path):
            with open(path, 'r') as db:
                AUTOMOD_CONF = json.load(db)
    except JSONDecodeError as e:
        logging.error(f"JSON error while parsing automod db: {e}")

        sys.exit(-1)
    except Exception as e:
        logging.error("Error while loading automod db: {e}")

        sys.exit(-1)

def automod_disable(msg):
    # Disable automod
    AUTOMOD_CONF[str(msg.guild.id)]["enabled"] = False
    automod_save()

def automod_enable(msg):
    # Enable automod
    AUTOMOD_CONF[str(msg.guild.id)]["enabled"] = True
    automod_save()

def automod_set_channel(msg, channel):
    # Set automod info channel
    pass
