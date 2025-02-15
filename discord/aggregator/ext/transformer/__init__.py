from .extension import Transformer


async def setup(bot):
    await bot.add_cog(Transformer(bot))
