import json
import logging
import os
import sys
import tabulate

from .config import Config

config = Config()

BLACKLISTS = {}

def blacklist_save():
    with open(config["WORKING_DIR"] + "/" + config["BLACKLIST_DB"], 'w') as db:
            json.dump(BLACKLISTS, db, indent=4)
    

def blacklist_init():
    global BLACKLISTS

    path = config["WORKING_DIR"] + "/" + config["BLACKLIST_DB"]

    try:
        if os.path.isfile(path):
            with open(path, 'r') as db:
                BLACKLISTS = json.load(db)
    except JSONDecodeError as e:
        logging.error(f"JSON error while parsing blacklist db: {e}")

        sys.exit(-1)
    except Exception as e:
        logging.error(f"Error while loading blacklist db: {e}")

        sys.exit(-1)

def blacklist_add(msg):
    try:
        for user in msg.mentions:
            BLACKLISTS[str(msg.guild.id)].append(user.id)

        blacklist_save()

        return f"{[u.mention for u in msg.mentions]} successfully diagnosed with terminal 7 autism"
    except Exception as e:
        logging.warning(f"Error attempting to add user(s) to blacklist: {e}")
        return "Error adding user(s) to blacklist"

def blacklist_list(msg, client):
    if len(BLACKLISTS[str(msg.guild.id)]) == 0:
        return "No blacklisted users"

    pretty = [[client.get_user(uid).name] for uid in BLACKLISTS[str(msg.guild.id)]]

    return tabulate.tabulate(pretty, headers=["User"], tablefmt="fancy_grid")#, showindex="always")

def blacklist_del(msg):
    try:
        for user in msg.mentions:
            BLACKLISTS[str(msg.guild.id)].remove(user.id)

        blacklist_save()

        return f"{[u.mention for u in msg.mentions]} now in remission"
    except Exception as e:
        logging.warning(f"Error attempting to remove user(s) from blacklist: {e}")
        return "Error removing user(s) from blacklist"
