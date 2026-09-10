import os

from app.providers.base import BaseSearchProvider


class ExaProvider(BaseSearchProvider):
    """Uses Exa AI API (Neural Embedding Semantic Search)"""
    def __init__(self, api_key: str = None):
        from exa_py import Exa
        key = api_key or os.getenv("EXA_API_KEY")
        if not key:
            raise ValueError("Missing Exa API Key. Set EXA_API_KEY environment variable.")
        self.client = Exa(api_key=key)

    def execute_search(self, query: str, max_results: int) -> list[dict]:
        try:
            raw_data = self.client.search(
                query,
                num_results=max_results,
                output_schema={"type": "text"},
                type="deep-reasoning",
                contents={"highlights": True},
            )

            results = []
            for result in raw_data.results:
                highlights = getattr(result, "highlights", None) or []
                snippet = " ".join(highlights)
                if not snippet:
                    snippet = getattr(result, "text", "")

                results.append(
                    {
                        "title": getattr(result, "title", "No Title"),
                        "url": getattr(result, "url", ""),
                        "snippet": snippet[:800],
                    }
                )

            return results
        except Exception as e:
            print(f"[Error Exa]: {e}")
            return []