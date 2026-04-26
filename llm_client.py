import os
import time
from datetime import timedelta
from typing import Optional, Type, TypeVar, overload

from openai import OpenAI
from pydantic import BaseModel

from chat_message import ChatMessage

T = TypeVar("T", bound=BaseModel)


class LLMClient:
    def __init__(self, api_key=None, base_url=None):
        self.api_key = api_key or os.environ.get("API_KEY")
        self.base_url = base_url or os.environ.get("BASE_URL")
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    @overload
    def chat(
        self,
        model: str,
        messages: list[ChatMessage],
        temperature: float = ...,
        *,
        structured_output: Type[T],
    ) -> T: ...

    @overload
    def chat(
        self,
        model: str,
        messages: list[ChatMessage],
        temperature: float = ...,
        structured_output: None = ...,
    ) -> str: ...

    def chat(
        self,
        model: str,
        messages: list[ChatMessage],
        temperature: float = 0.7,
        structured_output: Optional[Type[T]] = None,
    ) -> str | T:
        endpoint_info = f" at {self.base_url}" if self.base_url else ""
        print(
            f"INFO: Sending request to {model}{endpoint_info} with {len(messages)} messages and temperature={temperature}"
        )

        start_time = time.perf_counter()

        if structured_output is not None:
            response = self.client.responses.parse(
                model=model,
                input=messages,  # type: ignore[arg-type]
                temperature=temperature,
                text_format=structured_output,
            )
            parsed = response.output_parsed
            if parsed is None:
                raise ValueError("Failed to parse structured output from response")
            result: str | T = parsed
        else:
            response = self.client.responses.create(
                model=model,
                input=messages,  # type: ignore[arg-type]
                temperature=temperature,
            )
            result = response.output_text
            if result is None:
                raise ValueError("No output text found in response")

        elapsed = time.perf_counter() - start_time
        print(f"INFO: Request completed in {timedelta(seconds=elapsed)}")
        return result
