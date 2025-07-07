import chainlit as cl
import uuid
from typing import Tuple

class ElementManager:
    def __init__(self, text: str = "Agent is working on your request..."):
        self.text = text
        self.elements = []

        self.current_element = None
        self.current_message = None
        
    async def init(self):
        self.current_message = await cl.Message(
            content=self.text,
            elements=[]
        ).send()
    
    async def add(self, element_type: str, props: dict):
        if self.current_element is None:
            await self.init()
        
        if element_type == self.current_element:
            self.elements[-1].props['data'].extend(props)
            return
        
        
        self.current_element = element_type
        self.current_message.elements.append(cl.CustomElement(
            name=element_type,
            props=props))
    
    async def finish(self):
        """Update a specific stage status"""

        if len(self.stages) == 0:
            return
        for stage in self.stages:
            stage['status'] = 'finished'
        
        await self.update()
    
    async def update(self):
        self.workflow_element.props = {
            "stages": self.stages
        }
        
        await self.current_message.update()
    
    async def add(self, name: str, text: str, status: str = 'pending'):

        if self.workflow_element is None:
            await self.init_workflow()
        
        if self.exists(name): return 
        
        await self.finish()

        stage = {
            'id': name, # 'planning', 'searching', 'gathering'
            
            'text': text,
            'status': status # 'pending', 'active', 'finished'
        }

        self.stages.append(stage)
        await self.update()

    def exists(self, name: str):
        if self.stages:
            last_stage = self.stages[-1]
            return last_stage['id'] == name and last_stage['status'] == 'active'



def get_element_info(name: str) -> Tuple[str]:
    if name == "search":
        return "searching", "Spinning up search bots"
    elif name == "answer":
        return "gathering", "Compling results"
    else:
        return "planning", "Planning"