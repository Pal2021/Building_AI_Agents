import os

import requests

from app.providers.base import BaseSearchProvider


class JoobleProvider(BaseSearchProvider):
    """Searches jobs through the Jooble API."""

    endpoint_template = "https://jooble.org/api/{api_key}"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("JOOBLE_API_KEY")
        if not self.api_key:
            raise ValueError("Missing JOOBLE_API_KEY environment variable.")

    def execute_search(self, query: str, max_results: int) -> list[dict]:
        try:
            response = requests.post(
                self.endpoint_template.format(api_key=self.api_key),
                json={
                    "keywords": query,
                    "location": "India",
                    "page": 1,
                },
                timeout=30,
            )
            response.raise_for_status()
            results = []
            for item in response.json().get("jobs", []):
                results.append(
                    {
                        "title": item.get("title", "No title"),
                        "url": item.get("link", ""),
                        "snippet": item.get("snippet", "")[:1200],
                    }
                )
            return [result for result in results if result["url"]][:max_results]
        except (requests.RequestException, ValueError) as error:
            print(f"[Error Jooble]: {error}")
            return []
