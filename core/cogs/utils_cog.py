import random
import discord
from bot import DiscordBot
from discord.ext import commands
from utils.help import HELP

__all__: list[str] = ["UtilsCog"]


class UtilsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: DiscordBot = bot

    @commands.command(name="del")
    @commands.has_permissions(manage_messages=True)
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

    @commands.command(name="rand")
    async def rand(self, ctx: commands.Context, *, number: int) -> None:
        """Choose a random number.

        Args:
            ctx (commands.Context): The context.
            number (int): The maximum number to rand.
        """

        n: int = random.randint(1, number)
        msg: discord.Embed = await self.bot.create_embed(
            f"Rand {number}", f"Result: {n}"
        )
        await ctx.message.reply(embed=msg)

    @commands.command(name="question")
    async def question(self, ctx: commands.Context, *, question) -> None:
        """Make the bot answer a question."""

        choices: list[str] = [
            "Yes.",
            "Clearly.",
            "Definitely.",
            "Without a doubt.",
            "No.",
            "Not at all.",
            "Nope.",
            "This is false.",
        ]

        message: discord.Embed = await self.bot.create_embed(
            question, random.choice(choices)
        )
        await ctx.message.reply(embed=message)
