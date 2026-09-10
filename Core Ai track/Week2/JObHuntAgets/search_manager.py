import os
from abc import ABC, abstractmethod
from duckduckgo_search import DDGS

# ==========================================
# 1. ABSTRACT BASE CLASS (The Standard Contract)
# ==========================================
class BaseSearchProvider(ABC):
    """
    Abstract interface. Every new search engine we add in the future 
    MUST follow this exact structural blueprint.
    """
    @abstractmethod
    def execute_search(self, query: str, max_results: int) -> list:
        pass

# ==========================================
# 2. CONCRETE PROVIDERS (Individual Engines)
# ==========================================

class DuckDuckGoProvider(BaseSearchProvider):
    """Uses DuckDuckGo (Free, powered behind-the-scenes by Bing)"""
    def execute_search(self, query: str, max_results: int) -> list:
        try:
            with DDGS() as ddgs:
                raw_data = ddgs.text(query, max_results=max_results)
                return [
                    {"title": r.get('title'), "url": r.get('href'), "snippet": r.get('body')}
                    for r in raw_data
                ]
        except Exception as e:
            print(f"[Error DDG]: {e}")
            return []

class TavilyProvider(BaseSearchProvider):
    """Uses Tavily AI API (LLM-Optimized Agent Search)"""
    def __init__(self, api_key: str = None):
        from tavily import TavilyClient
        key = api_key or os.getenv("TAVILY_API_KEY")
        if not key:
            raise ValueError("Missing Tavily API Key. Set TAVILY_API_KEY environment variable.")
        self.client = TavilyClient(api_key=key)

    def execute_search(self, query: str, max_results: int) -> list:
        try:
            raw_data = self.client.search(query=query, max_results=max_results)
            return [
                {"title": r.get('title'), "url": r.get('url'), "snippet": r.get('content')}
                for r in raw_data.get('results', [])
            ]
        except Exception as e:
            print(f"[Error Tavily]: {e}")
            return []

class ExaProvider(BaseSearchProvider):
    """Uses Exa AI API (Neural Embedding Semantic Search)"""
    def __init__(self, api_key: str = None):
        from exa_py import Exa
        key = api_key or os.getenv("EXA_API_KEY")
        if not key:
            raise ValueError("Missing Exa API Key. Set EXA_API_KEY environment variable.")
        self.client = Exa(api_key=key)

    def execute_search(self, query: str, max_results: int) -> list:
        try:
            raw_data = self.client.search_and_contents(query, num_results=max_results, text=True)
            return [
                {"title": getattr(r, 'title', 'No Title'), "url": getattr(r, 'url'), "snippet": getattr(r, 'text', '')[:400]}
                for r in raw_data.results
            ]
        except Exception as e:
            print(f"[Error Exa]: {e}")
            return []

# ==========================================
# 3. SEARCH ENGINE FACTORY (The Switchboard)
# ==========================================
class SearchService:
    """
    Main manager for your app. You only talk to this service.
    It takes care of building the engine and formatting clean text output.
    """
    def __init__(self, provider_type: str = "duckduckgo"):
        self.provider_type = provider_type.lower()
        
        # Instantiate only the chosen single service
        if self.provider_type == "duckduckgo":
            self.provider = DuckDuckGoProvider()
        elif self.provider_type == "tavily":
            self.provider = TavilyProvider()
        elif self.provider_type == "exa":
            self.provider = ExaProvider()
        else:
            raise ValueError(f"Unknown search provider requested: {provider_type}")

    def search_to_string(self, query: str, max_results: int = 3) -> str:
        """Executes search and converts data into a clean text prompt for an AI."""
        results = self.provider.execute_search(query, max_results)
        
        if not results:
            return "No internet search data found."
            
        formatted_str = f"--- Live Internet Search Findings (via {self.provider_type.upper()}) ---\n"
        for idx, item in enumerate(results, 1):
            formatted_str += f"[{idx}] Title: {item['title']}\n"
            formatted_str += f"    URL: {item['url']}\n"
            formatted_str += f"    Content: {item['snippet']}\n\n"
        return formatted_str

# ==========================================
# 4. EXECUTION / TESTING
# ==========================================
if __name__ == "__main__":
    search_query = "What are the latest updates in Azure AI Foundry this month?"
    
    # CHANGE THIS STRING ONSITE TO SWITCH CORES: "duckduckgo", "tavily", or "exa"
    ACTIVE_SERVICE = "duckduckgo" 
    
    print(f"Initializing {ACTIVE_SERVICE} single engine...")
    search_engine = SearchService(provider_type=ACTIVE_SERVICE)
    
    print(f"Searching for: '{search_query}'\n")
    search_prompt_context = search_engine.search_to_string(search_query, max_results=3)
    
    print(search_prompt_context)
