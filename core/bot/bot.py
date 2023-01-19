import discord
from discord.ext import commands
from utils.help import HELP
from utils.chatgpt import ChatGPTError

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
        elif isinstance(error, commands.errors.BadArgument):
            msg = await self.create_embed(
                "Bad arguments",
                "Please refer to the help commands to check arguments",
            )
        elif isinstance(error.original, ChatGPTError):
            msg = await self.create_embed(
                "ChatGPT error",
                "Error with ChatGPT, check if hwat you asked respect ChatGPT policy.",
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
