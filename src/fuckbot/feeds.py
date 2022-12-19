import json
import logging
import os
import sys
import tabulate

import feedparser

from .config import Config

config = Config()

FEEDS = {}

def feed_save():
    try:
        with open(config["WORKING_DIR"] + "/" + config["FEED_DB"], 'w') as db:
            json.dump(FEEDS, db, indent=4)
    except Exception as e:
        logging.error(f"Error while saving feed db: {e}")

        sys.exit(-1)

def feed_init():
    global FEEDS

    path = config["WORKING_DIR"] + "/" + config["FEED_DB"]

    try:
        if os.path.isfile(path):
            with open(path, 'r') as db:
                FEEDS = json.load(db)
    except JSONDecodeError as e:
        logging.error(f"Error while loading feed db: {e}")

        sys.exit(-1)
    except Exception as e:
        logging.error(f"Error while loading feed db: {e}")

        sys.exit(-1)

def feed_add(guild_id, channel_id, url):
    f = feedparser.parse(url)

    if not f.entries or len(f.entries) == 0:
        return "Unable to parse feed"

    FEEDS[str(guild_id)].append({"title": f.feed.title, "channel": channel_id, "url": url, "last_publish": f.entries[0].published_parsed})

    feed_save()

    return "Feed added"

def feed_list(guild):
    if len(FEEDS[str(guild.id)]) == 0:
        return "No feeds available"

    pretty = [(f["title"], guild.get_channel(f["channel"])) for f in FEEDS[str(guild.id)]]

    return '```' + tabulate.tabulate(pretty, headers=["Title", "Notification Channel"], tablefmt="fancy_grid", showindex="always") + '```'

def feed_del(guild_id, idx):
    try:
        i = int(idx)
    except Exception as e:
        return "Index must be an integer"

    if i > len(FEEDS[str(guild_id)]) or i < 0:
        return "Invalid index. Use the `~feed-list` command to see a list of active triggers"


    FEEDS[str(guild_id)].pop(i)

    feed_save()

    return "Feed removed"
