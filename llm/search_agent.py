from tools.web_search import search_web
from datetime import datetime
from agents import Runner, Agent
from pydantic import BaseModel
from llm.utils import add_search_id


class SearchOutput(BaseModel):
    search_id: str
    search_results: str

INSTRUCTIONS = """
You are a Search Agent. You will be given a clearly defined task with all necessary components already decomposed. Today's date is **{current_date}**. You will use the `search_web` tool to search the web for information.

**Instructions:**

1. Focus only on generating precise, high-quality search queries.
2. Use the `search_web` tool to run these queries and find relevant information.
3. You may issue multiple search queries to fully address the task.
4. Return the gathered information in a structured format.

Do not perform task decomposition or analysis. Assume the breakdown is already done.
"""

search_agent = Agent(
    name = "search-agent",
    instructions = INSTRUCTIONS.format(current_date = datetime.now().strftime('%Y-%m-%d')),
    tools = [search_web],
    output_type = SearchOutput
)

search_tool = search_agent.as_tool(
    tool_name="search-agent",
    tool_description="Run the search agent and return results with a unique agent ID",
    custom_output_extractor=add_search_id,
)

if __name__ == "__main__":
    runner = Runner()
    result = runner.run_sync(search_agent, "What is the current weather in Tokyo right now?")
    print(result)