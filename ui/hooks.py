from agents.lifecycle import RunHooks, RunContextWrapper
from agents import Agent, Tool
from elements import get_element_info

import chainlit as cl

class MainRunHooks(RunHooks):
    async def on_agent_start(self, context: RunContextWrapper, agent: Agent):
        
        element_manager = cl.user_session.get("element_manager")
        
        if element_manager:
            agent_name = agent.name.split("-")[0]
            stage_type, text = get_element_info(agent_name)
            await element_manager.add(stage_type, text, "active")
    
    async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool: Tool) -> None:
        print("[TOOL] Tool started: ", tool.name)
        if tool.name == "search-agent":
            element_manager = cl.user_session.get("element_manager")
            if element_manager: 
                tool_name = tool.name.split("-")[0]
                stage_type, text = get_element_info(tool_name)
                await element_manager.add(stage_type, text, "active")
            

    async def on_agent_end(self, context: RunContextWrapper, agent: Agent, output) -> None:
        element_manager = cl.user_session.get("element_manager")
        
        if element_manager:
            await element_manager.finish()

    