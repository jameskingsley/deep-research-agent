from llama_index.tools.tavily_research import TavilyToolSpec
import os
from dotenv import load_dotenv

load_dotenv()

def get_search_tool():
    """
    Initializes and returns the Tavily search tool specification.
    """
    tavily_key = os.getenv("TAVILY_API_KEY")
    if not tavily_key:
        raise ValueError("TAVILY_API_KEY not found in environment variables")
        
    tavily_tool = TavilyToolSpec(api_key=tavily_key)
    return tavily_tool.to_tool_list()