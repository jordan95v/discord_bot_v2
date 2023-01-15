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

        limit: int = n + 1
        await ctx.channel.purge(limit=limit)
        msg: discord.Embed = await self.bot.create_embed(
            "Delete command", f"Deleted {n} messages !"
        )
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

    @commands.command(name="say")
    async def say(self, ctx: commands.Context, *, text: str) -> None:
        """Make the bot say something.

        Args:
            ctx (commands.Context): The context.
            text (str): The text the bot is gonna say.
        """

        await ctx.message.delete()
        await ctx.send(text)
