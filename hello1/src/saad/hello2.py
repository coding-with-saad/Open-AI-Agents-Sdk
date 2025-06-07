from agents import Agent,function_tool, Runner, set_tracing_disabled, AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv
from agents import enable_verbose_stdout_logging
import asyncio
import os
function_tool, enable_verbose_stdout_logging 

load_dotenv()
set_tracing_disabled(disabled=True)

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

@function_tool
def multiply(a:int,b:int)->int:
    "multiply two number"
    return a*b


agent = Agent(
    name="Assistant",
    instructions="A helpful assistant that can answer questions and provide information.",
    model=ext_model,
)



async def main():
    
    result = await Runner.run(
        agent,
        "2+3"
        )
    print(result.final_output)
    
if __name__ == "__main__":
    
    asyncio.run(main())
    
