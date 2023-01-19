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
        try:
            res: httpx.Response = await self.session.post(
                url, headers={"Authorization": f"Bearer {self.api_key}"}, json=data
            )
            res.raise_for_status()
        except httpx.HTTPError:
            raise ChatGPTError()
        else:
            return res

    async def completion(self, prompt: str, echo: bool = False) -> str:
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

    @functools.cached_property
    def session(self) -> httpx.AsyncClient:
        return httpx.AsyncClient()
