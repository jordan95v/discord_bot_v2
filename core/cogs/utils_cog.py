from discord.ext import commands
import discord
from bot import DiscordBot


class UtilsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: DiscordBot = bot

    @commands.command(name="del")
    async def delete(self, ctx: commands.Context, n: int) -> None:
        """Delete n messages from a channel.

        Args:
            ctx (commands.Context): The context.
            n (int): The number of messages to delete.
        """

        await ctx.channel.purge(limit=n + 1)
        msg: discord.Embed = await self.bot.create_embed(f"Deleted {n} messages !")
        await ctx.send(embed=msg)
