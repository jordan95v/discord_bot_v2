import asyncio
import os
import discord
from bot import DiscordBot
from cogs.chatgpt_cog import ChatGPTCog
from cogs.utils_cog import UtilsCog
from cogs.reddit_cog import RedditCog
from discord.ext import commands
from dotenv import load_dotenv

COGS: list[commands.Cog] = [RedditCog, UtilsCog]


async def main() -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    client: DiscordBot = DiscordBot(
        intents=intents, command_prefix="$", help_command=None
    )

    api_key: str = os.getenv("API_KEY", "")
    await client.add_cog(ChatGPTCog(client, api_key))

    for cog in COGS:
        await client.add_cog(cog(client))

    return client


if __name__ == "__main__":
    load_dotenv()
    client: DiscordBot = asyncio.run(main())
    client.run(os.getenv("KEY", ""))
