import os
from typing import Callable, Optional

from chat_message import ChatMessage
from llm_client import LLMClient

DEFAULT_SYSTEM_PROMPT_PATH = "system_prompt.txt"


class Agent:
    def __init__(
        self,
        llm_client: LLMClient,
        system_prompt_path: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        tools: Optional[list[Callable]] = None,
    ):
        self.llm_client = llm_client
        self.model = model or os.environ.get("MODEL", "gpt-5.4-mini")
        self.temperature = (
            temperature
            if temperature is not None
            else float(os.environ.get("TEMPERATURE", "0.7"))
        )
        self.system_prompt = self._load_system_prompt(system_prompt_path)
        self.tools = {tool.__name__: tool for tool in tools or []}

    def _load_system_prompt(self, path: Optional[str] = None) -> str:
        prompt_path = path or os.environ.get(
            "SYSTEM_PROMPT_PATH", DEFAULT_SYSTEM_PROMPT_PATH
        )
        with open(prompt_path, "r") as f:
            return f.read().strip()

    def run(self, chat_history: list[ChatMessage]) -> str:
        messages: list[ChatMessage] = [
            {"role": "system", "content": self.system_prompt},
            *chat_history,
        ]

        return self.llm_client.chat(self.model, messages, self.temperature)
