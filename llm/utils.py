import json
import uuid
from agents import RunResult

# Search Agent
async def add_search_id(run_result: RunResult) -> str:
    for item in reversed(run_result.new_items):
        if hasattr(item, 'raw_item') and hasattr(item.raw_item, 'content'):
            for content_item in item.raw_item.content:
                if hasattr(content_item, 'text') and content_item.text.strip().startswith("{"):
                    try:
                        # Parse the existing JSON and add a UUID if not present
                        output_data = json.loads(content_item.text.strip())
                        output_data["search_id"] = str(uuid.uuid4())
                        return json.dumps(output_data)
                    except json.JSONDecodeError:
                        continue
                
    # Fallback with a new UUID
    # return json.dumps({"search_id": str(uuid.uuid4()), "search_results": ""})