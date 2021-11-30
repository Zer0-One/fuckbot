import asyncio
import discord
import json
import logging
import subprocess
import youtube_dl

from .util import pp_time

YTDL_OPTS = [
    'youtube-dl',
    '-q',
    '-i',
    '--no-warnings',
    '-f', 'bestaudio/best',
#    '-f', 'worstaudio/worst',
    '--default-search', 'auto',
    '--restrict-filenames',
#    '--yes-playlist',
    '--no-check-certificate',
    '--buffer-size', '16k',
    '-o', '-'
]

YTDL_META_OPTS = [
    'youtube-dl',
    '-J',
    '--no-warnings',
    '--no-check-certificate',
    '--default-search', 'auto'
]

FFMPEG_OPTS = {
    'options': '-vn'
}

QUEUE_HEADERS = ['Title', 'Uploader', 'Duration', 'Queued By', 'URL', 'Thumbnail']

WAITPID = []
QUEUE = {}


# Handle waiting on child processes
async def waitpids():
    while True:
        for p in WAITPID:
            if p.poll():
                p.wait()

        await asyncio.sleep(5)

# Handle queue progress as tracks finish playing
def waitqueues(guild):
    # If not connected to voice, don't do anything
    if not guild.voice_client:
        return

    # Otherwise, pop the queue
    if len(QUEUE[guild.id]) > 0:
        QUEUE[guild.id].pop(0)

    # Start playing the next track, if any
    if len(QUEUE[guild.id]) > 0:
        playcont(guild)

# Determine if a user is qualified to issue a play command
def can_play(user):
    if not user.voice:
        return (False, "You must be in a voice channel before issuing this command")

    if not user.guild.voice_client or not user.guild.voice_client.channel:
        return (False, "You must join the bot to a voice channel before issuing this command")

    if user.voice.channel !=  user.guild.voice_client.channel:
        return (False, "You must be in the same channel as the bot before issuing this command")

    return True, "Success"

# Add track to back of queue; adds to front if front=True
def add(user, query, front=False):
    qualified, ret = can_play(user)

    if not qualified:
        return ret

    q = ' '.join(query).strip()

    entries = meta(user, q)

    if not entries:
        return "Error encountered while trying to add track to queue"

    for entry in entries:
        if front:
            QUEUE[user.guild.id].insert(0, entry)
        else:
            QUEUE[user.guild.id].append(entry)

# Clear the queue
def clear(user):
    qualified, ret = can_play(user)

    if not qualified:
        return ret

    QUEUE[user.guild.id].clear()

# Join voice chat
async def join(user):
    if not user.voice or not user.voice.channel:
        return "You must be in a voice channel to use this command"

    if not user.guild.voice_client or not user.guild.voice_client.is_connected():
        await user.voice.channel.connect()
    else:
        await user.guild.voice_client.move_to(user.voice.channel)

# Leave voice chat
async def leave(user):
    qualified, ret = can_play(user)

    if not qualified:
        return ret

    await user.guild.voice_client.disconnect()

# Fetch track metadata
def meta(user, query):
    try:
        p = subprocess.Popen(YTDL_META_OPTS + [query], stdout=subprocess.PIPE)

        WAITPID.append(p)

        yt_meta = json.load(p.stdout)

        out = []

        # Handle youtube metadata
        if 'youtube' in yt_meta['extractor']:
            if '_type' in yt_meta and yt_meta['_type'] == "playlist":
                for entry in yt_meta['entries']:
                    out.append((entry['title'], entry['uploader'], pp_time(entry['duration']), user, "https://youtu.be/" + entry['display_id'], entry['thumbnail']))
            else:
                out.append((yt_meta['title'], yt_meta['uploader'], pp_time(yt_meta['duration']), user, "https://youtu.be/" + yt_meta['display_id'], yt_meta['thumbnail']))

                return out

    except Exception as e:
        logging.warning(f"ytdl metadata fetch encountered an exception: {e}")

        return None

# Pause audio playback
def pause(user):
    qualified, ret = can_play(user)

    if not qualified:
        return ret

    user.guild.voice_client.pause()

# Create audiosource and play track
async def play(user):
    qualified, ret = can_play(user)

    if not qualified:
        return ret

    if user.guild.voice_client.is_playing():
        return "I'm already playing from the queue, dummy"
    elif user.guild.voice_client.is_paused():
        user.guild.voice_client.resume()

        return None

    try:
        p = subprocess.Popen(YTDL_OPTS + [QUEUE[user.guild.id][0][4]], stdout=subprocess.PIPE)

        WAITPID.append(p)

        await asyncio.sleep(3)

        #source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(p.stdout, pipe=True, **FFMPEG_OPTS))
        #source =  discord.FFmpegPCMAudio(p.stdout, pipe=True, **FFMPEG_OPTS)
        source =  discord.FFmpegOpusAudio(p.stdout, pipe=True, **FFMPEG_OPTS)
        #source = discord.FFmpegOpusAudio.from_probe(p.stdout, **FFMPEG_OPTS)

        user.guild.voice_client.play(source, after=lambda error: waitqueues(user.guild))
    except Exception as e:
        logging.warning(f"play command encountered an exception: {e}")

        return None

def playcont(guild):
    try:
        p = subprocess.Popen(YTDL_OPTS + [QUEUE[guild.id][0][4]], stdout=subprocess.PIPE)

        WAITPID.append(p)

        source =  discord.FFmpegOpusAudio(p.stdout, pipe=True, **FFMPEG_OPTS)

        guild.voice_client.play(source, after=lambda error: waitqueues(guild))
    except Exception as e:
        logging.warning(f"play command encountered an exception: {e}")

# Pretty-print the current queue
def embedqueue(user):
    if len(QUEUE[user.guild.id]) == 0:
        return [discord.Embed(title="Playlist", description="Queue is empty", color=0xe01b24)]

    embeds = []

    for i in range(0, len(QUEUE[user.guild.id])):
        q = discord.Embed(title="Playlist", description=f"\#{i}", color=0xe01b24)
        q.add_field(name="__Title__", value=f"{QUEUE[user.guild.id][i][0]}", inline=False)
        q.add_field(name="__Uploader__", value=f"{QUEUE[user.guild.id][i][1]}", inline=False)
        q.add_field(name="__Duration__", value=f"{QUEUE[user.guild.id][i][2]}", inline=False)
        q.add_field(name="__Queued By__", value=f"{QUEUE[user.guild.id][i][3]}", inline=False)
        q.set_thumbnail(url=QUEUE[user.guild.id][i][5])

        embeds.append(q)

    return embeds

# Stops playback, pops the queue, and plays the next track
async def skip(user):
    qualified, ret = can_play(user)

    if not qualified:
        return ret

    user.guild.voice_client.stop()

    if len(QUEUE[user.guild.id]) > 0:
        QUEUE[user.guild.id].pop(0)

    if len(QUEUE[user.guild.id]) > 0:
        ret = await play(user)

        if ret:
            return ret

# Stop playback
def stop(user):
    qualified, ret = can_play(user)

    if not qualified:
        return ret

    user.guild.voice_client.stop()
