import discord
import logging

import fuckbot.audio as audio
import fuckbot.automod as automod
import fuckbot.blacklist as blacklist
import fuckbot.help as help
import fuckbot.interject as interject
import fuckbot.roll as roll
import fuckbot.trigger as trigger

from enum import Enum
from .ticker import ticker_embed
from .version import AUTHOR, LICENSE_FULL_NAME, URL, VERSION

class ResponseType(Enum):
    TEXT = 1
    TEXTS = 2
    EMBED = 3
    EMBEDS = 4
    NONE = 5

def is_command(msg):
    if msg.content.startswith("~") and len(msg.content) > 1:
        return True

async def execute(client, msg):
    cmdseq = msg.content[1:].split()

    directive = cmdseq[0].lower()

    logging.debug(f"Command '{directive}' given")

    if directive == "add":
        if len(cmdseq) < 2:
            return (ResponseType.TEXT, "You must specify a URL to play from")

        ret = audio.add(msg.author, cmdseq[1:])

        if ret:
            return (ResponseType.TEXT, ret)

        await msg.delete()

        return (ResponseType.NONE, None)

    if directive == "am-disable":
        automod.automod_disable(msg)

        return (ResponseType.TEXT, "Automod disabled")

    if directive == "am-enable":
        automod.automod_enable(msg)

        return (ResponseType.TEXT, "Automod enabled")

    if directive == "bl-add":
        if not msg.author.guild_permissions.manage_messages:
            return (ResponseType.TEXT, "You must have the manage_messages permission to use the blacklist")

        if len(cmdseq) < 2:
            return (ResponseType.TEXT, "You must specify a user to blacklist")

        ret = blacklist.blacklist_add(msg)

        if ret:
            return (ResponseType.TEXT, ret)

        return (ResponseType.NONE, None)

    if directive == "bl-del":
        if not msg.author.guild_permissions.manage_messages:
            return (ResponseType.TEXT, "You must have the manage_messages permission to use the blacklist")

        if len(cmdseq) < 2:
            return (ResponseType.TEXT, "You must specify a user to blacklist")

        ret = blacklist.blacklist_del(msg)

        if ret:
            return (ResponseType.TEXT, ret)

        return (ResponseType.NONE, None)

    if directive == "bl-list":
        ret = blacklist.blacklist_list(msg, client)

        if ret:
            return (ResponseType.TEXT, "```" + ret + "```")

        return (ResponseType.NONE, None)

    if directive == "clear":
        ret = audio.clear(msg.author)

        if ret:
            return (ResponseType.TEXT, ret)

        await msg.delete()

        return (ResponseType.NONE, None)

    if directive == "help":
        if len(cmdseq) < 2 or len(cmdseq) > 2:
            return (ResponseType.TEXT, help.CMDLIST)

        return (ResponseType.TEXT, help.help(cmdseq[1]))

    if directive == "interject":
        return (ResponseType.TEXT, interject.INTERJECTION)

    if directive == "join":
        ret = await audio.join(msg.author)

        if ret:
            return (ResponseType.TEXT, ret)

        await msg.delete()

        return (ResponseType.NONE, None)

    if directive == "leave":
        ret = await audio.leave(msg.author)

        if ret:
            return (ResponseType.TEXT, ret)

        await msg.delete()

        return (ResponseType.NONE, None)

    if directive == "pause":
        ret = audio.pause(msg.author)

        if ret:
            return (ResponseType.TEXT, ret)

        await msg.delete()

        return (ResponseType.NONE, None)

    if directive == "ping":
        return (ResponseType.TEXT, "pong")

    if directive == "play":
        # Argument given, play it immediately
        if len(cmdseq) > 1:
            ret = audio.stop(msg.author)

            if ret:
                return (ResponseType.TEXT, ret)

            ret = audio.add(msg.author, cmdseq[1:], True)

            if ret :
                return (ResponseType.TEXT, ret)

            ret = await audio.play(msg.author)

            if ret:
                return (ResponseType.TEXT, ret)

            await msg.delete()

            return (ResponseType.NONE, None)
        # No argument given, play from current queue
        else:
            ret = await audio.play(msg.author)

            if ret:
                return (ResponseType.TEXT, ret)

            await msg.delete()

            return (ResponseType.NONE, None)

    if directive == "purge":
        if not msg.author.guild_permissions.manage_messages:
            return (ResponseType.TEXT, "You must have manage_messages permissions to use the 'purge' command")

        if len(cmdseq) > 2:
            return (ResponseType.TEXT, "You can only purge one user at a time (for safety 'n stuff)")

        if len(cmdseq) < 2:
            return (ResponseType.TEXT, "You need to mention a user to purge")

        if not msg.mentions:
            return (ResponseType.TEXT, "You need to mention a user to purge")

        name = msg.mentions[0].name

        await msg.reply("Purging message history for '{name}'")

        for channel in msg.guild.text_channels:
            deleted = await channel.purge(limit=None, check=lambda message:message.author.id == msg.mentions[0].id)

        return (ResponseType.TEXT, f"Successfully purged {deleted} messages from user '{name}'")

    if directive == "queue":
        return (ResponseType.EMBEDS, audio.embedqueue(msg.author))

    if directive == "roll":
        if len(cmdseq) < 2:
            return (ResponseType.TEXT, roll.USAGE)

        return (ResponseType.TEXT, roll.roll(cmdseq[1]))

    if directive == "skip" or directive == "next":
        ret = await audio.skip(msg.author)

        if ret:
            return (ResponseType.TEXT, ret)

        await msg.delete()

        return (ResponseType.NONE, None)

    #if directive == "speak":
    #    if msg.author.voice and msg.author.voice.channel:
    #        if msg.guild.voice_client and msg.guild.voice_client.is_connected():
    #            await msg.guild.voice_client.move_to(msg.author.voice.channel)
    #            add_q(msg.guild.id, "https://www.youtube.com/watch?v=EaDlo7uk9Dk", msg.author.name, True)
    #        else:
    #            return (ResponseType.TEXT, "FUCK")

    #    return (ResponseType.NONE, None)

    if directive == "stop":
        ret = audio.stop(msg.author)

        if ret:
            return (ResponseType.TEXT, ret)

        await msg.delete()

        return (ResponseType.NONE, None)

    #if directive == "ticker":
    #    return (ResponseType.EMBED, ticker_embed(cmdseq[1]))

    if directive == "tr-add":
        if len(cmdseq) > 3:
            return (ResponseType.TEXT, trigger.USAGE)

        case = False
        full = False

        for i in range(1, len(cmdseq)):
            if cmdseq[i] == "case":
                case = True
            elif cmdseq[i] == "full":
                full = True
            else:
                return (ResponseType.TEXT, trigger.USAGE)

        res = await trigger.trigger_create(msg, client, case, full)

        if not res:
            return (ResponseType.TEXT, "Error encountered while attempting to add trigger")

        return (ResponseType.TEXT, res)

    if directive == "tr-del":
        if len(cmdseq) < 2:
            return (ResponseType.TEXT, "You must specify a trigger index to delete")

        ret = await trigger.trigger_remove(msg, cmdseq[1])

        if ret:
            return (ResponseType.TEXT, ret)

        return (ResponseType.TEXT, "Error encountered while attempting to delete trigger")

    if directive == "tr-list":
        ret = trigger.trigger_list(msg)

        if ret:
            return (ResponseType.TEXTS, ret)

        return (ResponseType.TEXT, "Error encountered while attempting to enumerate triggers")

    if directive == "version":
        version_text = f"Fuckbot version: {VERSION}\n"
        version_text += f"Copyright (c) 2021, {AUTHOR}\nAll rights reserved\n"
        version_text += f"This software is licensed under the terms of the {LICENSE_FULL_NAME}\n"
        version_text += f"{URL}"

        return (ResponseType.TEXT, version_text)

    logging.debug(f"Command '{directive}' not registered, ignoring")

    return None
