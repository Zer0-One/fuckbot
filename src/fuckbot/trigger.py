import asyncio
import base64
import discord
import io
import json
import logging
import os
import sys
import tabulate

from enum import Enum

from .config import Config

config = Config()

USAGE = """
```
Usage: trigger [case] [full]\n
Notes:
By default, matches are case insensitive. To force case sensitivity, add the 'case' argument.
By default, substring matches are performed. To match an entire message, add the 'full' argument.
If no reply is given within 15 seconds, the bot will forget your trigger.
```
"""

TRIGGERS = {}

TRIGGER_HEADERS = {
    't_user': 'Added By',
    't_text': 'Trigger',
    't_full': 'Full-Match',
    't_case': 'Case-Sensitive',
    'r_name': '',
    'r_file': '',
    'r_text': ''
}

def trigger_save():
    with open(config["WORKING_DIR"] + "/" + config["TRIGGER_DB"], 'w') as db:
        json.dump(TRIGGERS, db, indent=4)
    
def trigger_init():
    global TRIGGERS

    path = config["WORKING_DIR"] + "/" + config["TRIGGER_DB"]

    try:
        if os.path.isfile(path):
            with open(path, 'r') as db:
                TRIGGERS = json.load(db)
    except JSONDecodeError as e:
        logging.error(f"Error while parsing trigger db: {e}")

        sys.exit(-1)
    except Exception as e:
        logging.error(f"Error while loading trigger db: {e}")

        sys.exit(-1)
#    engine = create_engine("sqlite+pysqlite:///" + config["WORKING_DIR"] + "/" + config["SQLITE_DB"], future=True)
#
#    try:
#        with engine.begin() as con:
#            res = con.execute(text(SQLITE_TRIGGER_CREATE))
#
#        return True
#    except Exception as e:
#        logging.error(f"Error initializing trigger database table: {e}")
#
#        return None

async def trigger_create(msg, client, case=False, full=False):
    def check(chk):
        return chk.author == msg.author and chk.reference and chk.reference.cached_message and chk.reference.cached_message.author == client.user

    params = {}

    try:
        await msg.reply("What text should I match on?")
        reply = await client.wait_for('message', check=check, timeout=30)

        if reply.content:
            params["t_text"] = reply.content

            for trg in TRIGGERS[str(msg.guild.id)]:
                if trg["t_text"].lower() == params["t_text"].lower():
                    TRIGGERS[str(msg.guild.id)].remove(trg)
                    break
        else:
            await msg.reply("I can't respond to nothing...")

            return None

        params["t_case"] = case
        params["t_full"] = full 
        params["t_user"] = msg.author.name
        #params["t_user"] = msg.author.id

        await reply.reply("And how should I respond when I see that text?")
        reply = await client.wait_for('message', check=check, timeout=30)

        if reply.attachments:
            params["r_name"] = reply.attachments[0].filename
            f = await reply.attachments[0].to_file()
            params["r_file"] = base64.b64encode(f.fp.read()).decode('utf-8')
        else:
            params["r_name"] = None
            params["r_file"] = None

        params["r_text"] = reply.content

        TRIGGERS[str(msg.guild.id)].append(params)

        trigger_save()

        return "Trigger successfully added"
    except asyncio.TimeoutError as e:
        logging.warning(f"Timeout while waiting on trigger reply")

        return "Timed out while waiting for reply. I'll forget about that trigger."
    except Exception as e:
        if 'r_text' in params:
            logging.error(f"Error creating trigger for '{params['r_text']}': {e}")
        else:
            logging.error(f"Error creating trigger: {e}")

        return None

async def trigger_remove(msg, index):
    try:
        i = int(index)

        if i > len(TRIGGERS[str(msg.guild.id)]) or i < 0:
            return "Invalid index. Use the `~list` command to see a list of active triggers"

        trg = TRIGGERS[str(msg.guild.id)].pop(i)

        trigger_save()

        return f"Trigger \"{trg['t_text']}\" successfully deleted"
    except Exception as e:
        logging.error(f"Error deleting trigger: {e}")

def trigger_list(msg):
    if len(TRIGGERS[str(msg.guild.id)]) == 0:
        return "No active triggers"

    trim = [trg.copy() for trg in TRIGGERS[str(msg.guild.id)]]

    for trg in trim:
        trg.pop('r_name')
        trg.pop('r_file')
        trg.pop('r_text')

    return tabulate.tabulate(trim, headers=TRIGGER_HEADERS, tablefmt="fancy_grid", showindex="always")

