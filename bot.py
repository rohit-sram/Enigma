"""
This file is the main entry point of the bot
"""

from multiprocessing.util import debug
import discord
import os
from src.get_all import *
import re
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import CheckFailure
from src.utils import searchSong, has_role_dj, update_vc_status, check_vc_status
from src.songs_queue import Songs_Queue
from src.songs_cog import Songs

load_dotenv('.env')
TOKEN = os.getenv('DISCORD_TOKEN')
# This can be obtained using ctx.message.author.voice.channel

VOICE_CHANNEL_ID = 1300855852374163497 # Group 86 test VC
# 1299270426794524708 # Enigma test general
# 1300499798545141873 # Hotel Quink Server
# 1300287459451736064 - SQUAD Server
# 1017135653789646851

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
intents.guilds = True
# client = commands.Bot(command_prefix='/', intents=intents)
client = commands.Bot(command_prefix=']', intents=intents)
authorized_channels = []

"""
Function that gets executed once the bot is initialized
"""
@client.event
async def on_ready():
    voice_channel = client.get_channel(VOICE_CHANNEL_ID)
    if client.user not in voice_channel.members:
        await voice_channel.connect()
    await client.load_extension("src.songs_cog")
    print("Enigma is online!")


"""
Function to reconnect bot if it disconnects
"""
@client.event
async def on_voice_state_update(member, before, after):
    # if member == client.user and before.channel is not None and after.channel is None:
    #     print(f"{str(member.name)} disconnected from {before.channel.name}")
    #     # voice_channel = client.get_channel(VOICE_CHANNEL_ID)
    #     voice_channel = discord.utils.get(client.voice_clients, guild=before.channel.guild)

    #     # Ensure the bot only attempts to connect if it is not already connected
    #     if voice_channel and not voice_channel.is_connected():
    #         await voice_channel.connect(reconnect=True, timeout=10.0)
    
    await update_vc_status(client, member, before, after)
    

client.add_check(check_vc_status())


"""
Function to authorize channels 
"""
channels_help = """
Add allowed channels for the bot 
- example : ]channels <channel1>, <channel2>, ...
"""
# @client.command(name='channels', help='Add allowed channels for the bot')
@client.command(name='channels', help=channels_help)
@has_role_dj()
async def authorize_channel(ctx):
    global authorized_channels
    user_message = str(ctx.message.content)
    extract = re.search(r"\]channels (.+)", user_message)
    if extract:
        channels_extract = [channel.strip() for channel in extract.group(1).split(",")]
        new_channels = []
        for tc in channels_extract:
            if tc not in authorized_channels:
                authorized_channels.append(tc)
                new_channels.append(tc)     
        if new_channels:
            new_channels_str = ', '.join(new_channels)
            await ctx.send(f"Added authorized channels: {new_channels_str}")
        else:
            await ctx.send("No new channels added. All channels have been authorized already.")
    else:
        await ctx.send("No channels found to authorize. Use format: `]channels <channel1>, <channel2>, ...`")


"""
Function for playing a song
"""
@client.command(name='play', help='To play a song')
@has_role_dj()
async def play(ctx, *, song: str):
    await ctx.send(f"Playing {song} requested by {ctx.author.display_name}")

"""
Function that is executed once any message is received by the bot
"""
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    options = set()

    # available_channels = ['general', 't-time', 'testing-space']
    if message.channel.name in authorized_channels:
    # if message.channel.name == 'testing-space':
        user_message = str(message.content)
        await client.process_commands(message)
        
    if message.channel.name == 'testing-space':
        user_message = str(message.content)
        await client.process_commands(message)
           

"""
Error checking function that returns any error received by the bot
"""
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CheckFailure):
        await ctx.send("You need the DJ role to use this command!")
    else:
        print(f"An error has occurred: {error}")


@client.command(name='reconnect', help='To connect the bot to voice channel')
@has_role_dj()
async def reconnect(ctx):
    await ctx.send("Reconnecting enigma to VC ...")
    await on_ready()

"""
Start the bot
"""
client.run(TOKEN)