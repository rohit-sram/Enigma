"""
This file is responsible for all the helper functions that are used
"""
from youtubesearchpython import VideosSearch
from src.get_all import filtered_songs

import discord
from discord.ext import commands
from discord.ext.commands import CheckFailure
"""
This function seaches the song on youtube and returns the URL
"""


def searchSong(name_song):
    videosSearch = VideosSearch(name_song, limit=1)
    result = videosSearch.result()
    link = result['result'][0]['link']
    return link


all_songs = filtered_songs()[["track_name", "artist", "genre"]]
"""
This function returns random 25 songs for generating the poll for the user
"""


def random_25():
    random_songs = (all_songs.sample(
        frac=1).groupby('genre').head(1)).sample(25)
    return random_songs


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
