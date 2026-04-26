import tiktoken

from chat_message import ChatMessage

ENCODING = tiktoken.get_encoding("o200k_base")


def count_tokens(text: str) -> int:
    return len(ENCODING.encode(text))


def estimate_tokens_messages(messages: list[ChatMessage]) -> int:
    total = 0
    for message in messages:
        total += 3
        total += count_tokens(message["role"])
        total += count_tokens(message["content"])
    total += 3
    return total


def print_message(message: ChatMessage) -> None:
    print(f"{message['role'].upper()}: {message['content']}")


def print_messages(messages: list[ChatMessage]) -> None:
    for message in messages:
        print()
        print_message(message)


def get_function_docstring(func) -> str:
    return func.__doc__ or "No description available."
