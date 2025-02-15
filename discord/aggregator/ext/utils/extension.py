from datetime import datetime

import discord
from configurable_cog import ConfigurableCog
from discord import app_commands

default_settings = {"pong_message": "pong"}


class Utils(ConfigurableCog):
    def __init__(self, bot, **kwargs):
        super().__init__(bot, "utils", default_settings, **kwargs)

    @app_commands.command()
    async def ping(self, interaction: discord.Interaction):
        """Latency/bot-uptime command."""
        time_passed = datetime.now(self.bot.timezone) - self.start_time
        await interaction.response.send_message(
            f"{self.settings.pong_message}, took {round(self.bot.latency*1000)}ms.\n"
            f"bot has been up for {round(time_passed.seconds)} seconds\n"
            f"running on version {self.bot.version}.",
            ephemeral=True,
        )
