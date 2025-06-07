from agents import Agent, Runner, set_tracing_disabled, AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv
import asyncio
import os
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("BASE_URL")
model = os.getenv("Model")


ext_client = AsyncOpenAI(
                        api_key=gemini_api_key,
                        base_url=base_url,
                        )

ext_model = OpenAIChatCompletionsModel(
        model = model,
        openai_client=ext_client
        )

set_tracing_disabled(disabled=True)

agent = Agent(
    name="Assistant",
    instructions="A helpful assistant that can answer questions and provide information.",
    model=ext_model,
)


async def main():
    
    result = await Runner.run(
        agent,
        "What is capital of USA?"
        )
    print(result.final_output)
    
if __name__ == "__main__":
    
    asyncio.run(main())
    
