from configurable_cog import ConfigurableCog
from discord.ext import commands

from .llm import LLMWrapper

default_settings = {}


class Transformer(ConfigurableCog):
    def __init__(self, bot, **kwargs):
        super().__init__(bot, "transformer", default_settings, **kwargs)

    def cog_load(self):
        super().cog_load()
        self.llm = LLMWrapper(self.settings.llm_api_key)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.settings.target_channel_id and message.author.id in self.settings.valid_users:
            await self.transform_message(message.content)

    async def transform_message(self, content):
        data = self.llm.parse_event_details(content)
        print(data)
