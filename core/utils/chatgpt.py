import openai

__all__: list[str] = ["ChatGPT", "ChatGPTError"]


class ChatGPTError(Exception):
    """Happens when there is an error with ChatGPT."""


class ChatGPT:
    def __init__(self, api_key: str) -> None:
        openai.api_key = api_key

    async def completion(self, prompt: str, echo: bool = False) -> str:
        max_tokens: int = 4096 - len(prompt)
        res: dict[str, str] = await openai.Completion.acreate(
            model="text-davinci-003", prompt=prompt, max_tokens=max_tokens, echo=echo
        )
        try:
            ret: str = res["choices"][0]["text"]
        except KeyError:
            raise ChatGPTError()
        else:
            return ret
