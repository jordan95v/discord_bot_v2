from dataclasses import dataclass
from typing import Any
import pytest
from pytest_mock import MockerFixture
import httpx
from core.utils.chatgpt import ChatGPT, ChatGPTError

__all__: list[str] = ["TestChatGPT"]


@dataclass
class ResponseMock:
    code: int
    data: dict[str, Any]

    def raise_for_status(self) -> None:
        if self.code != 200:
            raise httpx.HTTPError("yo")

    def json(self) -> dict[str, Any]:
        return self.data


class TestChatGPT:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "output, throwable",
        [
            ({"choices": [{"text": "Hello"}]}, None),
            ({}, ChatGPTError),
        ],
    )
    async def test_completion(
        self, mocker: MockerFixture, output: dict[str, str], throwable: Exception | None
    ) -> None:
        client: ChatGPT = ChatGPT(api_key="hello you :)")
        mocker.patch.object(
            httpx.AsyncClient, "post", return_value=ResponseMock(200, output)
        )

        if throwable:
            with pytest.raises(ChatGPTError):
                await client.completion("Hello")
        else:
            res: str = await client.completion("Hello")
            assert res == "Hello"

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "output, throwable",
        [
            ({"data": [{"url": "Hello"}, {"url": "World"}]}, None),
            ({}, ChatGPTError),
        ],
    )
    async def test_generate(
        self, mocker: MockerFixture, output: dict[str, str], throwable: Exception | None
    ) -> None:
        client: ChatGPT = ChatGPT(api_key="hello you :)")
        mocker.patch.object(
            httpx.AsyncClient, "post", return_value=ResponseMock(200, output)
        )
        if throwable:
            with pytest.raises(ChatGPTError):
                await client.generate_images("Hello", "2")
        else:
            res: str = await client.generate_images("Hello", "2")
            assert res[0] == "Hello"

    @pytest.mark.asyncio
    async def test_call(self, mocker: MockerFixture) -> None:
        client: ChatGPT = ChatGPT(api_key="hello you :)")
        mocker.patch.object(
            httpx.AsyncClient, "post", return_value=ResponseMock(400, {})
        )
        with pytest.raises(ChatGPTError):
            await client._call("heeelo", {})
