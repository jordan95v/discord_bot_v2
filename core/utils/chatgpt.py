from dataclasses import dataclass
import functools
from typing import Any
import httpx

__all__: list[str] = ["ChatGPT", "ChatGPTError"]


class ChatGPTError(Exception):
    """Happens when there is an error with ChatGPT."""


@dataclass
class ChatGPT:
    api_key: str

    async def _call(self, url: str, data: dict[str, Any]) -> httpx.Response:
        """Make a call to the ChatGPT API.

        Args:
            url (str): The url to request.
            data (dict[str, Any]): The json to post.

        Raises:
            ChatGPTError: If there is an error with the API.

        Returns:
            httpx.Response: The response
        """

        try:
            res: httpx.Response = await self.session.post(
                url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=data,
                timeout=None,
            )
            res.raise_for_status()
        except httpx.HTTPError:
            raise ChatGPTError()
        else:
            return res

    async def completion(self, prompt: str, echo: bool = False) -> str:
        """Ask ChatGPT to complete something.

        Args:
            prompt (str): The question.
            echo (bool, optional): Add the question to the response. Defaults to False.

        Raises:
            ChatGPTError: If there is an error getting the data from the response.

        Returns:
            str: The response from the API.
        """

        max_tokens: int = 4096 - len(prompt)
        data: dict[str, Any] = dict(
            prompt=prompt, model="text-davinci-003", max_tokens=max_tokens, echo=echo
        )
        res: httpx.Response = await self._call(
            "https://api.openai.com/v1/completions", data
        )
        try:
            ret: str = res.json()["choices"][0]["text"]
        except KeyError:
            raise ChatGPTError()
        else:
            return ret

    async def generate_images(self, prompt: str, n: int) -> list[str]:
        """Make OpenAI generate an image.

        Args:
            prompt (str): The prompt to generate the image.
            n (int): The number of image generated.

        Raises:
            ChatGPTError: If there is an error getting the data from the response.

        Returns:
            list[str]: All the URL of the image generated by the API.
        """

        n = 10 if n > 10 else n
        data: dict[str, Any] = dict(prompt=prompt, n=n, size="1024x1024")
        res: httpx.Response = await self._call(
            "https://api.openai.com/v1/images/generations", data
        )
        try:
            urls: list[str] = [element["url"] for element in res.json()["data"]]
        except KeyError:
            raise ChatGPTError()
        else:
            return urls

    @functools.cached_property
    def session(self) -> httpx.AsyncClient:
        return httpx.AsyncClient()
