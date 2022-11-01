import asyncio
import discord
import logging
import pprint

import fuckbot.audio as audio
import fuckbot.automod as automod
import fuckbot.blacklist as blacklist
import fuckbot.eightball as eightball
import fuckbot.trigger as trigger
import fuckbot.twoweeks as twoweeks

from .config import Config

from .command import ResponseType, is_command, execute
from .rekt import rekt

config = Config()

class FuckbotClient(discord.Client):
    async def on_connect(self):
        # Initialize automod module
        automod.automod_init()

        # Initialize blacklist module
        blacklist.blacklist_init()

        # Initialize trigger module
        trigger.trigger_init()

        # Create task to wait on children created by the audio module
        asyncio.create_task(audio.waitpids())

    async def on_guild_join(self, guild):
        await self.on_guild_available(guild)

    async def on_guild_available(self, guild):
        # Initialize the guild's queue for the audio module
        if not guild.id in audio.QUEUE:
            audio.QUEUE[guild.id] = []

        # Initialize blacklist map, write to disk
        if not str(guild.id) in blacklist.BLACKLISTS:
            blacklist.BLACKLISTS[str(guild.id)] = []
            blacklist.blacklist_save()

        # Initialize trigger map, write to disk
        if not str(guild.id) in trigger.TRIGGERS:
            trigger.TRIGGERS[str(guild.id)] = []
            trigger.trigger_save()

        # Initialize automod config, write to disk
        if not str(guild.id) in automod.AUTOMOD_CONF:
            automod.AUTOMOD_CONF[str(guild.id)] = {}
            automod.automod_save()

    async def on_message(self, message):
        # Don't process messages from yourself
        if message.author == self.user:
            return

        # Don't process DM or Group messages, unless they're from the admin
        if message.channel.type != discord.ChannelType.text and message.author.id != config["ADMIN"]:
            return

        # Don't process messages from blacklisted users
        if message.channel.type == discord.ChannelType.text and message.author.id in blacklist.BLACKLISTS[str(message.guild.id)]:
            return

        # If the message is a question to the bot, answer it
        if self.user in message.mentions:
            msg_stripped = message.content

            while True:
                if msg_stripped.startswith("<"):
                    msg_stripped = msg_stripped.split(None, 1)[1]
                else:
                    break

            if eightball.is_question(msg_stripped):
                await message.channel.send(eightball.answer())

                return

            if twoweeks.is_question(msg_stripped):
                await message.channel.send(twoweeks.answer())

                return

        # If the message is a command, execute it
        if is_command(message):
            resp = await execute(self, message)

            if resp != None:
                if resp[0] == ResponseType.EMBED:
                    await message.channel.send(embed=resp[1])
                elif resp[0] == ResponseType.EMBEDS:
                    for em in resp[1]:
                        await message.channel.send(embed=em)
                elif resp[0] == ResponseType.TEXT:
                    await message.channel.send(resp[1])
                elif resp[0] == ResponseType.TEXTS:
                    for msg in resp[1]:
                        await message.channel.send(msg)
                else:
                    return

        # Process message triggers
        if message.channel.type == discord.ChannelType.text:
            await trigger.trigger(message)

        # If the message is candleja-
        if message.channel.type == discord.ChannelType.text and "candlej" in message.content:
            await message.channel.send("https://i.kym-cdn.com/photos/images/original/000/459/677/ca1.jpg")
            return

    async def on_member_remove(self, member):
        # If someone leaves, make sure we rekt em on the way out
        if member.guild.system_channel:
            await member.guild.system_channel.send(rekt(member.display_name))
