from configurable_cog import ConfigurableCog
from discord.ext import commands
import aiohttp

from .data import add_guild_past_event, get_guild_prompting
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
        if message.channel.id == self.settings.target_channel_id and message.author.id in self.settings.valid_guilds:
            await self.transform_message(message.content,
                                         additional_data=get_guild_prompting(message.author.id),
                                         timezone=self.bot.timezone)

    async def transform_message(self, content, additional_data=None, timezone=None):
        data = self.llm.parse_event_details(content, additional_data=additional_data, timezone=timezone)

        add_guild_past_event(data["guild_channel_id"], data["title"], data["date"])

        async with aiohttp.ClientSession() as session:
            async with session.post(self.settings.transformer_url, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    print("Response from transformer:", result)
                else:
                    print("Failed to send data to transformer:", response.status)

        print(data)
