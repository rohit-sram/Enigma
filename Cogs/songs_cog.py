"""
This file is responsible for all bot commands regarding songs such ]poll for generating recommendations,
]next_song for playing next song and so on
"""

import discord
from dotenv import load_dotenv
from discord.ext import commands
import youtube_dl
import yt_dlp
import asyncio
import sys
import urllib.parse, urllib.request, re

from src.get_all import *
from src.utils import searchSong, random_25, has_role_dj, check_vc_status
from src.songs_queue import Songs_Queue
<<<<<<< HEAD:src/songs_cog.py
=======
# from bot import on_ready
>>>>>>> 8a10413 (Changed file structure and version to fix compatibility with Linux and Windows):Cogs/songs_cog.py


# client = commands.Bot(command_prefix=']', intents=intents)
# client.add_check(check_vc_status)

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": [
        "ffmpeg",
        "-i",
        "./assets/sample.mp4",
        "-vn",
        "-f",
        "mp3",
        "./assets/sample.mp3",
    ],
}


ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.25"'}

youtube_base_url = 'https://www.youtube.com/'
youtube_results_url = youtube_base_url + 'results?'
youtube_watch_url = youtube_base_url + 'watch?v='
YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': 'True'}
ytdl = yt_dlp.YoutubeDL(YDL_OPTIONS)
# songs_queue = []
songs_queue = Songs_Queue([])

