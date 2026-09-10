import os

import requests

from app.providers.base import BaseSearchProvider


class AdzunaProvider(BaseSearchProvider):
    """Searches jobs through the Adzuna API."""

    endpoint_template = "https://api.adzuna.com/v1/api/jobs/{country}/search/1"

    def __init__(
        self,
        app_id: str | None = None,
        app_key: str | None = None,
        country: str = "in",
    ):
        self.app_id = app_id or os.getenv("ADZUNA_APP_ID")
        self.app_key = app_key or os.getenv("ADZUNA_APP_KEY")
        self.country = country
        if not self.app_id or not self.app_key:
            raise ValueError(
                "Missing ADZUNA_APP_ID or ADZUNA_APP_KEY environment variable."
            )

    def execute_search(self, query: str, max_results: int) -> list[dict]:
        try:
            response = requests.get(
                self.endpoint_template.format(country=self.country),
                params={
                    "app_id": self.app_id,
                    "app_key": self.app_key,
                    "results_per_page": max_results,
                    "what": query,
                    "where": "India",
                    "sort_by": "date",
                },
                timeout=30,
            )
            response.raise_for_status()
            results = []
            for item in response.json().get("results", []):
                results.append(
                    {
                        "title": item.get("title", "No title"),
                        "url": item.get("redirect_url", ""),
                        "snippet": item.get("description", "")[:1200],
                    }
                )
            return [result for result in results if result["url"]]
        except (requests.RequestException, ValueError) as error:
            print(f"[Error Adzuna]: {error}")
            return []
