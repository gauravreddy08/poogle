from agents import function_tool, HandoffInputData
import json

# Global shared memory that can be accessed by all agents
SHARED_MEMORY = set()

@function_tool
def add_to_memory(id: str) -> str:
    """
    Add an item to the shared memory. If the item is already in memory, it will be added anyway.
    
    Args:
        id: The unique identifier of the item to add to memory.
        
    Returns:
        A message indicating the item has been added to memory.
    """
    SHARED_MEMORY.add(id)
    return f"Item '{id}' added to shared memory."

def manage_context(handoff_input_data: HandoffInputData) -> HandoffInputData:
    
    filtered_items = tuple()
    remove_call_id = set()

    # First pass: identify call IDs to remove
    for item in handoff_input_data.pre_handoff_items:

        if item.type == "tool_call_item":
            if item.raw_item.name == "add_to_memory":
                remove_call_id.add(item.raw_item.call_id)
                continue

        if item.type == "tool_call_output_item":
            try:
                parsed_output = json.loads(item.output)
                if "search_id" in parsed_output and parsed_output["search_id"] not in SHARED_MEMORY: 
                    remove_call_id.add(item.raw_item["call_id"])
            except (json.JSONDecodeError, KeyError, TypeError):
                # If we can't parse the output or access call_id, skip this item
                continue

    # Second pass: filter out items with call IDs in remove_call_id
    for item in handoff_input_data.pre_handoff_items:
        should_skip = False
        
        if item.type == "tool_call_output_item":
            try:
                if item.raw_item["call_id"] in remove_call_id:
                    should_skip = True
            except (KeyError, TypeError):
                # If we can't access call_id, keep the item
                pass
                
        elif item.type == "tool_call_item":
            try:
                if item.raw_item.call_id in remove_call_id:
                    should_skip = True
            except AttributeError:
                # If we can't access call_id, keep the item
                pass
        
        if not should_skip:
            filtered_items += (item,)

    return HandoffInputData(
        input_history=handoff_input_data.input_history,
        pre_handoff_items=filtered_items,
        new_items=handoff_input_data.new_items
    )

def search_memory(id: str) -> str:
    """
    Search the shared memory for an item.
    """
    return id in SHARED_MEMORY

# @function_tool
# def discard_from_memory(id: str) -> str:
#     """
#     Remove an item from the shared memory. If the item is not found, returns an error message.
    
#     Args:
#         id: The unique identifier of the item to remove from memory.
        
#     Returns:
#         A message indicating whether the item was successfully removed or not found.
#     """
#     if id not in SHARED_MEMORY:
#         return f"Item '{id}' not found in shared memory."
    
#     SHARED_MEMORY.remove(id)
#     print(f"Removed item {id} from shared memory.")
#     return f"Item '{id}' removed from shared memory."