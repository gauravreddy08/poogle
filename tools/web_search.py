from serpapi import GoogleSearch
import tiktoken
from firecrawl import FirecrawlApp

from agents import function_tool
from ui.agent_workflow import add_query_element

import os
import dotenv

dotenv.load_dotenv(override=True)

@function_tool
async def search_web(query: str, fresh: str = "fresh") -> str:
    """
    Search the web for information about the query.
    Returns the markdown content of top results.
    
    Args:
        query: The query to search the web for.
        fresh: The freshness of the data to search the web for. (Default: "fresh") ["5min", "hour", "day", "week", "month", "year"]
    
    Returns:
        The markdown content of top results.
    """
    fresh = data_freshness.get(fresh, 0)
    await add_query_element(query)

    links = get_links(query)
    content = ""
    for link in links:
        content += f"# Data from {link}\n"
        try:
            content += link_to_md(link, fresh=fresh)
            content += "\n\n"
        except Exception as e:
            content += f"Error fetching content: {str(e)}\n\n"

    return content

def get_links(query):
    """Search the web for information about the query"""
    api_key = os.getenv("SERP_API")
    if not api_key:
        return ["https://example.com"] 
    
    params = {
        "engine": "google_light",
        "google_domain": "google.com",
        "hl": "en",
        "num": 3,
        "api_key": api_key
    }
    try:
        search = GoogleSearch({**params, "q": query})
        results = search.get_dict()
        organic_results = results.get("organic_results", [])
        links = [result["link"] for result in organic_results]
        return links
    except Exception as e:
        print(f"Error in web search: {e}")
        return ["https://example.com"] 


def count_tokens(text):
    encoding = tiktoken.encoding_for_model("gpt-4o")
    return len(encoding.encode(text))

data_freshness = {
    "5min": 300000,
    "hour": 3600000,
    "day": 86400000,
    "week": 604800000,
    "month": 2592000000,
    "year": 31536000000,
}

def link_to_md(link, fresh = 0):
    api_key = os.getenv("FIRECRAWL_API")
    if not api_key:
        return f"Content from {link} (API key not configured)"
    
    if fresh != 0:
        fresh = data_freshness["week"]
    
    try:
        app = FirecrawlApp(api_key=api_key)
        response = app.scrape_url(url=link, max_age=fresh)
        return response.markdown
    except Exception as e:
        return f"Error fetching content from {link}: {str(e)}"


if __name__ == "__main__":
    links = search_web("Red Earphones to Buy")
    total_tokens = 0
    for link in links:
        md = link_to_md(link, fresh=data_freshness["year"])
        print(md)
        break
    print(total_tokens)
    