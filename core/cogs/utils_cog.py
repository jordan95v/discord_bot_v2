from discord.ext import commands
import discord
from bot import DiscordBot
from utils.help import HELP


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

    @commands.command(name="help")
    async def help(self, ctx: commands.Context) -> None:
        """Show the help message.
        Args:
            ctx (commands.Context): The context.
        """

        message: discord.Embed = discord.Embed(
            title="Help",
            description="Show the list of commands available.",
            color=discord.Color.green(),
        )

        for element in HELP:
            message.add_field(name=element["name"], value=element["value"])

        await ctx.send(embed=message)
