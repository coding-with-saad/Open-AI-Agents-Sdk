import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, enable_verbose_stdout_logging 
from agents import enable_verbose_stdout_logging

enable_verbose_stdout_logging()
#enable_verbose_stdout

load_dotenv()

set_tracing_disabled(disabled=True)
#BASE URL
BASE_URL = os.getenv("BASE_URL")
#API KEY FROM .ENV FILE
API_KEY= os.getenv("GEMINI_API_KEY")
#MODEL
MODEL=os.getenv("Model")

client = AsyncOpenAI(
    api_key = API_KEY,
    base_url = BASE_URL
)

gemini_model = OpenAIChatCompletionsModel(
    model = MODEL,
    openai_client= client,
)

#Create a tool
@function_tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b + 2


agenta = Agent(
    name = "Assistant",
    instructions = "you will provide weather report of Islamabad",
    model = gemini_model,
    handoff_description="You will provide weather report in a funny way"
)

agentb = Agent(
    name = "math_agent",
    instructions="you are a mathematician", # system instructions / Persona
    model = gemini_model,
    tools = [multiply],
    handoff_description="you will multiply"
)

triage_agent = Agent(
    name = "Boss_agent",
    instructions = "You are Boss agent and will distribut tasks to Subordinate agents",
    model = gemini_model,
    handoffs=[agenta , agentb]
)
result = Runner.run_sync(triage_agent,"what is weather of Islamabad")
print(result.final_output)