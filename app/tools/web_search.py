from langchain_tavily import TavilySearch

from app.config import TAVILY_API_KEY


search_tool = TavilySearch(
    max_results=5,
    topic="general",
    tavily_api_key=TAVILY_API_KEY,
)