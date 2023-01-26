import io
import discord
from bot import DiscordBot
from discord.ext import commands
from utils.chatgpt import ChatGPT

__all__: list[str] = ["ChatGPTCog"]

EXTENSIONS: list[str] = [
    "c",
    "cpp",
    "cs",
    "java",
    "py",
    "php",
    "html",
    "css",
    "js",
    "rb",
    "r",
    "go",
    "swift",
    "go",
    "rs",
    "scala",
    "sql",
    "asm",
]


class ChatGPTCog(commands.Cog):
    def __init__(self, bot: commands.Bot, api_key: str):
        self.bot: DiscordBot = bot
        self.client: ChatGPT = ChatGPT(api_key)

    @commands.command(name="code")
    async def code(self, ctx: commands.Context, _type: str, *, prompt: str) -> None:
        """Ask ChatGPT to produce code.

        Args:
            ctx (commands.Context): The context.
            _type (str): The langage, used for formatting output.
            prompt (str): The question.
        """

        res: str = await self.client.completion(prompt=prompt)
        if _type in EXTENSIONS:
            await ctx.message.reply(
                file=discord.File(
                    io.BytesIO(res.encode("utf8")), filename=f"ret.{_type}"
                )
            )

    @commands.command(name="ask")
    async def ask(self, ctx: commands.Context, *, prompt: str) -> None:
        """Ask a question to ChatGPT.

        Args:
            ctx (commands.Context): The context.
            prompt (str): The question.
        """

        res: str = await self.client.completion(prompt=prompt)
        await ctx.message.reply(
            file=discord.File(io.BytesIO(res.encode("utf8")), filename="ret.txt")
        )

    @commands.command(name="generate")
    async def generate_images(
        self, ctx: commands.Context, n: int, *, prompt: str
    ) -> None:
        res: list[str] = await self.client.generate_images(prompt, n)

        for url in res:
            await ctx.message.reply(url)
