import os 
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chainlit as cl
from agents import Runner
from ui.hooks import MainRunHooks
from elements import ElementManager
from llm.research_agent import research_agent
import time

@cl.on_message
async def on_message(msg: cl.Message):
    # Create status manager
    element_manager = ElementManager()
    cl.user_session.set("element_manager", element_manager)

    # await element_manager.add("planning", "Hello Word", "active")
    # time.sleep(2)
    # await element_manager.add("searching", "Hello Word2", "active")
    # time.sleep(2)
    # await element_manager.add("gathering", "Hello Word3", "active")

    # await cl.Message(
    #     content="Lol",  # ← Use result.final_output
    # ).send()


    # Create hooks by subclassing RunHooks
    hooks = MainRunHooks()
    
    # Create runner without arguments
    runner = Runner()

    # Run the agent with hooks passed to run_async
    result = await runner.run(research_agent, msg.content, hooks=hooks)

    # Send final answer
    await cl.Message(
        content=result.final_output,  # ← Use result.final_output
    ).send()