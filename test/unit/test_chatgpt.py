import pytest
from pytest_mock import MockerFixture
import openai
from core.utils.chatgpt import ChatGPT, ChatGPTError

__all__: list[str] = ["TestChatGPT"]


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
        mocker.patch.object(openai.Completion, "acreate", return_value=output)

        if throwable:
            with pytest.raises(ChatGPTError):
                await client.completion("Hello")
        else:
            res: str = await client.completion("Hello")
            assert res == "Hello"
