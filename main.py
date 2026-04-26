from dotenv import load_dotenv

from agent import Agent
from chat_message import ChatMessage
from llm_client import LLMClient
from tools import calculator, get_current_datetime

load_dotenv()


def main():
    llm_client = LLMClient()
    agent = Agent(llm_client, tools=[get_current_datetime, calculator])
    chat_history: list[ChatMessage] = []

    print(
        f"Chat started with {agent.model}. Type 'q', 'quit' or 'exit' to end the conversation.\n"
    )

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("q", "quit", "exit"):
            print("Goodbye!")
            break

        chat_history.append({"role": "user", "content": user_input})
        response = agent.run(chat_history)
        chat_history.append({"role": "assistant", "content": response})

        print(f"\nAgent ({agent.model}): {response}\n")


if __name__ == "__main__":
    main()
