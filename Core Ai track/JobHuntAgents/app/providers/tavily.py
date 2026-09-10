import os

from app.providers.base import BaseSearchProvider


class TavilyProvider(BaseSearchProvider):
    """Uses Tavily AI API (LLM-Optimized Agent Search)"""
    def __init__(self, api_key: str = None):
        from tavily import TavilyClient
        key = api_key or os.getenv("TAVILY_API_KEY")
        if not key:
            raise ValueError("Missing Tavily API Key. Set TAVILY_API_KEY environment variable.")
        self.client = TavilyClient(api_key=key)

    def execute_search(self, query: str, max_results: int) -> list[dict]:
        try:
            raw_data = self.client.search(query=query, max_results=max_results)
            return [
                {"title": r.get('title'), "url": r.get('url'), "snippet": r.get('content')}
                for r in raw_data.get('results', [])
            ]
        except Exception as e:
            print(f"[Error Tavily]: {e}")
            return []