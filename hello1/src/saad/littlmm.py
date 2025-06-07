from __future__ import annotations
import os
import asyncio
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Disable tracing
set_tracing_disabled(disabled=True)

# Fetch model and API key from environment variables
Model = os.environ.get("GEMINI_MODEL")  # Use correct variable name
KEY = os.environ.get("GEMINI_API_KEY")

# Async function to define agent and run query
async def agent_working2():
    @function_tool
    def get_weather(city: str) -> str:
        print(f"[debug] getting weather for {city}")
        return f"The weather in {city} is sunny."

    agent = Agent(
        name="Assistant",
        model=LitellmModel(model=Model, api_key=KEY),
        tools=[get_weather]
    )

    # Run the agent with a query
    result = await Runner.run(agent, "what is the current weather")
    print(result.final_output)

# Entry point
def main():
    asyncio.run(agent_working2())

if __name__ == "__main__":
    main()
