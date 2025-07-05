from agents import Agent, Runner, handoff
from tools.memory import manage_context

answer_agent = Agent(
    name="answer-agent",
    instructions=f"You are an answer agent. You will be given context of a set of questions and a set of documents. You will need to answer the questions based on the documents.",
    model="gpt-4o",
)

answer_agent_handoff = handoff(answer_agent, input_filter=manage_context)

if __name__ == "__main__":
    runner = Runner()
    result = runner.run_sync(answer_agent, "What is the capital of France?")