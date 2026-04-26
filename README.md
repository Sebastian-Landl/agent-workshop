# AI Agent Workshop

In this workshop you will implement the core agent loop yourself to truly understand how LLM-powered agents work from the ground up.

---

## Setup

### 1. (Optional) Run a local model with Ollama

If you'd like to run inference locally instead of using a hosted API:

1. Install Ollama from [ollama.com](https://ollama.com)
2. Start the Ollama server:
   ```bash
   OLLAMA_CONTEXT_LENGTH=32768 OLLAMA_FLASH_ATTENTION=1 OLLAMA_KV_CACHE_TYPE=q8_0 ollama serve
   ```
We may especially want to set the context length to a value higher than the default of 4096. The context is where the model "remembers" the conversation, so a longer context allows for more in-depth interactions. The flash attention and kv cache settings are optimizations that can help with performance and memory usage.

3. Pull a model:
   ```bash
   ollama pull ministral:3b
   ```
4. Verify it runs:
   ```bash
   ollama run ministral:3b
   ```
Add `--verbose` to see some nice stats about the model's performance.

### 2. Install `uv`

[`uv`](https://docs.astral.sh/uv/) is a fast Python package and project manager. It will handle the virtual environment, dependencies and the python interpreter for you. Install it with:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then install the project dependencies:

```bash
uv sync
```

### 3. Configure your `.env`

Create a `.env` file in the project root. Simply copy the `.env.example` file to a `.env` and edit that accordingly. If you are using local ollama, you can use any non-empty value for the `API_KEY`. If you are using the OpenAI API, set `BASE_URL` to `https://api.openai.com/v1` or leave it empty.

### 4. Run the agent

```bash
uv run main.py
```

You should see a chat prompt. Type a message and press Enter to chat with the LLM.

---

## Workshop Steps

### 🏆 Final Boss: Build an Agent that calcualtes this

`(sin(current_month) + 17890047.323211) * (86608.432254 + current_hour) / current_year + current_day * 998877.11223344`

The variables (`current_month`, `current_hour`, `current_year`, `current_day`) refer to the **current** date and time — the agent must look them up at runtime using tools.

Use the `verify.py` script to check if your agent's answer is correct.
```bash
uv run verify.py
```

---

### ⚔️ Side Quests (level up before tackling the boss)

Work through these first to build the skills you'll need:

#### Structured Output
Make the LLM respond with a structured JSON object instead of free text.

- Define a [Pydantic](https://docs.pydantic.dev/) model with the fields you want the LLM to fill in
- Force the LLM to respond with an instance of that model

**Goal:** Given a user message like *"What is the capital of France?"*, have the LLM respond with a structured object instead of free text:

```python
class Response(BaseModel):
   thought: str    # e.g. "The user is asking about the capital of France."
   answer: str     # e.g. "The capital of France is Paris."
```

Including a `thought` field encourages the model to reason before answering — a useful pattern for any task that requires more control over the shape of LLM output.

Note on Pydantic models; for debugging you can dump them as json and print that:

```python
response = Response(thought="...", answer="...")
print(response.model_dump_json())
```

---

#### Single Tool Call
Have the LLM express a *wish* to call a tool and then execute that call in Python and return the result to the user. Instructions like "You have the following tools available: ... If you want to call a tool respond with ...". may be useful here.

- Describe an available tool to the LLM in the system prompt (name, purpose, parameters)
- Ask the LLM to respond with the tool name and arguments it wants to invoke, in a format you can parse
- Call the corresponding Python function with the provided arguments
- Show the LLM the result, so it can craft a nice answer for the user

**Goal:** Given *"What time is it?"*, the LLM should respond with a tool call — specifying the tool name and any arguments — that you parse and execute to get a result.

The LLM never runs code itself, it can't — it only declares what it wants to call and with what arguments.
