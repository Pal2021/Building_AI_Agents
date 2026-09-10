import os

import requests

from app.providers.base import BaseSearchProvider


class JSearchProvider(BaseSearchProvider):
    """Searches jobs through JSearch on RapidAPI."""

    endpoint = "https://jsearch.p.rapidapi.com/search"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("RAPIDAPI_KEY") or os.getenv("JSEARCH_RAPIDAPI_KEY")
        if not self.api_key:
            raise ValueError("Missing RAPIDAPI_KEY or JSEARCH_RAPIDAPI_KEY environment variable.")

    def execute_search(self, query: str, max_results: int) -> list[dict]:
        try:
            response = requests.get(
                self.endpoint,
                headers={
                    "X-RapidAPI-Key": self.api_key,
                    "X-RapidAPI-Host": "jsearch.p.rapidapi.com",
                },
                params={
                    "query": query,
                    "page": "1",
                    "num_pages": "1",
                    "date_posted": "today",
                },
                timeout=30,
            )
            response.raise_for_status()
            results = []
            for item in response.json().get("data", []):
                url = item.get("job_apply_link") or item.get("job_google_link") or item.get("job_url")
                if not url:
                    continue
                results.append(
                    {
                        "title": item.get("job_title", "No title"),
                        "url": url,
                        "snippet": item.get("job_description", "")[:1200],
                    }
                )
                if len(results) == max_results:
                    break
            return results
        except (requests.RequestException, ValueError) as error:
            print(f"[Error JSearch]: {error}")
            return []
