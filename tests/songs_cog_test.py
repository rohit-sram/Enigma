# import pytest
# import unittest
# from Cogs.songs_cog import *
# import warnings
# import sys

# sys.path.append("../")

# warnings.filterwarnings("ignore")


# @pytest.mark.asyncio
# class Test_Songs_Cog(unittest.TestCase):

#     async def test_resume(self):
#         result = await Songs.resume()
#         assert result == "The bot was not playing anything before this. Use play command"

#     async def test_stop(self):
#         result = await Songs.stop()
#         assert result == "The bot is not playing anything at the moment."

#     async def test_play_song(self):
#         result = await Songs.play_song()
#         assert result == "The bot is not connected to a voice channel."

#     async def test_handle_empty_queue(self):
#         result = await Songs.handle_empty_queue()
#         assert result == "No recommendations present. First generate recommendations using /poll"

#     async def test_pause(self):
#         result = await Songs.pause()
#         assert result == "The bot is not playing anything at the moment."

#     async def test_shuffle(self):
#         result = await Songs.shuffle()
#         assert result == "Playlist shuffled"

#     async def test_add_song(self):
#         result = await Songs.add_song()
#         assert result == "Song added to queue"



import pytest
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from discord.ext import commands
from Cogs.songs_cog import Songs
import warnings
import sys

sys.path.append("../")

warnings.filterwarnings("ignore")

@pytest.mark.asyncio
class Test_Songs_Cog(unittest.TestCase):

    def setUp(self):
        self.bot = MagicMock(spec=commands.Bot)
        self.cog = Songs(self.bot)

    async def test_resume(self):
        ctx = AsyncMock()
        ctx.message.guild.voice_client = AsyncMock()
        ctx.message.guild.voice_client.is_paused.return_value = True

        await self.cog.resume(ctx)

        ctx.message.guild.voice_client.resume.assert_called_once()
        ctx.send.assert_not_called()

    async def test_play_custom(self):
        ctx = AsyncMock()
        ctx.message.guild.voice_client = AsyncMock()
        ctx.message.content = "]play_custom Test Song"

        with patch.object(self.cog, 'play_song') as mock_play_song:
            await self.cog.play_custom(ctx)

        ctx.message.guild.voice_client.pause.assert_called_once()
        mock_play_song.assert_called_once_with(ctx, song_name="Test Song")

    async def test_stop(self):
        ctx = AsyncMock()
        ctx.message.guild.voice_client = AsyncMock()
        ctx.message.guild.voice_client.is_playing.return_value = True

        await self.cog.stop(ctx)

        ctx.message.guild.voice_client.stop.assert_called_once()

    @patch('Cogs.songs_cog.ytdl')
    @patch('Cogs.songs_cog.discord.FFmpegOpusAudio')
    async def test_play_song(self, mock_ffmpeg, mock_ytdl):
        ctx = AsyncMock()
        ctx.message.guild.voice_client = AsyncMock()
        mock_ytdl.extract_info.return_value = {'url': 'test_url', 'title': 'Test Song'}

        await self.cog.play_song(ctx, "Test Song")

        ctx.send.assert_called_with("Now playing: Test Song")
        ctx.message.guild.voice_client.play.assert_called_once()

    async def test_handle_empty_queue(self):
        ctx = AsyncMock()
        self.cog.songs_queue = MagicMock()
        self.cog.songs_queue.get_len.return_value = 0

        result = await self.cog.handle_empty_queue(ctx)

        assert result == True
        ctx.send.assert_called_with("No recommendations present. First generate recommendations using ]poll")

    async def test_next_song(self):
        ctx = AsyncMock()
        self.cog.songs_queue = MagicMock()
        self.cog.songs_queue.next_song.return_value = "Next Song"

        with patch.object(self.cog, 'play_song') as mock_play_song:
            await self.cog.next_song(ctx)

        ctx.send.assert_called_with("Playing the next song now ... ")
        mock_play_song.assert_called_once_with(ctx, "Next Song")

    async def test_prev_song(self):
        ctx = AsyncMock()
        self.cog.songs_queue = MagicMock()
        self.cog.songs_queue.prev_song.return_value = "Previous Song"

        with patch.object(self.cog, 'play_song') as mock_play_song:
            await self.cog.prev_song(ctx)

        mock_play_song.assert_called_once_with(ctx, "Previous Song")

    async def test_pause(self):
        ctx = AsyncMock()
        ctx.message.guild.voice_client = AsyncMock()
        ctx.message.guild.voice_client.is_playing.return_value = True

        await self.cog.pause(ctx)

        ctx.message.guild.voice_client.pause.assert_called_once()
        ctx.send.assert_called_with("The song is paused now.")

    @patch('Cogs.songs_cog.random_25')
    @patch('Cogs.songs_cog.recommend')
    async def test_poll(self, mock_recommend, mock_random_25):
        ctx = AsyncMock()
        mock_random_25.return_value = {"track_name": ["Song1", "Song2", "Song3"], "artist": ["Artist1", "Artist2", "Artist3"]}
        mock_recommend.return_value = ["Rec1", "Rec2", "Rec3"]
        self.bot.wait_for.return_value = (AsyncMock(emoji="👍"), AsyncMock())

        with patch.object(self.cog, 'play_song') as mock_play_song:
            await self.cog.poll(ctx)

        ctx.send.assert_any_call("Selected songs are : Song1 , Song2 , Song3")
        mock_play_song.assert_called_once()

    async def test_queue(self):
        ctx = AsyncMock()
        self.cog.songs_queue = MagicMock()
        self.cog.songs_queue.return_queue.return_value = (["Song1", "Song2", "Song3"], 1)

        await self.cog.queue(ctx)

        ctx.send.assert_any_call("Queue of recommendations: ")
        ctx.send.assert_any_call("Currently Playing: Song2")

    async def test_shuffle(self):
        ctx = AsyncMock()
        self.cog.songs_queue = MagicMock()

        await self.cog.shuffle(ctx)

        self.cog.songs_queue.shuffle_queue.assert_called_once()
        ctx.send.assert_called_with("Playlist shuffled")

    async def test_add_song(self):
        ctx = AsyncMock()
        ctx.message.content = "]add_song New Song"
        self.cog.songs_queue = MagicMock()

        await self.cog.add_song(ctx)

        self.cog.songs_queue.add_to_queue.assert_called_once_with("New Song")
        ctx.send.assert_called_with("Song added to queue")

    @patch('Cogs.songs_cog.ytdl')
    async def test_play_song_genre(self, mock_ytdl):
        ctx = AsyncMock()
        ctx.message.guild.voice_client = AsyncMock()
        ctx.message.content = "]genre Rock"
        mock_ytdl.extract_info.return_value = {'url': 'test_url', 'title': 'Test Song'}

        await self.cog.play_song_genre(ctx, genre_name="Rock")

        ctx.send.assert_called_with("Playing song : Test Song")
        ctx.message.guild.voice_client.play.assert_called()

    async def test_play(self):
        ctx = AsyncMock()
        ctx.message.guild.voice_client = AsyncMock()
        self.cog.songs_queue = MagicMock()
        self.cog.songs_queue.queue = ["Song1", "Song2", "Song3"]
        self.cog.songs_queue.current_index = 0

        with patch.object(self.cog, 'play_song') as mock_play_song:
            await self.cog.play(ctx)

        ctx.send.assert_called_with("Playing next from queue: Song2")
        mock_play_song.assert_called_once_with(ctx, "Song2")

if __name__ == '__main__':
    unittest.main()