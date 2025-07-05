import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents import Agent, Runner
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from llm.answer_agent import answer_agent_handoff
from llm.search_agent import search_tool
from tools.memory import add_to_memory

from agents.extensions.visualization import draw_graph

from dotenv import load_dotenv

load_dotenv(override=True)


INSTRUCTIONS = f"""
{RECOMMENDED_PROMPT_PREFIX}

You are a research agent. Your job is to create a research plan for the given task, then execute it by launching one or more search agents, each with their own specific sub-task.

For each step:
- First, break down the main research task into clear, actionable sub-tasks.
- For each sub-task, spin up a search agent to gather relevant information.
- After each search agent returns results, you may choose to add important findings to a shared context using the `add_to_memory` tool (use the search agent's id as the memory id).
- Repeat this process in a loop: continue planning, launching search agents, and collecting information until you have gathered all necessary documents and data.

Once you have collected all the required information and selected the most relevant context (stored in shared memory), transfer the task to the answer agent. Only the context you have explicitly added to shared memory will be passed to the answer agent for generating the final answer to the user.

Focus on planning, delegation, iterative information gathering, and careful selection of context for the final answer.
"""

research_agent = Agent(
    name="research-agent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    tools=[
        search_tool,
        add_to_memory],
    handoffs=[answer_agent_handoff]
)

if __name__ == "__main__":
    runner = Runner()
    result = runner.run_sync(research_agent, "What is the current weather in Tokyo right now?")
    print(result.final_output)

    draw_graph(research_agent, filename="agent_graph")