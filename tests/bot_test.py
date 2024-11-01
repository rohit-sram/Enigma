import unittest
from unittest.mock import AsyncMock, patch, MagicMock
import discord
from discord.ext import commands
from bot import (
    client,
    authorize_channel,
    on_ready,
    on_voice_state_update,
    on_message,
    on_command_error,
    reconnect,
)


class TestEnigmaBot(unittest.TestCase):

    def setUp(self):
        self.bot = client
        self.ctx = AsyncMock()
        self.ctx.send = AsyncMock()

    @patch("discord.ext.commands.Bot.load_extension")
    @patch("discord.VoiceChannel.connect")
    async def test_on_ready(self, mock_connect, mock_load_extension):
        mock_channel = MagicMock(spec=discord.VoiceChannel)
        self.bot.get_channel = MagicMock(return_value=mock_channel)
        mock_channel.members = []

        await on_ready()

        mock_connect.assert_called_once()
        mock_load_extension.assert_called_once_with("Cogs.songs_cog")

    @patch("src.utils.update_vc_status")
    async def test_on_voice_state_update(self, mock_update_vc_status):
        member = MagicMock()
        before = MagicMock()
        after = MagicMock()

        await on_voice_state_update(member, before, after)

        mock_update_vc_status.assert_called_once_with(self.bot, member, before, after)

    @patch("bot.has_role_dj")
    async def test_authorize_channel(self, mock_has_role_dj):
        mock_has_role_dj.return_value = True
        self.ctx.message.content = "]channels test-channel1, test-channel2"

        await authorize_channel(self.ctx)

        self.ctx.send.assert_called_once_with(
            "Added authorized channels: test-channel1, test-channel2"
        )

    async def test_on_message(self):
        message = MagicMock()
        message.author = MagicMock(spec=discord.Member)
        message.author.bot = False
        message.channel.name = "testing-space"

        with patch.object(self.bot, "process_commands") as mock_process_commands:
            await on_message(message)
            mock_process_commands.assert_called_once_with(message)

    async def test_on_command_error_check_failure(self):
        error = commands.CheckFailure()

        await on_command_error(self.ctx, error)

        self.ctx.send.assert_called_once_with(
            "You need the DJ role to use this command!"
        )

    @patch("bot.on_ready")
    @patch("bot.has_role_dj")
    async def test_reconnect(self, mock_has_role_dj, mock_on_ready):
        mock_has_role_dj.return_value = True

        await reconnect(self.ctx)

        self.ctx.send.assert_called_once_with("Reconnecting enigma to VC ...")
        mock_on_ready.assert_called_once()


if __name__ == "__main__":
    unittest.main()
