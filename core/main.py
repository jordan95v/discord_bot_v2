import asyncio
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from bot import DiscordBot
from cogs.chatgpt_cog import ChatGPTCog
from cogs.utils_cog import UtilsCog

COGS: list[commands.Cog] = [ChatGPTCog, UtilsCog]


async def main() -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    client: DiscordBot = DiscordBot(intents=intents, command_prefix="!")
    for cog in COGS:
        await client.add_cog(cog(client))
    return client


if __name__ == "__main__":
    load_dotenv()
    client: DiscordBot = asyncio.run(main())
    client.run(os.getenv("KEY", ""))
