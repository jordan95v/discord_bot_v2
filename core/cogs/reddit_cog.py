from typing import Any
import httpx
from bot import DiscordBot
from discord.ext import commands

__all__: list[str] = ["RedditCog"]


class RedditCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: DiscordBot = bot

    async def _scrape_reddit(self, sub: str, n: int, top: bool) -> dict[str, Any]:
        """Scrape the subreddit.

        Args:
            sub (str): The subreddit to scrape.
            n (int): The number of images to scrape.
            top (bool): The sort of the subreddit.

        Returns:
            dict[str, Any]: The scraped post.
        """

        async with httpx.AsyncClient() as client:
            try:
                res: httpx.Response = await client.get(
                    f"https://www.reddit.com/r/{sub}/top.json",
                    headers={"User-agent": "jdr"},
                    params={"limit": n, "t": "all" if top else ""},
                )
                res.raise_for_status()
            except httpx.HTTPError:
                print("An error occurred")
            else:
                return res.json()

    async def send_images(self, ctx: commands.Context, posts: dict[str, Any]) -> None:
        """Send the images to the discord channel.

        Args:
            ctx (commands.Context): The context.
            posts (dict[str, Any]): The dict containing posts element.
        """

        for element in posts:
            url: str = element["data"]["url"]
            if url.endswith((".jpg", ".png", ".gif")) and url.startswith(
                ("https://i.redd.it/", "https://i.imgur.com")
            ):
                await ctx.send(element["data"]["url"])

    @commands.command(name="top")
    async def top(self, ctx: commands.Context, sub: str, n: int) -> None:
        """Scrape the top n images of a subreddit.

        Args:
            ctx (commands.Context): The context.
            sub (str): The sub to scrape.
            n (int): The number of images to scrape.
        """

        data: dict[str, Any] = await self._scrape_reddit(sub, n, True)
        posts: list[dict[str, Any]] = data["data"]["children"]
        await self.send_images(ctx, posts)

    @commands.command(name="hot")
    async def hot(self, ctx: commands.Context, sub: str, n: int) -> None:
        """Scrape the most viewed of the day n images of a subreddit.

        Args:
            ctx (commands.Context): The context.
            sub (str): The sub to scrape.
            n (int): The number of images to scrape.
        """

        data: dict[str, Any] = await self._scrape_reddit(sub, n, False)
        posts: list[dict[str, Any]] = data["data"]["children"]
        await self.send_images(ctx, posts)
