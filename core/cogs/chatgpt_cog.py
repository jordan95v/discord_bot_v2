import discord
from discord.ext import commands
from chatgpt_wrapper.chatgpt import ChatGPT
from chatgpt_wrapper.utils.exceptions import ChatGPTError
from bot import DiscordBot


class ChatGPTCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: DiscordBot = bot
        self.client: ChatGPT = ChatGPT(
            "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"
        )

    async def _call(self, ctx: commands.Context, prompt: str) -> str:
        """Call the ChatGPT API.

        Args:
            ctx (commands.Context): The context.
            prompt (str): The question to ask.

        Returns:
            str: The response from the API.
        """

        try:
            res: str = await self.client.completion(prompt=prompt)
        except ChatGPTError:
            await ctx.message.reply("Error with ChatGPT. Try later.")
        else:
            return res

    @commands.command(name="code")
    async def code(self, ctx: commands.Context, _type: str, *, prompt: str) -> None:
        """Ask ChatGPT to produce code.

        Args:
            ctx (commands.Context): The context.
            _type (str): The langage, used for formatting output.
            prompt (str): The question.
        """

        res: str = await self._call(ctx, prompt)
        msg: discord.Embed = await self.bot.create_embed(f"```{_type}\n{res}```")
        await ctx.message.reply(embed=msg)

    @commands.command(name="ask")
    async def ask(self, ctx: commands.Context, *, prompt: str) -> None:
        """Ask a question to ChatGPT.

        Args:
            ctx (commands.Context): The context.
            prompt (str): The question.
        """

        res: str = await self._call(ctx, prompt)
        msg: discord.Embed = await self.bot.create_embed(f"```{res}```")
        await ctx.message.reply(embed=msg)
