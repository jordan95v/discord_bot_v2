from bot import DiscordBot
from discord.ext import commands
from utils.chatgpt import ChatGPT, ChatGPTError

__all__: list[str] = ["ChatGPTCog"]

LENGTH: int = 1980


class ChatGPTCog(commands.Cog):
    def __init__(self, bot: commands.Bot, api_key: str):
        self.bot: DiscordBot = bot
        self.client: ChatGPT = ChatGPT(api_key)

    async def split(
        self, ctx: commands.Context, res: str, _type: str | None = None
    ) -> None:
        """Split the string in half.

        Args:
            ctx (commands.Context): The context.
            res (str): The API response.
            _type (str | None, optional): If it's code, then it's the langage. Defaults to None.
        """

        splitted: list[str] = [res[:LENGTH], res[LENGTH:]]
        for text in splitted:
            type_fmt: str = f"{_type}\n" if _type else ""
            await ctx.message.reply(f"```{type_fmt}{text}```")

    @commands.command(name="code")
    async def code(self, ctx: commands.Context, _type: str, *, prompt: str) -> None:
        """Ask ChatGPT to produce code.

        Args:
            ctx (commands.Context): The context.
            _type (str): The langage, used for formatting output.
            prompt (str): The question.
        """

        res: str = await self.client.completion(prompt=prompt)
        res = res.replace("```", "")
        if len(res) > 2000:
            await self.split(ctx, res, _type)
        else:
            await ctx.message.reply(f"```{_type}\n{res}```")

    @commands.command(name="ask")
    async def ask(self, ctx: commands.Context, *, prompt: str) -> None:
        """Ask a question to ChatGPT.

        Args:
            ctx (commands.Context): The context.
            prompt (str): The question.
        """

        res: str = await self.client.completion(prompt=prompt)
        if len(res) > 2000:
            await self.split(ctx, res)
        else:
            await ctx.message.reply(f"```{res}```")

    @commands.command(name="generate")
    async def generate_images(
        self, ctx: commands.Context, n: int, *, prompt: str
    ) -> None:
        res: list[str] = await self.client.generate_images(prompt, n)

        for url in res:
            await ctx.message.reply(url)