async def trigger(msg):
    try:
        for trg in TRIGGERS[str(msg.guild.id)]:
            if trg['t_full'] and trg['t_case']:
                if msg.content != trg['t_text']:
                    continue
            elif trg['t_full'] and not trg['t_case']:
                if msg.content.lower() != trg['t_text'].lower():
                    continue
            elif not trg['t_full'] and trg['t_case']:
                if not trg['t_text'] in msg.content:
                    continue
            elif not trg['t_full'] and not trg['t_case']:
                if not trg['t_text'].lower() in msg.content.lower():
                    continue

            if trg['r_name']:
                await msg.channel.send(content=trg['r_text'], file=discord.File(fp=io.BytesIO(base64.b64decode(trg['r_file'])), filename=trg['r_name']))
            else:
                await msg.channel.send(trg['r_text'])

            break
    except Exception as e:
        logging.error(f"Error searching trigger db for matching trigger: {e}")

#async def trigger_create(msg, client, case=False, exact=False):
#    def check(chk):
#        return chk.author == msg.author and chk.reference and chk.reference.cached_message and chk.reference.cached_message.author == client.user
#
#    params = {}
#
#    try:
#        params["gid"] = msg.guild.id
#        params["t_user"] = msg.author.name
#        params["t_case"] = case
#        params["t_exact"] = exact
#
#        await msg.reply("What text should I match on?")
#        reply = await client.wait_for('message', check=check, timeout=15)
#
#        if reply.content:
#            params["t_text"] = reply.content
#        else:
#            await msg.reply("I can't respond to nothing...")
#
#            return None
#
#        await msg.reply("And how should I respond when I see that text?")
#        reply = await client.wait_for('message', check=check, timeout=15)
#
#        if reply.attachments:
#            params["r_name"] = reply.attachments[0].filename
#            f = await reply.attachments[0].to_file()
#            params["r_file"] = base64.b64encode(f.fp)
#        else:
#            params["r_name"] = None
#            params["r_file"] = None
#
#        params["r_text"] = reply.content
#
#        #engine = create_engine("sqlite+pysqlite:///" + config["WORKING_DIR"] + "/" + config["SQLITE_DB"], future=True)
#        with engine.begin() as con:
#            res = con.execute(text(SQLITE_TRIGGER_INSERT), params)
#
#        return "Trigger successfully added"
#    except TimeoutError as e:
#        logging.warning("Timed out while waiting for reply. I'll forget about that trigger.")
#
#        return None
#    except Exception as e:
#        logging.error(f"Error creating trigger for '{params['r_text']}': {e}")
#
#        return None

#def trigger(msg):
#    try:
#        with engine.begin() as con:
#            res = con.execute(text(SQLITE_TRIGGER_SELECT), {'gid': msg.guild.id})
#
#            for row in res.all():
#                if row.t_exact and row.t_case:
#                    if msg.content != row.t_text:
#                        continue
#                elif row.t_exact and not row.t_case:
#                    if msg.content.lower() != row.t_text.lower():
#                        continue
#                elif not row.t_exact and row.t_case:
#                    if row.t_text in msg.content:
#    except Exception as e:
#        logging.error(f"Error searching trigger db for matching trigger: {e}")

#def trigger(msg):
#    engine = create_engine("sqlite+pysqlite:///" + config["WORKING_DIR"] + config["SQLITE_DB"], future=True)
#
#    with engine.connect() as conn:
#        res = conn.execute(text(f"select * from triggers"))
#
#        for row in res.all():
#            if row.exact and row.nocase:
#                if msg.lower() != row.trigger.lower():
#                    return None
#            elif row.exact and not row.nocase:
#                if msg != row.trigger:
#                    return None
#            elif not row.exact and row.nocase:
#                if msg.lower() not in row.trigger.lower():
#                    return None
#            else
#                if msg not in row.trigger:
#                    return None
#
#        res = conn.execute(text(f"select * from responses where rhash='{row.rhash}'"))
#
#        # Throw an exception if we get no response, or if there are multiple responses for this one trigger
#        res_row = res.one()
#
#        # Text response
#        if res.type == 0:
#            return res_row.data_txt
#        # Image response
#        elif res.type == 1:
#            # filename?
#            return res_row.data_img
#
#        sys.exit(-1)
#
#def trigger_create(trigger, response, exact = False):
#    engine = create_engine("sqlite+pysqlite:///" + config["WORKING_DIR"] + config["SQLITE_DB"], future=True)
#
#    with engine.connect() as conn:
#        if exact:
#             #don't lowercase
#        else:
#            trigger.lower()