class Songs(commands.Cog):
    """
    Cog for bot that handles all commands related to songs
    """

    def __init__(self, bot):
        self.bot = bot

    # """
    # Function for playing a song
    # """
    # @commands.command(name='play', help='To play a song')
    # @has_role_dj()
    # async def play(self, ctx):
    #     # await ctx.send(f"Playing {song} requested by {ctx.author.display_name}")
    #     user_message = str(ctx.message.content)
    #     song_name = user_message.split(' ', 1)[1]
    #     await self.play_song(song_name, ctx)


    """
    Function to resume playing
    """
    @commands.command(name="resume", help="Resumes the song")
    @has_role_dj()
    async def resume(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client is None:

            await ctx.send("The bot is not connected to any voice channel at the moment.")

        if voice_client.is_paused():
            await voice_client.resume()
        else:
            await ctx.send(
                "The bot was not playing anything before this. Use play command"
            )

    """
    Function for playing a custom song
    """

    @commands.command(name="play_custom", help="To play custom song")
    @has_role_dj()
    async def play_custom(self, ctx):
        voice_client = ctx.message.guild.voice_client
        user_message = str(ctx.message.content)
        song_name = user_message.split(' ', 1)[1]
        if voice_client.is_playing():
            voice_client.pause()
            await self.play_song(ctx, song_name=song_name)
            return # 
        
        # await self.play_song(ctx, song_name=song_name)


    """
    Function to stop playing the music
    """

    @commands.command(name="stop", help="Stops the song")
    @has_role_dj()
    async def stop(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    """
    Helper function for playing song on the voice channel
    """
    # async def play_song(self, ctx, song_name):
    #     try:
    #         server = ctx.message.guild
    #         voice_channel = server.voice_client
    #     except Exception as e:
    #         print("The user hasn't joined the voice channel.")
    #     try:
    #         if youtube_base_url not in song_name:

    #             query_string = urllib.parse.urlencode({
    #                 'search_query': song_name
    #             })

    #             content = urllib.request.urlopen(
    #                 youtube_results_url + query_string
    #             )

    #             search_results = re.findall(r'/watch\?v=(.{11})', content.read().decode())

    #             link = youtube_watch_url + search_results[0]


    #         loop = asyncio.get_event_loop()
    #         data = await loop.run_in_executor(None, lambda: ytdl.extract_info(link, download=False))

    #         song = data['url']
    #         song_title = data['title']
    #         print(song_title)
    #         player = discord.FFmpegOpusAudio(song, **ffmpeg_options)

    #         voice_channel.play(player)

    #     except Exception as e:
    #         await ctx.send("The bot is not connected to any voice channel at the moment.")

    #         content = urllib.request.urlopen(youtube_results_url + query_string)

    #         search_results = re.findall(
    #             r"/watch\?v=(.{11})", content.read().decode()
    #         )

    #         link = youtube_watch_url + search_results[0]

    #         loop = asyncio.get_event_loop()
    #         data = await loop.run_in_executor(
    #             None, lambda: ytdl.extract_info(link, download=False)
    #         )

    #         song = data["url"]
    #         song_title = data["title"]
    #         print(song_title)
    #         player = discord.FFmpegOpusAudio(song, **ffmpeg_options)

    #         voice_channel.play(player)

    #     except Exception as e:
    #         await ctx.send(
    #             "The bot is not connected to any voice channel at the moment."
    #         )
    
    async def play_song(self, ctx, song_name):
        try:
            server = ctx.message.guild
            voice_channel = server.voice_client
            
            # Check if the bot is connected to a voice channel
            if not voice_channel:
                await ctx.send("The bot is not connected to any voice channel.")
                return
            
            # Stop any currently playing audio before starting a new one
            if voice_channel.is_playing():
                voice_channel.stop()
            
            # Check if song_name is a YouTube URL; otherwise, perform a search
            if youtube_base_url not in song_name:
                query_string = urllib.parse.urlencode({'search_query': song_name})
                content = urllib.request.urlopen(youtube_results_url + query_string)
                search_results = re.findall(r'/watch\?v=(.{11})', content.read().decode())
                if not search_results:
                    await ctx.send("No results found for the song.")
                    return
                
                link = youtube_watch_url + search_results[0]
            else:
                link = song_name  # song_name is already a URL
            
            # Fetch video data asynchronously
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(link, download=False))
            
            # Validate the retrieved song URL
            if 'url' not in data:
                await ctx.send("Unable to retrieve the song URL.")
                return
            
            song = data['url']
            song_title = data['title']
            await ctx.send(f"Now playing: {song_title}")
            print(f"Now playing: {song_title}")
            
            # Play the audio
            player = discord.FFmpegOpusAudio(song, **ffmpeg_options)
            voice_channel.play(player)
            
        except Exception as e:
            # Generic error handling, providing a more detailed message
            await ctx.send(f"An error occurred while trying to play the song: {str(e)}")
            print(f"Error in play_song(): {e}")


    """
    Helper function to handle empty song queue
    """

    async def handle_empty_queue(self, ctx):
        try:
            global songs_queue
        except NameError:
            await ctx.send(
                "No recommendations present. First generate recommendations using ]poll"
            )
            return True
        if songs_queue.get_len() == 0:
            await ctx.send(
                "No recommendations present. First generate recommendations using ]poll"
            )
            return True
        return False

    """
    Function to play the next song in the queue
    """

    @commands.command(name="next_song", help="To play next song in queue")
    @has_role_dj()
    async def next_song(self, ctx):
        global songs_queue
        voice_client = ctx.message.guild.voice_client
        empty_queue = await self.handle_empty_queue(ctx)

        if empty_queue:
            await ctx.send("The queue is empty.")
            return
        
        if voice_client.is_playing():
            await voice_client.pause()
        # print(songs_queue) # temp remove
                  
        # next_song = songs_queue.queue.next_song()
        next_song = songs_queue.next_song()
        # print(next_song)
        if next_song is None:
            await ctx.send("No more songs in the queue")
            return
        # if next_song is not None:
        #     print(next_song)
        
        await ctx.send("Playing the next song now ... ")
        await self.play_song(ctx, next_song)


    """
    Function to play the previous song in the queue
    """

    @commands.command(name="prev_song", help="To play prev song in queue")
    @has_role_dj()
    async def prev_song(self, ctx):
        global songs_queue
        empty_queue = await self.handle_empty_queue(ctx)
        if not empty_queue:
            await self.play_song(ctx, songs_queue.prev_song())

    """
    Function to pause the music that is playing
    """

    @commands.command(name='pause', help='This command pauses the song')
    
    @has_role_dj()
    async def pause(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client is None:

            await ctx.send("The bot is not connected to any voice channel at the moment.")
        elif voice_client.is_playing():
            await voice_client.pause()
            await ctx.send("The song is paused now.")
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    """
    Function to generate poll for playing the recommendations
    """

    @commands.command(name="poll", help="Poll for recommendation")
    # @has_role_dj()
    async def poll(self, ctx):

        global songs_queue
        # self.songs_queue = []
        reactions = ['👍', '👎']
        selected_songs = []
        count = 0
        bot_message = "Select song preferences by reaction '👍' or '👎' to the choices. \nSelect 3 songs"
        await ctx.send(bot_message)
        ten_random_songs = random_25()
        for ele in zip(ten_random_songs["track_name"], ten_random_songs["artist"]):
            bot_message = str(ele[0]) + " By " + str(ele[1])
            description = []
            poll_embed = discord.Embed(
                title=bot_message, color=0x31FF00, description="".join(description)
            )
            react_message = await ctx.send(embed=poll_embed)
            for reaction in reactions[: len(reactions)]:
                await react_message.add_reaction(reaction)
            res, user = await self.bot.wait_for("reaction_add")
            if res.emoji == "👍":
                selected_songs.append(str(ele[0]))
                count += 1
            if count == 3:
                bot_message = "Selected songs are : " + " , ".join(selected_songs)
                await ctx.send(bot_message)
                break
        recommended_songs = recommend(selected_songs)
        songs_queue = Songs_Queue(recommended_songs)
        # print(songs_queue.next_song())
        await self.play_song(ctx, songs_queue.next_song())
        # await self.play_song(songs_queue.next_song(), ctx)


    """
    Function to display all the songs in the queue
    """

    @commands.command(name="queue", help="Show active queue of recommendations")
    @has_role_dj()
    async def queue(self, ctx):
        global songs_queue
        empty_queue = await self.handle_empty_queue(ctx)
        if not empty_queue:
            queue, index = songs_queue.return_queue()
            await ctx.send("Queue of recommendations: ")
            # songs_queue = queue
            songs_queue.queue = queue
            for i in range(len(queue)):
                if i == index:
                    await ctx.send("Currently Playing: " + queue[i])
                else:
                    await ctx.send(queue[i])

    """
    Function to shuffle songs in the queue
    """

    @commands.command(name="shuffle", help="To shuffle songs in queue")
    @has_role_dj()
    async def shuffle(self, ctx):
        global songs_queue
        empty_queue = await self.handle_empty_queue(ctx)
        if not empty_queue:
            songs_queue.shuffle_queue()
            await ctx.send("Playlist shuffled")

    """
    Function to add custom song to the queue
    """

    @commands.command(name="add_song", help="To add custom song to the queue")
    @has_role_dj()
    async def add_song(self, ctx):
        global songs_queue
        user_message = str(ctx.message.content)
        song_name = user_message.split(" ", 1)[1]
        songs_queue.add_to_queue(song_name)
        await ctx.send("Song added to queue")
     
       
    # """
    # Recommending songs based on genre
    # """
    # @commands.command(name='genre', help='To play 5 first songs from the specified genre')
    # async def genre(self, ctx):
    #     user_message = str(ctx.message.content)
    #     genre_name = user_message.split(' ', 1)[1]
    #     await self.play_song_genre(ctx, genre_name=genre_name)
        
    # async def play_song_genre(self, ctx, *, genre_name):
    #     user_message = str(ctx.message.content)
    #     # genre_name = user_message.split(' ')
    #     match = re.search(r"]genre\s+(.+)", user_message)
    #     genre_name = match.group(1)
    #     try:
    #         server = ctx.message.guild
    #         voice_channel = server.voice_client
    #     except Exception as e:
    #         print("The user hasn't joined the voice channel.")
    #     try:
    #         url_list = []
    #         for i in range(5):
    #             if youtube_base_url not in genre_name:
    #                 query_string = urllib.parse.urlencode({
    #                     'search_query': genre_name
    #                 })

    #                 content = urllib.request.urlopen(
    #                     youtube_results_url + query_string
    #                 )

    #                 search_results = re.findall(r'/watch\?v=(.{11})', content.read().decode())

    #                 link = youtube_watch_url + search_results[i]


    #             loop = asyncio.get_event_loop()
    #             # data = await loop.run_in_executor(None, lambda: ytdl.extract_info(link, download=False))
    #             data = loop.run_in_executor(None, lambda: ytdl.extract_info(link, download=False))

    #             song = data['url']
    #             song_title = data['title']
    #             await ctx.send("Playing song : " + song_title)
    #             print(song_title)
    #             player = discord.FFmpegOpusAudio(song, **ffmpeg_options)
    #             voice_channel.play(player)
                
                
    #     except Exception as e:
    #         await ctx.send("The bot is not connected to any voice channel at the moment.")
        

    """
    Recommending songs based on genre
    """
    @commands.command(
        name="genre", help="To play 5 first songs from the specified genre"
    )
    # async def genre(self, ctx):
    #     user_message = str(ctx.message.content)
    #     genre_name = user_message.split(" ", 1)[1]
    #     await self.play_song_genre(ctx, genre_name=genre_name)

    async def play_song_genre(self, ctx, *, genre_name):
        user_message = str(ctx.message.content)
        # genre_name = user_message.split(' ')
        match = re.search(r"]genre\s+(.+)", user_message)
        genre_name = match.group(1)
        try:
            server = ctx.message.guild
            voice_channel = server.voice_client
        except Exception as e:
            print("The user hasn't joined the voice channel.")
        try:
            url_list = []
            for i in range(5):
                if youtube_base_url not in genre_name:
                    query_string = urllib.parse.urlencode({"search_query": genre_name})

                    content = urllib.request.urlopen(youtube_results_url + query_string)

                    search_results = re.findall(
                        r"/watch\?v=(.{11})", content.read().decode()
                    )

                    link = youtube_watch_url + search_results[i]

                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(
                    None, lambda: ytdl.extract_info(link, download=False)
                )

                song = data["url"]
                song_title = data["title"]
                await ctx.send("Playing song : " + song_title)
                print(song_title)
                player = discord.FFmpegOpusAudio(song, **ffmpeg_options)
                voice_channel.play(player)

        except Exception as e:
            await ctx.send(
                "The bot is not connected to any voice channel at the moment."
            )


    """
    Function to play the current song from the queue
    """
    @commands.command(name='play', help="Resume playing from queue")
    @has_role_dj()
    async def play(self, ctx):
        global songs_queue
        voice_client = ctx.message.guild.voice_client
        user_message = str(ctx.message.content) # 
        match = re.search(r"\]play\s*(.+)", user_message) #
        if match is None:
            song_name = ""
        else:
            song_name = match.group(1) # 
        # song_name = user_message.split(' ', 1)[1]
        if voice_client is None:
            await ctx.send("The bot is not connected to any voice channel.")
            return
    
        if song_name is None or song_name == "":
            try:
                index = songs_queue.current_index + 1
                # songs_queue.queue.index = index
                song_in_queue = songs_queue.queue[index]
                print(f"Index = {index} \nSong in Queue: {song_in_queue}")
                print(f"Playing next from queue: {song_in_queue}")
                await ctx.send(f"Playing next from queue: {song_in_queue}")
                await self.play_song(ctx, song_in_queue)
            except Exception as e:
                await ctx.send("There are no more songs in the queue")
                
            
        else:    
            if voice_client.is_playing():
                voice_client.pause()
                await self.play_song(ctx, song_name=song_name)
                return
        
        # if voice_client.is_playing():
        #     await ctx.send("The bot is already playing.")
        #     return

        


"""
    Function to add the cog to the bot
"""
async def setup(client):
    await client.add_cog(Songs(client))
