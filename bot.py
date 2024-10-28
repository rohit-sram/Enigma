"""
This file is the main entry point of the bot
"""

from multiprocessing.util import debug
import discord
import os
from src.get_all import *
import re
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import CheckFailure
from src.utils import searchSong
from src.songs_queue import Songs_Queue
from src.songs_cog import Songs

load_dotenv('.env')
TOKEN = os.getenv('DISCORD_TOKEN')
# This can be obtained using ctx.message.author.voice.channel
VOICE_CHANNEL_ID = 1300499798545141873 # Hotel Quink Server
# 1300287459451736064 - SQUAD Server
# 1017135653789646851
intents = discord.Intents.all()
intents.members = True
intents.message_content = True
intents.guilds = True
# client = commands.Bot(command_prefix='/', intents=intents)
client = commands.Bot(command_prefix=']', intents=intents)

"""
Function to check if user had 'DJ' role
"""

def has_role_dj():
    async def predicate(ctx):
        dj_role = discord.utils.get(ctx.guild.roles, name='DJ')
        if dj_role in ctx.author.roles:
            return True
        raise CheckFailure("You do not have permission to use the bot")
    return commands.check(predicate)

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
Function restricting DJ role to use 'play'
"""

@client.command(name='play')
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

    # if message.channel.name == 'general':
    #     user_message = str(message.content)
    #     await client.process_commands(message)
    
    if message.channel.name == 't-time':
        user_message = str(message.content)
        await client.process_commands(message)


"""
Function to reconnect bot if it disconnects
"""

@client.event
async def on_voice_state_update(member, before, after):
    if member == client.user and before.channel is not None and after.channel is None:
        print(f"{member} disconnected from the {before.channel.name} channel")
        # voice_channel = client.get_channel(VOICE_CHANNEL_ID)
        voice_channel = discord.utils.get(client.voice_clients, guild=before.channel.guild)

        # Ensure the bot only attempts to connect if it is not already connected
        if voice_channel and not voice_channel.is_connected():
            await voice_channel.connect(reconnect=True, timeout=10.0)


"""
Error checking function that returns any error received by the bot
"""

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CheckFailure):
        await ctx.send("You need the DJ role to use this command!")
    else:
        print(f"An error has occurred: {error}")


"""
Start the bot
"""
client.run(TOKEN)
