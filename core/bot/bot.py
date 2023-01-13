import discord
from discord.ext import commands


class DiscordBot(commands.Bot):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def create_embed(self, value: str) -> discord.Embed:
        output: discord.Embed = discord.Embed(color=discord.Color.purple())
        output.set_author(name="ChatGPT Response")
        output.add_field(name="", value=value)
        return output
