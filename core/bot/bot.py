import discord
from discord.ext import commands
from utils.help import HELP

__all__: list[str] = ["DiscordBot"]


class DiscordBot(commands.Bot):
    async def on_ready(self):
        """Print when the bot is ready to be used."""

        print(f"Logged on as {self.user}!")

    async def on_command_error(
        self, ctx: commands.Context, error: commands.errors.CommandError
    ) -> None:
        """Send a message when an erro occur.

        Args:
            ctx (commands.Context): The context.
            exception (commands.errors.CommandError): The exception.
        """

        print(error)
        msg: discord.Embed

        if isinstance(error, commands.errors.MissingRequiredArgument):
            msg = await self.create_embed(
                "Arguments missing",
                "You need to give me an arguments !",
            )
        elif isinstance(error, commands.errors.MissingPermissions):
            msg = await self.create_embed(
                "Permission error",
                "You don't have the permission to do that.",
            )
        else:
            msg = await self.create_embed("Error", error)

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
