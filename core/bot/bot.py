import discord
from discord.ext import commands

__all__: list[str] = ["DiscordBot"]


class DiscordBot(commands.Bot):
    async def on_ready(self):
        """Print when the bot is ready to be used."""

        print(f"Logged on as {self.user}!")

    async def on_command_error(
        self, ctx: commands.Context, exception: commands.errors.CommandError
    ) -> None:
        """Send a message when an erro occur.

        Args:
            ctx (commands.Context): The context.
            exception (commands.errors.CommandError): The exception.
        """

        print(exception)
        msg: discord.Embed = await self.create_embed("Error", exception)
        await ctx.message.reply(embed=msg)

    async def create_embed(self, name: str, value: str) -> discord.Embed:
        """Create an embed message.

        Args:
            value (str): The value of the message.

        Returns:
            discord.Embed: The embedded message.
        """

        output: discord.Embed = discord.Embed(color=discord.Color.purple())
        output.set_author(name=name)
        output.add_field(name="", value=value)
        return output
